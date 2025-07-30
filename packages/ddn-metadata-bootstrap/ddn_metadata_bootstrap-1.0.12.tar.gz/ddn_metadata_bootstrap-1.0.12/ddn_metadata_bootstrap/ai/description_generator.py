#!/usr/bin/env python3

"""
AI-powered description generation for schema elements with intelligent caching.
Handles communication with Anthropic API and description quality control.
Enhanced with acronym expansion BEFORE AI generation for better context.
UPDATED: Now properly uses system_prompt for all AI interactions.
FIXED: Now correctly uses configured field_tokens and kind_tokens limits.
"""

import hashlib
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, Set, Optional, Any, List

import anthropic

from .specificity import WordNetGenericDetector
from ..config import config
from ..utils.text_utils import clean_description_response, refine_ai_description, normalize_description

logger = logging.getLogger(__name__)


@dataclass
class CachedDescription:
    """Represents a cached field description with metadata."""
    description: str
    field_name: str
    entity_name: str
    field_type: str
    context_hash: str
    use_count: int = 0
    quality_score: int = 0


class DescriptionCache:
    """Intelligent caching system for field descriptions with similarity matching."""

    def __init__(self, similarity_threshold: float = 0.85, max_cache_size: int = 10000):
        """
        Initialize the description cache.

        Args:
            similarity_threshold: Minimum similarity score for cache hits (0.0-1.0)
            max_cache_size: Maximum number of cached descriptions
        """
        self.similarity_threshold = similarity_threshold
        self.max_cache_size = max_cache_size

        # Primary cache: exact matches by context hash
        self.exact_cache: Dict[str, CachedDescription] = {}

        # Similarity cache: organized by field name patterns for fast lookup
        self.similarity_cache: Dict[str, List[CachedDescription]] = defaultdict(list)

        # Statistics for monitoring cache performance
        self.stats = {
            'exact_hits': 0,
            'similarity_hits': 0,
            'misses': 0,
            'api_calls_saved': 0
        }

    @staticmethod
    def _is_generic_field(field_name: str) -> bool:
        """Check if field name is generic and should not use cache.
        OPTIMIZED: Hash-based lookups for generic field checking."""

        # OPTIMIZED: Convert to set for O(1) lookup instead of list iteration
        generic_fields_set = getattr(config, '_generic_fields_set', None)
        if generic_fields_set is None:
            # Build optimized lookup set once and cache it
            generic_fields_list = getattr(config, 'generic_fields', [])
            generic_fields_set = {gf.lower() for gf in generic_fields_list}
            # Cache the set on config for future use
            setattr(config, '_generic_fields_set', generic_fields_set)

        # Direct hash lookup instead of iteration
        if field_name.lower() in generic_fields_set:
            return True

        # Check against generic field regex patterns
        generic_fields_regex = getattr(config, 'generic_fields_regex', [])
        for pattern in generic_fields_regex:
            if pattern.match(field_name.lower()):
                return True

        return False

    @staticmethod
    def _generate_context_hash(field_name: str, entity_name: str, field_type: str, business_context: str) -> str:
        """Generate a hash for exact context matching."""
        context_string = f"{field_name}|{entity_name}|{field_type}|{business_context}"
        return hashlib.md5(context_string.encode()).hexdigest()

    @staticmethod
    def _normalize_field_name(field_name: str) -> str:
        """Normalize field name for similarity matching."""
        # Convert to lowercase and split on common separators
        normalized = re.sub(r'[_\-\s]+', '_', field_name.lower())
        # Remove common prefixes/suffixes
        normalized = re.sub(r'^(tbl_|vw_|sp_|fn_)', '', normalized)
        normalized = re.sub(r'_(id|key|ref|fk|pk)$', '', normalized)
        return normalized

    def _calculate_similarity(self, field1: str, field2: str, entity1: str, entity2: str,
                              type1: str, type2: str) -> float:
        """
        Calculate similarity score between two field contexts.

        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Normalize field names for comparison
        norm_field1 = self._normalize_field_name(field1)
        norm_field2 = self._normalize_field_name(field2)

        # Field name similarity (most important factor)
        field_similarity = SequenceMatcher(None, norm_field1, norm_field2).ratio()

        # Entity name similarity (significantly increased importance)
        entity_similarity = SequenceMatcher(None, entity1.lower(), entity2.lower()).ratio()

        # Type similarity
        type_similarity = 1.0 if type1 == type2 else 0.7 if self._types_compatible(type1, type2) else 0.3

        # Rebalanced weighted combination - entity context is now much more important
        # Field name: 50% (reduced from 70%)
        # Entity context: 35% (increased from 10%)
        # Type: 15% (reduced from 20%)
        overall_similarity = (
                field_similarity * 0.5 +
                entity_similarity * 0.35 +
                type_similarity * 0.15
        )

        return overall_similarity

    @staticmethod
    def _types_compatible(type1: str, type2: str) -> bool:
        """Check if two types are compatible for description reuse."""
        # Remove nullable indicators
        clean_type1 = type1.rstrip('!').lower()
        clean_type2 = type2.rstrip('!').lower()

        # Group compatible types
        string_types = {'string', 'text', 'varchar', 'char'}
        number_types = {'int', 'integer', 'float', 'double', 'decimal', 'number'}
        bool_types = {'boolean', 'bool', 'bit'}
        date_types = {'date', 'datetime', 'timestamp', 'time'}

        type_groups = [string_types, number_types, bool_types, date_types]

        for group in type_groups:
            if clean_type1 in group and clean_type2 in group:
                return True

        return clean_type1 == clean_type2

    def get_cached_description(self, field_name: str, entity_name: str, field_type: str, business_context: str) -> \
    Optional[str]:
        """
        Retrieve cached description if available.

        Returns:
            Cached description if found, None otherwise
        """
        # Skip cache for generic fields - they are too context-dependent
        if self._is_generic_field(field_name):
            logger.debug(f"Skipping cache for generic field: {field_name}")
            return None

        # Try exact match first
        context_hash = self._generate_context_hash(field_name, entity_name, field_type, business_context)

        if context_hash in self.exact_cache:
            cached = self.exact_cache[context_hash]
            cached.use_count += 1
            self.stats['exact_hits'] += 1
            logger.debug(f"✅ EXACT CACHE HIT: {entity_name}.{field_name} -> '{cached.description}'")
            return cached.description

        # Try similarity matching
        normalized_field = self._normalize_field_name(field_name)
        candidates = self.similarity_cache.get(normalized_field, [])

        best_match = None
        best_similarity = 0.0

        for cached in candidates:
            similarity = self._calculate_similarity(
                field_name, cached.field_name,
                entity_name, cached.entity_name,
                field_type, cached.field_type
            )

            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = cached

        if best_match:
            best_match.use_count += 1
            self.stats['similarity_hits'] += 1
            self.stats['api_calls_saved'] += 1

            logger.info(f"🎯 SIMILARITY CACHE HIT ({best_similarity:.2f}): "
                        f"{entity_name}.{field_name} -> {best_match.entity_name}.{best_match.field_name}")
            logger.info(f"   Reusing: '{best_match.description}'")

            return best_match.description

        self.stats['misses'] += 1
        return None

    def cache_description(self, field_name: str, entity_name: str, field_type: str, business_context: str,
                          description: str,
                          quality_score: int = 100):
        """Cache a generated description."""
        if not description or quality_score < 40:  # Don't cache low-quality descriptions
            return

        # Don't cache generic fields - they are too context-dependent
        if self._is_generic_field(field_name):
            logger.debug(f"Skipping cache storage for generic field: {field_name}")
            return

        context_hash = self._generate_context_hash(field_name, entity_name, field_type, business_context)

        cached_desc = CachedDescription(
            description=description,
            field_name=field_name,
            entity_name=entity_name,
            field_type=field_type,
            context_hash=context_hash,
            quality_score=quality_score
        )

        # Store in exact cache
        self.exact_cache[context_hash] = cached_desc

        # Store in similarity cache
        normalized_field = self._normalize_field_name(field_name)
        self.similarity_cache[normalized_field].append(cached_desc)

        # Manage cache size
        self._evict_if_needed()

        logger.debug(f"💾 CACHED: {entity_name}.{field_name} -> '{description}'")

    def _evict_if_needed(self):
        """Evict least-used entries if cache is too large."""
        if len(self.exact_cache) <= self.max_cache_size:
            return

        # Sort by use_count (ascending) and quality_score (ascending)
        # This prioritizes keeping frequently used, high-quality descriptions
        sorted_items = sorted(
            self.exact_cache.items(),
            key=lambda x: (x[1].use_count, x[1].quality_score)
        )

        # Remove oldest 10% of entries
        num_to_remove = max(1, len(sorted_items) // 10)

        for context_hash, cached_desc in sorted_items[:num_to_remove]:
            # Remove from exact cache
            del self.exact_cache[context_hash]

            # Remove from similarity cache
            normalized_field = self._normalize_field_name(cached_desc.field_name)
            if normalized_field in self.similarity_cache:
                self.similarity_cache[normalized_field] = [
                    c for c in self.similarity_cache[normalized_field]
                    if c.context_hash != context_hash
                ]

                # Clean up empty lists
                if not self.similarity_cache[normalized_field]:
                    del self.similarity_cache[normalized_field]

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        total_requests = sum(self.stats.values()) - self.stats['api_calls_saved']
        hit_rate = 0.0

        if total_requests > 0:
            total_hits = self.stats['exact_hits'] + self.stats['similarity_hits']
            hit_rate = total_hits / total_requests

        return {
            **self.stats,
            'cache_size': len(self.exact_cache),
            'similarity_patterns': len(self.similarity_cache),
            'hit_rate': hit_rate,
            'api_call_reduction': f"{self.stats['api_calls_saved']} calls saved"
        }


class DescriptionGenerator:
    """Handles AI-powered description generation for schema elements with intelligent caching."""

    def __init__(self, api_key: str, model: Optional[str] = None, enable_caching: bool = True,
                 similarity_threshold: float = 0.85):
        """
        Initialize the description generator.

        Args:
            api_key: Anthropic API key
            model: Model to use (defaults to config value)
            enable_caching: Whether to enable similarity caching
            similarity_threshold: Minimum similarity for cache hits (0.0-1.0)
        """
        self._generic_detector = None
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model or config.model

        # Initialize caching system
        self.enable_caching = enable_caching
        if enable_caching:
            self.cache = DescriptionCache(similarity_threshold=similarity_threshold)
            logger.info(f"🧠 Description caching enabled (similarity threshold: {similarity_threshold})")
        else:
            self.cache = None
        self._generic_detector = WordNetGenericDetector()

    @staticmethod
    def _expand_acronyms_in_field_name(field_name: str, _context: str = "") -> Dict[str, str]:
        """
        Expand acronyms found in field name and return mapping.
        Uses normalized field name components for proper camelCase handling.
        OPTIMIZED: Direct hash lookups instead of iteration.

        Args:
            field_name: The field name to analyze
            _context: Combined context from entity and field information

        Returns:
            Dictionary mapping original acronyms to their expanded meanings
        """
        expansions = {}

        # Use the enhanced field name splitting for proper camelCase handling
        field_parts = DescriptionGenerator._split_field_name(field_name)

        # Get acronym mappings once and ensure it's a dict
        acronym_mappings = getattr(config, 'acronym_mappings', {})
        if not isinstance(acronym_mappings, dict):
            acronym_mappings = {}

        for part in field_parts:
            if len(part) <= 5 and part.isalpha():
                # Direct hash lookup instead of iteration
                part_lower = part.lower()
                if part_lower in acronym_mappings:
                    expansions[part_lower] = acronym_mappings[part_lower]

        return expansions

    @staticmethod
    def _should_attempt_description_generation(field_name: str, _field_data: Dict, _context: Dict) -> bool:
        """
        Fixed pre-screening with proper acronym checking before vowel analysis.
        OPTIMIZED: Hash-based lookups for all acronym sources.

        Args:
            field_name: Name of the field
            _field_data: Field metadata
            _context: Generation context

        Returns:
            True if description generation should be attempted
        """
        field_lower = field_name.lower()

        if len(field_lower) <= 1:
            logger.info(f"⏭️ SKIPPING single-character field '{field_name}'")
            return False

        # Check for known acronyms FIRST - using ALL possible acronym sources
        if len(field_lower) <= 4:
            # OPTIMIZED: Pre-build combined acronym lookup set
            known_terms = set()

            # Get all acronym sources with safe dict checking
            domain_abbreviations = getattr(config, 'domain_abbreviations', {})
            if isinstance(domain_abbreviations, dict):
                default_terms = domain_abbreviations.get('default', set())
                if isinstance(default_terms, (set, list)):
                    known_terms.update(default_terms)

            acronym_meanings = getattr(config, 'acronym_meanings', {})
            if isinstance(acronym_meanings, dict):
                known_terms.update(acronym_meanings.keys())

            acronym_mappings = getattr(config, 'acronym_mappings', {})
            if isinstance(acronym_mappings, dict):
                known_terms.update(acronym_mappings.keys())

            # Check technical patterns
            technical_patterns = [
                r'^[a-z]+_id$', r'^id_[a-z]+$', r'^[a-z]+_cd$',
                r'^[a-z]+_nm$', r'^[a-z]+_dt$', r'^[a-z]+_fl$',
                r'^[a-z]+_ct$', r'^[a-z]+_amt$'
            ]

            is_technical_pattern = any(re.match(pattern, field_lower) for pattern in technical_patterns)
            # OPTIMIZED: Direct hash lookup instead of iteration
            is_known_acronym = field_lower in known_terms

            # If it's a known acronym or technical pattern, allow generation
            if is_known_acronym or is_technical_pattern:
                if is_known_acronym:
                    logger.debug(f"✅ KNOWN ACRONYM: '{field_name}' found in acronym sources")
                return True

            # NOW check vowels - only for truly unknown short fields
            vowel_count = sum(1 for c in field_lower if c in 'aeiou')

            if len(field_lower) > 2 and vowel_count == 0:
                logger.info(f"⏭️ SKIPPING cryptic field '{field_name}' - no vowels, no domain knowledge")
                return False
            elif len(field_lower) <= 3 and vowel_count == 0:
                logger.info(f"⏭️ SKIPPING cryptic abbreviation '{field_name}' - unclear meaning")
                return False

        # Skip metadata fields
        metadata_patterns = [
            r'^_[a-z]+',
            r'^meta_[a-z]+',
            r'^temp_[a-z]+',
            r'^tmp_[a-z]+',
        ]

        if any(re.match(pattern, field_lower) for pattern in metadata_patterns):
            logger.info(f"⏭️ SKIPPING metadata field '{field_name}'")
            return False

        return True

    @staticmethod
    def _build_flag_context(field_lower: str, _business_role: str, entity_name: str) -> str:
        """Build context for boolean flags with acronym expansion.
        OPTIMIZED: Direct hash lookups for acronym meanings."""

        # First check hardcoded flag contexts
        flag_contexts = {
            'enabled': f"controls whether this {entity_name} is active",
            'active': f"indicates if this {entity_name} is operational",
            'available': f"shows whether this {entity_name} can be used",
            'deleted': f"tracks if this {entity_name} has been removed",
            'modified': f"tracks if this {entity_name} has been changed",
            'verified': f"confirms validation of this {entity_name}",
            'approved': f"shows approval status of this {entity_name}",
            'published': f"indicates visibility to users"
        }

        # Handle standard flag prefixes
        if field_lower.startswith('is_'):
            condition = field_lower[3:].replace('_', ' ')
            return f"indicates whether this {entity_name} is {condition}"
        elif field_lower.startswith('has_'):
            condition = field_lower[4:].replace('_', ' ')
            return f"shows whether this {entity_name} has {condition}"
        elif field_lower.startswith('can_'):
            condition = field_lower[4:].replace('_', ' ')
            return f"determines if this {entity_name} can {condition}"

        # Check exact flag contexts
        if field_lower in flag_contexts:
            return flag_contexts[field_lower]

        # Try acronym expansion for more meaningful context
        # Extract the main part (remove _flag, _enabled, etc.)
        flag_base = field_lower
        flag_suffixes = ['_flag', '_enabled', '_disabled', '_active', '_inactive', '_indicator', '_ind']

        for suffix in flag_suffixes:
            if flag_base.endswith(suffix):
                flag_base = flag_base[:-len(suffix)]
                break

        # Split into components and try to expand acronyms
        # OPTIMIZED: Get acronym meanings once and ensure it's a dict
        acronym_meanings = getattr(config, 'acronym_meanings', {})
        if not isinstance(acronym_meanings, dict):
            acronym_meanings = {}

        if flag_base and acronym_meanings:
            components = flag_base.split('_')
            expanded_parts = []
            found_acronym = False

            for part in components:
                # OPTIMIZED: Direct hash lookup
                if part in acronym_meanings:
                    expanded_parts.append(acronym_meanings[part])
                    found_acronym = True
                else:
                    expanded_parts.append(part.title())

            if found_acronym:
                expanded_context = ' '.join(expanded_parts)

                # Create context based on what the acronym represents
                if any(term in expanded_context.lower() for term in
                       ['act', 'law', 'regulation', 'compliance', 'standard']):
                    return f"indicates compliance with {expanded_context} requirements"
                elif any(term in expanded_context.lower() for term in ['system', 'service', 'platform', 'application']):
                    return f"controls activation of {expanded_context} functionality"
                elif any(term in expanded_context.lower() for term in
                         ['security', 'protection', 'authentication', 'authorization']):
                    return f"enables {expanded_context} security controls"
                elif any(term in expanded_context.lower() for term in ['process', 'workflow', 'operation']):
                    return f"controls {expanded_context} process execution"
                else:
                    return f"indicates {expanded_context} status"

        # Enhanced fallback based on field patterns
        if 'compliance' in field_lower or 'compliant' in field_lower:
            return f"indicates regulatory compliance status for this {entity_name}"
        elif 'security' in field_lower or 'secure' in field_lower:
            return f"controls security settings for this {entity_name}"
        elif 'valid' in field_lower or 'validated' in field_lower:
            return f"confirms validation status of this {entity_name}"
        elif 'authorized' in field_lower or 'authorized' in field_lower:
            return f"indicates authorization status for this {entity_name}"
        elif 'critical' in field_lower or 'important' in field_lower:
            return f"marks critical status of this {entity_name}"
        elif 'required' in field_lower or 'mandatory' in field_lower:
            return f"indicates if this {entity_name} is required"
        else:
            # Final fallback - but more specific than before
            return f"controls operational status of this {entity_name}"

    @staticmethod
    def _build_count_context(field_lower: str, components: List[str], _business_role: str, entity_name) -> str:
        """Build context for count fields with acronym expansion.
        OPTIMIZED: Direct hash lookups for acronym meanings."""

        # First check for common count patterns
        if any(comp in ['user', 'member', 'customer'] for comp in components):
            return f"number of users associated with {entity_name}"
        elif any(comp in ['service', 'application', 'app'] for comp in components):
            return f"count of applications connected to {entity_name}"
        elif any(comp in ['error', 'failure', 'exception'] for comp in components):
            return f"number of errors or failures for {entity_name}"
        elif any(comp in ['attempt', 'retry', 'try'] for comp in components):
            return f"number of attempts made for {entity_name}"
        elif any(comp in ['connection', 'session', 'login'] for comp in components):
            return f"count of active connections to {entity_name}"
        elif any(comp in ['transaction', 'txn', 'transfer'] for comp in components):
            return f"number of transactions processed by {entity_name}"
        elif any(comp in ['request', 'call', 'query'] for comp in components):
            return f"count of requests handled by {entity_name}"
        elif any(comp in ['alert', 'notification', 'warning'] for comp in components):
            return f"number of alerts generated for {entity_name}"
        elif any(comp in ['violation', 'breach', 'incident'] for comp in components):
            return f"count of security incidents involving {entity_name}"

        # Try acronym expansion for more meaningful context
        # OPTIMIZED: Get acronym meanings once and ensure it's a dict
        acronym_meanings = getattr(config, 'acronym_meanings', {})
        if not isinstance(acronym_meanings, dict):
            acronym_meanings = {}

        if acronym_meanings:
            # Remove count suffixes to get the base components
            count_suffixes = ['count', 'cnt', 'num', 'number', 'total', 'quantity', 'amount']
            base_components = [comp for comp in components if comp not in count_suffixes]

            expanded_parts = []
            found_acronym = False

            for comp in base_components:
                # OPTIMIZED: Direct hash lookup
                if comp in acronym_meanings:
                    expanded_parts.append(acronym_meanings[comp])
                    found_acronym = True
                else:
                    expanded_parts.append(comp.title())

            if found_acronym and expanded_parts:
                expanded_context = ' '.join(expanded_parts)

                # Create context based on what the acronym represents
                if any(term in expanded_context.lower() for term in ['system', 'service', 'application', 'platform']):
                    return f"number of {expanded_context} instances associated with {entity_name}"
                elif any(term in expanded_context.lower() for term in ['security', 'protection', 'threat', 'incident']):
                    return f"count of {expanded_context} events for {entity_name}"
                elif any(term in expanded_context.lower() for term in ['compliance', 'regulatory', 'audit']):
                    return f"number of {expanded_context} items tracked for {entity_name}"
                elif any(term in expanded_context.lower() for term in ['user', 'identity', 'access', 'authentication']):
                    return f"count of {expanded_context} entities linked to {entity_name}"
                elif any(term in expanded_context.lower() for term in ['endpoint', 'device', 'asset']):
                    return f"number of {expanded_context} devices managed by {entity_name}"
                elif any(term in expanded_context.lower() for term in ['network', 'connection', 'interface']):
                    return f"count of {expanded_context} connections for {entity_name}"
                else:
                    return f"number of {expanded_context} items associated with {entity_name}"

        # Enhanced fallback patterns
        non_count_components = [comp for comp in components
                                if comp not in ['count', 'cnt', 'num', 'number', 'total', 'quantity', 'amount', 'size']]

        if non_count_components:
            items_desc = ' '.join(non_count_components).replace('_', ' ')

            # Contextual descriptions based on field patterns
            if any(pattern in field_lower for pattern in ['fail', 'error', 'exception', 'issue']):
                return f"number of {items_desc} failures recorded for {entity_name}"
            elif any(pattern in field_lower for pattern in ['success', 'complete', 'finished']):
                return f"count of successful {items_desc} operations for {entity_name}"
            elif any(pattern in field_lower for pattern in ['pending', 'waiting', 'queue']):
                return f"number of {items_desc} items awaiting processing for {entity_name}"
            elif any(pattern in field_lower for pattern in ['active', 'running', 'live']):
                return f"count of active {items_desc} instances for {entity_name}"
            elif any(pattern in field_lower for pattern in ['total', 'sum', 'aggregate']):
                return f"total number of {items_desc} items for {entity_name}"
            else:
                return f"quantity of {items_desc} associated with {entity_name}"
        else:
            # Final fallback
            return f"numerical count related to {entity_name}"

    @staticmethod
    def _build_timestamp_context(field_lower: str, components: List[str], _business_role: str, entity_name) -> str:
        """Build context for timestamp fields with acronym expansion.
        OPTIMIZED: Direct hash lookups for acronym meanings."""

        # First check for common timestamp patterns
        if any(comp in ['created', 'creation'] for comp in components):
            return f"when this {entity_name} was created"
        elif any(comp in ['updated', 'modified', 'changed'] for comp in components):
            return f"when this {entity_name} was last modified"
        elif any(comp in ['deleted', 'removed', 'purged'] for comp in components):
            return f"when this {entity_name} was deleted"
        elif any(comp in ['found', 'discovered', 'detected'] for comp in components):
            return f"when this {entity_name} was identified"
        elif any(comp in ['started', 'begin', 'initiated'] for comp in components):
            return f"when this {entity_name} was started"
        elif any(comp in ['completed', 'finished', 'ended'] for comp in components):
            return f"when this {entity_name} was completed"
        elif any(comp in ['deployed', 'installed', 'provisioned'] for comp in components):
            return f"when this {entity_name} was deployed"
        elif any(comp in ['activated', 'enabled', 'turned'] for comp in components):
            return f"when this {entity_name} was activated"
        elif any(comp in ['deactivated', 'disabled', 'suspended'] for comp in components):
            return f"when this {entity_name} was deactivated"
        elif any(comp in ['accessed', 'visited', 'used'] for comp in components):
            return f"when this {entity_name} was last accessed"
        elif any(comp in ['authenticated', 'logged', 'signed'] for comp in components):
            return f"when authentication occurred for this {entity_name}"
        elif any(comp in ['expired', 'expiration', 'expires'] for comp in components):
            return f"when this {entity_name} expires or expired"
        elif any(comp in ['validated', 'verified', 'checked'] for comp in components):
            return f"when this {entity_name} was last validated"
        elif any(comp in ['synchronized', 'synced', 'sync'] for comp in components):
            return f"when this {entity_name} was last synchronized"
        elif any(comp in ['backup', 'backed', 'snapshot'] for comp in components):
            return f"when this {entity_name} was backed up"
        elif any(comp in ['scanned', 'analyzed', 'assessed'] for comp in components):
            return f"when this {entity_name} was last scanned"

        # Try acronym expansion for more meaningful context
        # OPTIMIZED: Get acronym meanings once and ensure it's a dict
        acronym_meanings = getattr(config, 'acronym_meanings', {})
        if not isinstance(acronym_meanings, dict):
            acronym_meanings = {}

        if acronym_meanings:
            # Remove timestamp suffixes to get the base components
            timestamp_suffixes = ['time', 'timestamp', 'date', 'at', 'on', 'when', 'ts', 'dt']
            base_components = [comp for comp in components if comp not in timestamp_suffixes]

            expanded_parts = []
            found_acronym = False
            action_context = None

            for comp in base_components:
                # OPTIMIZED: Direct hash lookup
                if comp in acronym_meanings:
                    expanded_parts.append(acronym_meanings[comp])
                    found_acronym = True
                else:
                    # Check if this component suggests an action
                    if comp in ['created', 'updated', 'modified', 'deleted', 'started', 'completed',
                                'deployed', 'activated', 'scanned', 'validated', 'synchronized']:
                        action_context = comp
                    else:
                        expanded_parts.append(comp.title())

            if found_acronym and expanded_parts:
                expanded_context = ' '.join(expanded_parts)

                # Determine the action based on context
                if action_context:
                    action_map = {
                        'created': 'was created',
                        'updated': 'was last updated',
                        'modified': 'was last modified',
                        'deleted': 'was deleted',
                        'started': 'was started',
                        'completed': 'was completed',
                        'deployed': 'was deployed',
                        'activated': 'was activated',
                        'scanned': 'was last scanned',
                        'validated': 'was last validated',
                        'synchronized': 'was last synchronized'
                    }
                    action = action_map.get(action_context, f'{action_context} occurred')
                    return f"when {expanded_context} {action} for this {entity_name}"

                # Create context based on what the acronym represents
                elif any(term in expanded_context.lower() for term in ['system', 'service', 'application', 'platform']):
                    return f"when {expanded_context} interaction occurred with this {entity_name}"
                elif any(term in expanded_context.lower() for term in
                         ['security', 'protection', 'authentication', 'authorization']):
                    return f"when {expanded_context} security event occurred for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['compliance', 'regulatory', 'audit']):
                    return f"when {expanded_context} compliance check occurred for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['backup', 'recovery', 'restore']):
                    return f"when {expanded_context} operation was performed on this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['scan', 'analysis', 'assessment']):
                    return f"when {expanded_context} was performed on this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['endpoint', 'device', 'asset']):
                    return f"when {expanded_context} event occurred for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['network', 'connection', 'communication']):
                    return f"when {expanded_context} activity occurred for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['integration', 'synchronization', 'sync']):
                    return f"when {expanded_context} process occurred for this {entity_name}"
                else:
                    return f"when {expanded_context} event occurred for this {entity_name}"

        # Enhanced fallback patterns
        non_time_components = [comp for comp in components
                               if comp not in ['time', 'timestamp', 'date', 'at', 'on', 'when', 'ts', 'dt']]

        if non_time_components:
            event_desc = ' '.join(non_time_components).replace('_', ' ')

            # Contextual descriptions based on field patterns
            if any(pattern in field_lower for pattern in ['start', 'begin', 'init']):
                return f"when {event_desc} process began for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['end', 'finish', 'complete', 'done']):
                return f"when {event_desc} process completed for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['last', 'recent', 'latest']):
                return f"when {event_desc} last occurred for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['next', 'scheduled', 'planned']):
                return f"when {event_desc} is scheduled for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['first', 'initial', 'original']):
                return f"when {event_desc} first occurred for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['error', 'fail', 'exception']):
                return f"when {event_desc} error occurred for this {entity_name}"
            elif any(pattern in field_lower for pattern in ['success', 'pass', 'complete']):
                return f"when {event_desc} completed successfully for this {entity_name}"
            else:
                return f"when {event_desc} occurred for this {entity_name}"
        else:
            # Final fallback
            return f"timing information for this {entity_name}"

    @staticmethod
    def _build_data_field_context(field_lower: str, components: List[str], _business_role: str, entity_name: str) -> \
    Optional[str]:
        """Build context for general data fields with acronym expansion - try to be specific or skip.
        OPTIMIZED: Direct hash lookups for acronym meanings."""

        # First check for common data field patterns
        if any(comp in ['name', 'title', 'label'] for comp in components):
            return f"identifies or labels this {entity_name}"
        elif any(comp in ['description', 'desc', 'notes', 'comments'] for comp in components):
            return f"provides descriptive details about this {entity_name}"
        elif any(comp in ['url', 'link', 'address', 'location'] for comp in components):
            return f"specifies location or connection details for this {entity_name}"
        elif any(comp in ['config', 'setting', 'option'] for comp in components):
            return f"configures behavior or options for this {entity_name}"
        elif any(comp in ['version', 'revision', 'build'] for comp in components):
            return f"tracks version or revision information for this {entity_name}"
        elif any(comp in ['owner', 'creator', 'author'] for comp in components):
            return f"identifies responsible party for this {entity_name}"
        elif any(comp in ['category', 'type', 'kind', 'class'] for comp in components):
            return f"classifies or categorizes this {entity_name}"
        elif any(comp in ['priority', 'importance', 'weight'] for comp in components):
            return f"determines priority or importance of this {entity_name}"
        elif any(comp in ['threshold', 'limit', 'max', 'min'] for comp in components):
            return f"sets operational limits or boundaries for this {entity_name}"
        elif any(comp in ['size', 'length', 'width', 'height', 'depth'] for comp in components):
            return f"specifies dimensional measurements for this {entity_name}"
        elif any(comp in ['value', 'amount', 'cost', 'price', 'rate'] for comp in components):
            return f"defines monetary or quantitative value for this {entity_name}"
        elif any(comp in ['path', 'directory', 'folder', 'file'] for comp in components):
            return f"specifies file system location for this {entity_name}"
        elif any(comp in ['port', 'endpoint', 'interface'] for comp in components):
            return f"defines network access point for this {entity_name}"
        elif any(comp in ['protocol', 'method', 'algorithm'] for comp in components):
            return f"specifies technical approach used by this {entity_name}"
        elif any(comp in ['token', 'key', 'secret', 'credential'] for comp in components):
            return f"provides authentication material for this {entity_name}"
        elif any(comp in ['policy', 'rule', 'constraint'] for comp in components):
            return f"defines operational rules for this {entity_name}"
        elif any(comp in ['template', 'pattern', 'format'] for comp in components):
            return f"specifies structural template for this {entity_name}"
        elif any(comp in ['role', 'permission', 'access', 'privilege'] for comp in components):
            return f"defines access rights for this {entity_name}"
        elif any(comp in ['environment', 'context', 'scope'] for comp in components):
            return f"defines operational context for this {entity_name}"
        elif any(comp in ['mode', 'state', 'phase'] for comp in components):
            return f"indicates operational mode of this {entity_name}"
        elif any(comp in ['source', 'origin', 'provider'] for comp in components):
            return f"identifies data source for this {entity_name}"
        elif any(comp in ['target', 'destination', 'recipient'] for comp in components):
            return f"specifies target destination for this {entity_name}"
        elif any(comp in ['hash', 'checksum', 'signature'] for comp in components):
            return f"provides data integrity verification for this {entity_name}"
        elif any(comp in ['encoding', 'format', 'codec'] for comp in components):
            return f"specifies data encoding method for this {entity_name}"

        # Try acronym expansion for more meaningful context
        # OPTIMIZED: Get acronym meanings once and ensure it's a dict
        acronym_meanings = getattr(config, 'acronym_meanings', {})
        if not isinstance(acronym_meanings, dict):
            acronym_meanings = {}

        if acronym_meanings:
            expanded_parts = []
            found_acronym = False

            for comp in components:
                # OPTIMIZED: Direct hash lookup
                if comp in acronym_meanings:
                    expanded_parts.append(acronym_meanings[comp])
                    found_acronym = True
                else:
                    expanded_parts.append(comp.title())

            if found_acronym and expanded_parts:
                expanded_context = ' '.join(expanded_parts)

                # Create context based on what the acronym represents
                if any(term in expanded_context.lower() for term in ['identifier', 'id', 'key', 'number']):
                    return f"uniquely identifies {expanded_context} for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['system', 'service', 'application', 'platform']):
                    return f"references {expanded_context} associated with this {entity_name}"
                elif any(term in expanded_context.lower() for term in
                         ['security', 'protection', 'authentication', 'authorization']):
                    return f"manages {expanded_context} settings for this {entity_name}"
                elif any(term in expanded_context.lower() for term in
                         ['compliance', 'regulatory', 'audit', 'governance']):
                    return f"tracks {expanded_context} requirements for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['configuration', 'setting', 'parameter']):
                    return f"configures {expanded_context} behavior for this {entity_name}"
                elif any(term in expanded_context.lower() for term in
                         ['network', 'connection', 'communication', 'protocol']):
                    return f"defines {expanded_context} connectivity for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['endpoint', 'device', 'asset', 'hardware']):
                    return f"identifies {expanded_context} associated with this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['management', 'administration', 'control']):
                    return f"enables {expanded_context} capabilities for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['integration', 'interface', 'api']):
                    return f"facilitates {expanded_context} interaction with this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['monitoring', 'logging', 'tracking']):
                    return f"supports {expanded_context} activities for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['backup', 'recovery', 'restore', 'archive']):
                    return f"manages {expanded_context} operations for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['virtualization', 'container', 'cloud']):
                    return f"controls {expanded_context} environment for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['database', 'storage', 'repository']):
                    return f"specifies {expanded_context} location for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['user', 'identity', 'account', 'person']):
                    return f"associates {expanded_context} with this {entity_name}"
                elif any(
                        term in expanded_context.lower() for term in ['process', 'workflow', 'operation', 'procedure']):
                    return f"controls {expanded_context} execution for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['certificate', 'credential', 'token']):
                    return f"provides {expanded_context} authentication for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['policy', 'rule', 'standard', 'guideline']):
                    return f"enforces {expanded_context} requirements for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['risk', 'threat', 'vulnerability', 'incident']):
                    return f"tracks {expanded_context} assessment for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['report', 'metric', 'measurement', 'analytics']):
                    return f"provides {expanded_context} data for this {entity_name}"
                elif any(term in expanded_context.lower() for term in ['license', 'subscription', 'entitlement']):
                    return f"manages {expanded_context} rights for this {entity_name}"
                else:
                    # Generic but meaningful fallback with expanded context
                    return f"manages {expanded_context} information for this {entity_name}"

        # Enhanced pattern-based fallbacks
        if any(pattern in field_lower for pattern in ['external', 'remote', 'foreign']):
            return f"references external resource for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['internal', 'local', 'private']):
            return f"manages internal resource for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['public', 'shared', 'common']):
            return f"provides shared resource for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['custom', 'user', 'manual']):
            return f"stores customizable setting for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['auto', 'automatic', 'generated']):
            return f"contains automatically generated value for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['temp', 'temporary', 'cache']):
            return f"holds temporary data for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['backup', 'archive', 'history']):
            return f"preserves historical data for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['default', 'standard', 'base']):
            return f"defines default behavior for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['override', 'custom', 'special']):
            return f"provides override capability for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['summary', 'aggregate', 'total']):
            return f"summarizes related data for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['reference', 'ref', 'link']):
            return f"establishes reference connection for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['index', 'position', 'order']):
            return f"defines positional information for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['filter', 'criteria', 'condition']):
            return f"specifies filtering criteria for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['result', 'outcome', 'response']):
            return f"captures operation result for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['message', 'text', 'content']):
            return f"contains textual content for this {entity_name}"
        elif any(pattern in field_lower for pattern in ['meta', 'metadata', 'header']):
            return f"provides metadata information for this {entity_name}"
        else:
            # If we can't be specific, return None to trigger skipping
            return None

    @staticmethod
    def _split_field_name(field_name: str) -> List[str]:
        """Split field name into components for analysis."""
        import inflection

        # Handle mixed cases: if already has underscores, process each part separately
        if '_' in field_name:
            parts = field_name.split('_')
            processed_parts = []
            for part in parts:
                if part and any(c.isupper() for c in part[1:]):  # Has internal capitals (camelCase)
                    # Apply inflection to camelCase parts
                    processed_parts.extend(inflection.underscore(part).split('_'))
                else:
                    # Keep snake_case parts as-is
                    processed_parts.append(part)
            return [part.lower() for part in processed_parts if part]
        else:
            # Pure camelCase - use inflection directly
            snake_case = inflection.underscore(field_name)
            return [part.lower() for part in snake_case.split('_') if part]

    @staticmethod
    def _build_field_description_prompt(field_name: str, entity_name: str,
                                        acronym_expansions: Dict[str, str] = None) -> str:
        """
        Build prompt with entity context and optional acronym expansions.
        """

        display_concept = field_name.replace('_', ' ')

        prompt_parts = [
            f"Entity: {entity_name}",
            f"Field: {display_concept}",
        ]

        if acronym_expansions:
            expansions_text = ", ".join(
                [f"{acronym.upper()}={meaning}" for acronym, meaning in acronym_expansions.items()])
            prompt_parts.append(f"Acronym meanings: {expansions_text}")

        prompt_parts.extend([
            "",
            "Write a noun phrase describing what this field represents.",
            "",
            "RULES:",
            f"- NEVER include '{field_name}' or '{display_concept}' in your response",
            "- NOUN PHRASE ONLY (no 'contains', 'stores', 'represents', 'is')",
            "- Use spaces, never underscores",
            f"- Maximum {config.short_field_target} characters",
            "- Be specific: 'User account identifier' not just 'Unique identifier'",
            "- NEVER use 'unique' - most IDs are references, not unique within this entity",  # NEW RULE
            "- For 'Type' fields: specify what kind of type (e.g., 'User access type', 'Payment method type')",
            "",
            "Examples:",
            "GOOD: 'Project identifier', 'Member access type', 'Resource classification level'",
            "GOOD: 'In security review, Permissions under review', 'Data in transit', 'Items awaiting approval'",
            "BAD: 'Unique identifier', 'Type of member', 'The applied resource'",
            "",
            "Noun phrase:"
        ])

        return "\n".join(prompt_parts)

    @staticmethod
    def _validate_response_format(description: str, field_name: str) -> Dict[str, Any]:
        """
        Pre-validate response format before quality assessment.
        """

        description_lower = description.lower().strip()
        field_lower = field_name.lower()
        display_concept = field_name.replace('_', ' ').lower()

        # Check for field name inclusion
        if field_lower in description_lower or display_concept in description_lower:
            return {
                'valid': False,
                'issue': 'field_name_included',
                'message': f"Response includes field name '{field_name}'"
            }

        # Check for underscores
        if '_' in description:
            return {
                'valid': False,
                'issue': 'underscores_present',
                'message': "Response contains underscores"
            }

        # Check for verb phrase indicators
        verb_indicators = ['contains', 'stores', 'holds', 'represents', 'indicates', 'shows', 'tracks', 'manages']
        if any(verb in description_lower for verb in verb_indicators):
            return {
                'valid': False,
                'issue': 'verb_phrase_detected',
                'message': "Response uses verb phrase - must be noun phrase only"
            }

        return {'valid': True}

    def generate_field_description_with_quality_check(self, field_data: Dict[str, Any], context: Dict[str, Any]) -> \
    Optional[str]:
        """
        Generate field description with enhanced context and format validation.
        """
        field_name = field_data.get('name', '')
        entity_name = context.get('parent_name', context.get('entity_name', ''))
        field_type = field_data.get('type', field_data.get('outputType', ''))

        if not self._should_attempt_description_generation(field_name, field_data, context):
            return None

        value_assessment = self._should_generate_description_for_value(field_name, field_data, context)

        if not value_assessment['should_generate']:
            logger.info(f"⏭️ SKIPPING '{field_name}' - {value_assessment['reason']}: {value_assessment['value_add']}")
            return None

        logger.info(f"🎯 GENERATING '{field_name}' - {value_assessment['reason']}: {value_assessment['value_add']}")

        acronym_expansions = value_assessment.get('acronym_expansions', {})

        if acronym_expansions:
            logger.info(f"🔍 ACRONYM EXPANSIONS for '{field_name}': {acronym_expansions}")

        # Try cache first - include field type in context for better matching
        if self.enable_caching and self.cache:
            cache_context = f"entity:{entity_name}|reason:{value_assessment['reason']}"
            if field_type:
                cache_context += f"|type:{field_type}"
            if acronym_expansions:
                acronym_cache = ','.join([f"{k}={v}" for k, v in acronym_expansions.items()])
                cache_context += f"|acronyms:{acronym_cache}"

            cached_description = self.cache.get_cached_description(
                field_name, entity_name, field_type or '', cache_context
            )
            if cached_description:
                return cached_description

        # Try up to configured attempts with enhanced prompts
        max_attempts = getattr(config, 'max_description_retry_attempts', 3)
        best_description = None
        best_score = 0

        for attempt in range(max_attempts):
            # Build prompt with field type context if available
            prompt = self._build_field_description_prompt(field_name, entity_name, acronym_expansions)

            # Add field type context if available
            if field_type:
                prompt = prompt.replace("Write a noun phrase", f"Data type: {field_type}\n\nWrite a noun phrase")

            # Add attempt-specific guidance
            if attempt == 1:
                prompt += "\nBe more specific about the business context."
            elif attempt == 2:
                prompt += "\nFocus on the most essential meaning."

            try:
                description = self._make_api_call(prompt, config.field_tokens)
            except Exception as e:
                logger.error(f"❌ API ERROR: {e}")
                continue

            if not description:
                continue

            description = description.strip().strip('"\'')

            # Pre-validate format
            format_check = self._validate_response_format(description, field_name)

            if not format_check['valid']:
                logger.info(f"   Attempt {attempt + 1}: ❌ REJECTED - {format_check['message']}")
                continue

            assessment = self._assess_description_quality(description, field_name, entity_name, acronym_expansions=acronym_expansions)
            logger.info(f"   Attempt {attempt + 1}: '{description}' (Score: {assessment['score']})")

            if assessment['score'] == 0:
                logger.info(f"   ❌ REJECTED: {', '.join(assessment['issues'])}")
                continue

            if assessment['score'] > best_score:
                best_score = assessment['score']
                best_description = description

            if assessment['should_include']:
                logger.info(f"   ✅ ACCEPTED: Score {assessment['score']}")

                # Cache the successful description
                if self.enable_caching and self.cache:
                    cache_context = f"entity:{entity_name}|reason:{value_assessment['reason']}"
                    if field_type:
                        cache_context += f"|type:{field_type}"
                    if acronym_expansions:
                        acronym_cache = ','.join([f"{k}={v}" for k, v in acronym_expansions.items()])
                        cache_context += f"|acronyms:{acronym_cache}"
                    self.cache.cache_description(
                        field_name, entity_name, field_type or '', cache_context, description, assessment['score']
                    )

                return description

        # Handle marginal descriptions
        minimum_marginal_score = getattr(config, 'minimum_marginal_score', 40)
        if best_score >= minimum_marginal_score and best_description:
            logger.info(f"   ⚠️ MARGINAL: Using best description (Score: {best_score})")
            return best_description

        logger.info(f"   ❌ REJECTED ALL: No description met quality threshold (Best: {best_score})")
        return None

    def _should_generate_description_for_value(self, field_name: str, _field_data: Dict, context: Dict) -> Dict[
        str, Any]:
        """
        Enhanced value assessment with proper order and existing config usage.
        """
        # field_lower = field_name.lower()
        entity_name = context.get('entity_name', context.get('parent_name', ''))

        # Check if field name is self-explanatory FIRST
        if self._is_self_explanatory(field_name):
            return {
                'should_generate': False,
                'reason': 'self_explanatory',
                'value_add': 'Field name is already clear and descriptive'
            }

        # Check for acronym expansion opportunities
        acronym_expansions = self._expand_acronyms_in_field_name(field_name, entity_name)

        if acronym_expansions:
            expanded_meanings = ', '.join([f"{k.upper()}={v}" for k, v in acronym_expansions.items()])
            return {
                'should_generate': True,
                'reason': f'acronym_expansion',
                'value_add': f'Expands: {expanded_meanings}',
                'acronym_expansions': acronym_expansions
            }

        # Check for domain-specific terms that benefit from entity context
        domain_value = self._assess_domain_context_value(field_name, context)
        if domain_value['adds_value']:
            return {
                'should_generate': True,
                'reason': 'domain_context',
                'value_add': domain_value['explanation'],
                'domain_terms': domain_value['terms']
            }

        # Check if field appears cryptic or needs clarification
        if len(field_name) <= 6:
            return {
                'should_generate': True,
                'reason': 'cryptic_name',
                'value_add': f'Short field name may need clarification in {entity_name} context',
                'entity_context': entity_name
            }

        # Check for technical terms that need business translation
        technical_terms = self._find_technical_terms_needing_translation(field_name)
        if technical_terms:
            return {
                'should_generate': True,
                'reason': 'technical_translation',
                'value_add': f'Translates technical terms: {", ".join(technical_terms)}',
                'technical_terms': technical_terms
            }

        # Check if field name is ambiguous or cryptic
        ambiguity_check = self._generic_detector.assess_field_name_clarity(field_name)
        if not ambiguity_check['is_clear']:
            return {
                'should_generate': True,
                'reason': 'ambiguous_name',
                'value_add': f'Clarifies meaning: {ambiguity_check["issues"]}',
                'clarity_issues': ambiguity_check['issues']
            }

        # Default to skip if no clear value is identified
        return {
            'should_generate': False,
            'reason': 'no_value_add',
            'value_add': 'No meaningful enhancement beyond field name'
        }

    @staticmethod
    def _build_ultra_explicit_prompt(field_name: str, entity_name: str,
                                     acronym_expansions: Dict[str, str] = None) -> str:
        """
        Extremely explicit prompt for difficult cases.
        """

        prompt = f"""Write a short noun phrase describing a data concept.

    CONTEXT: {entity_name} entity
    CONCEPT: {field_name.replace('_', ' ')}"""

        if acronym_expansions:
            prompt += f"\nACRONYMS: {', '.join([f'{k}={v}' for k, v in acronym_expansions.items()])}"

        prompt += f"""

    STRICT RULES:
    1. Write ONLY a noun phrase (like "customer account number")
    2. Maximum {config.short_field_target} characters
    3. Do NOT write: {field_name}, {field_name.replace('_', ' ')}
    4. Do NOT use: contains, stores, represents, indicates, shows, tracks
    5. Use spaces between words, never underscores

    GOOD examples: "Risk assessment score", "Payment method type", "User access level"
    BAD examples: "Field that contains...", "status_code", "The {field_name} represents..."

    Write only the noun phrase:"""

        return prompt

    @staticmethod
    def _build_minimal_strict_prompt(field_name: str, entity_name: str) -> str:
        """
        Minimal prompt for final attempt.
        """

        concept = field_name.replace('_', ' ')

        return f"""Entity: {entity_name}
    Concept: {concept}

    Write a noun phrase (like "customer ID" or "payment status"):
    - Maximum {config.short_field_target} characters
    - No verbs, no field name repetition
    - Spaces only, no underscores

    Noun phrase:"""

    def _make_api_call(self, prompt: str, max_tokens: int) -> str:
        """
        Make API call to Anthropic with system prompt included.

        Args:
            prompt: User prompt content
            max_tokens: Maximum tokens for response

        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]

        # Prepare system prompt separately
        system_prompt = None
        if config.system_prompt and config.system_prompt.strip():
            system_prompt = config.system_prompt.strip()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages,
            system=system_prompt
        )

        return response.content[0].text.strip() if response and response.content else ""

    def _assess_description_quality(self, description: str, _field_name: str, entity_name: str, kind: str = 'field', acronym_expansions: Dict[str, str] = None) -> \
            Dict[str, Any]:
        """
        ULTRA-AGGRESSIVE quality assessment with hard length limits and severe penalties.
        """
        score = 100
        issues = []
        recommendations = []

        description_lower = description.lower().strip()
        # entity_lower = entity_name.lower()
        # field_lower = field_name.lower()

        # IMMEDIATE REJECTION: Length violations (MOST IMPORTANT)
        # Use appropriate config value based on element type
        if kind.upper() == 'OBJECTTYPE':
            max_length = config.kind_desc_max_length
        else:
            max_length = config.field_desc_max_length

        if len(description) > max_length:
            # score = 0
            issues.append(f"WAY TOO LONG: {len(description)} chars (max {max_length})")
            recommendations.append(f"Respond with maximum {max_length // 2} characters")
            logger.info(f"❌ LENGTH VIOLATION: {len(description)} chars > {max_length} in '{description[:100]}...'")
            return {
                'score': 0,
                'should_include': False,
                'issues': issues,
                'recommendations': recommendations,
                'assessment': 'REJECTED - Too verbose'
            }

        # IMMEDIATE REJECTION: Contains underscores (technical formatting)
        if '_' in description:
            # score = 0
            issues.append("Contains underscores - use natural language with spaces")
            recommendations.append("Use spaces between words, not underscores")
            logger.info(f"❌ UNDERSCORE VIOLATION: '{description}'")
            return {
                'score': 0,
                'should_include': False,
                'issues': issues,
                'recommendations': recommendations,
                'assessment': 'REJECTED - Technical formatting'
            }

        # CONTEXTUAL REJECTION: Generic/buzzword language (only if not relevant to entity)
        buzzwords = config.buzzwords

        # Only reject terms if they're not actually relevant to the entity's purpose
        entity_name_lower = entity_name.lower()

        # Find terms that are irrelevant (not in entity name) but present in description
        found_irrelevant_buzzwords = []
        acronym_terms = set()
        if acronym_expansions:
            for expansion in acronym_expansions.values():
                expansion_words = expansion.lower().split()
                acronym_terms.update(expansion_words)
        for buzzword in buzzwords:
            if buzzword not in entity_name_lower and buzzword not in acronym_terms and buzzword in description_lower:
                found_irrelevant_buzzwords.append(buzzword)

        if found_irrelevant_buzzwords:
            # score = 0
            issues.append(f"Uses irrelevant buzzwords: {', '.join(found_irrelevant_buzzwords)}")
            recommendations.append("Use specific business terminology relevant to this entity")
            logger.info(f"❌ IRRELEVANT BUZZWORDS: {found_irrelevant_buzzwords} in '{description}'")
            return {
                'score': 0,
                'should_include': False,
                'issues': issues,
                'recommendations': recommendations,
                'assessment': 'REJECTED - Irrelevant buzzwords'
            }

        # IMMEDIATE REJECTION: Forbidden patterns (explanatory format and generic jargon)
        forbidden_patterns = config.forbidden_patterns

        for pattern in forbidden_patterns:
            if re.search(pattern, description_lower):
                # score = 0
                issues.append("Uses forbidden explanatory format or generic jargon")
                recommendations.append("State the business concept directly")
                logger.info(f"❌ FORBIDDEN PATTERN: '{pattern}' in '{description}'")
                return {
                    'score': 0,
                    'should_include': False,
                    'issues': issues,
                    'recommendations': recommendations,
                    'assessment': 'REJECTED - Forbidden pattern'
                }

        # IMMEDIATE REJECTION: Technical type explanations
        technical_type_patterns = config.technical_type_patterns

        for pattern in technical_type_patterns:
            if re.search(pattern, description_lower):
                # score = 0
                issues.append("Contains technical implementation details")
                recommendations.append("State what business concept this represents, not how it works")
                logger.info(f"❌ TECHNICAL DETAIL: '{pattern}' in '{description}'")
                return {
                    'score': 0,
                    'should_include': False,
                    'issues': issues,
                    'recommendations': recommendations,
                    'assessment': 'REJECTED - Technical details'
                }

        # HEAVY PENALTY: Still too long but under max_length
        target_length = config.short_kind_target if kind.upper() == 'OBJECTTYPE' else config.short_field_target

        if len(description) > target_length:
            score -= 60
            issues.append(f"Too long: {len(description)} chars (target: {target_length})")
            recommendations.append("Be much more concise")
        elif len(description) > target_length // 2:
            score -= 20
            issues.append("Could be more concise")

        # BONUS: Reward ultra-concise, direct descriptions
        if len(description) <= target_length // 3 and not any(word in description_lower for word in ['the', 'a', 'an']):
            score += 20
            logger.debug(f"✅ CONCISE BONUS: +20 points for {len(description)} chars")

        # BONUS: Reward direct business meaning (no verbs)
        direct_patterns = [
            r'^[A-Z][a-z]+\s+(ID|identifier|number|code|name|status|flag|date|time)',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s+(status|flag|identifier)',
            r'^\w+\s+\w+\s+(encryption\s+)?keys?'
        ]

        if any(re.match(pattern, description) for pattern in direct_patterns):
            score += 15
            logger.debug(f"✅ DIRECT FORMAT BONUS: +15 points")

        # Final length check
        if len(description) < 10:
            score -= 30
            issues.append("Too brief - needs more context")

        minimum_score = getattr(config, 'minimum_description_score', 70)
        should_include = score >= minimum_score

        return {
            'score': max(0, score),
            'should_include': should_include,
            'issues': issues,
            'recommendations': recommendations,
            'assessment': self._get_quality_assessment(score)
        }

    @staticmethod
    def _build_kind_prompt(semantic_info: Dict[str, Any], _kind: str, max_len: int, _domain_context: str) -> str:
        """Build a clearer prompt for entity descriptions."""
        name = semantic_info["name"]
        # entity_description = semantic_info["entity_description"]

        # Use config value instead of hardcoded limit
        hard_limit = min(config.short_kind_target, max_len // 2)

        return f"""Describe what data the '{name}' entity contains.

RULES:
- Maximum {hard_limit} characters
- Format: Noun phrase only (not a complete sentence)
- Use natural language with spaces (no underscores)
- Be direct and business-focused
- DO NOT repeat the entity name in your response
- NO FLUFF WORDS: avoid "contains", "information about", "including", "details", "data", "metadata"
- Start with the actual business concept, not generic descriptions

Example: "Authentication settings and publisher verification for single-page applications"

Describe in {hard_limit} characters or less:"""

    @staticmethod
    def _build_concise_kind_prompt(semantic_info: Dict[str, Any], _kind: str, target_len: int,
                                   _domain_context: str) -> str:
        """Build simpler concise kind prompt."""
        name = semantic_info["name"]

        # Use config value instead of hardcoded limit
        hard_limit = min(config.short_kind_target, target_len)

        return f"""What data does this entity contain?

    Context: {name}
    Rules: Maximum {hard_limit} characters, natural language.
    NO fluff words: "contains", "information", "details", "data", "metadata", "including"
    State the business concept directly.

    Response:"""

    @staticmethod
    def _build_enhanced_prompt_with_acronyms(field_name: str, _field_type: str,
                                             _business_context: str, _domain_context: str,
                                             max_len: int, acronym_expansions: Dict[str, str]) -> str:
        """
        ULTRA-AGGRESSIVE prompt with hard character limits and strong constraints.
        """
        # Use config-derived limit instead of hardcoded value
        hard_limit = min(config.short_field_target, max_len // 2)

        prompt_parts = [
            f"DESCRIBE: '{field_name}'",
        ]

        # Add acronym expansions if any were found
        if acronym_expansions:
            expansions_text = ", ".join(
                [f"{acronym.upper()}={meaning}" for acronym, meaning in acronym_expansions.items()])
            prompt_parts.append(f"Acronyms: {expansions_text}")

        prompt_parts.extend([
            f"MAXIMUM {hard_limit} CHARACTERS - WILL BE REJECTED IF LONGER",
            "FORBIDDEN WORDS: contains, stores, holds, represents, enables, facilitates, information, details, data, metadata, including",
            "FORBIDDEN: explanations, definitions, examples, business context phrases",
            "REQUIRED: Direct business concept only",
            "Example: 'Customer account number' (23 chars)",
            f"RESPOND IN {hard_limit} CHARS:"
        ])

        return "\n".join(prompt_parts)

    @staticmethod
    def _build_field_prompt(semantic_info: Dict[str, Any], _field_type: str, max_len: int, _domain_context: str) -> str:
        """Build ULTRA-AGGRESSIVE prompt for standard field description."""
        business_context = semantic_info["business_context"]
        name = semantic_info["name"]

        # Use config-derived limit instead of hardcoded value
        hard_limit = min(config.short_field_target, max_len // 3)

        prompt = f"""'{name}' = ?
    Context: {business_context}
    MAX {hard_limit} CHARS - WILL REJECT IF LONGER
    NO: contains/stores/represents/enables/information/details/data/metadata/including
    YES: Direct business concept
    Example: 'Customer account number'
    RESPOND:"""

        return prompt

    def generate_kind_description(self, data: Dict, context: Dict) -> str:
        """
        Generate a description for a schema kind using explicit business context.
        Updated to pass kind parameter to quality assessment.
        """
        kind = context.get('kind')
        element_name = context.get('name')

        if not kind or not element_name:
            return ""

        # Check if technical name is sufficient
        if self.is_technical_name_sufficient(element_name, 'entity'):
            return ""

        max_len = config.kind_desc_max_length
        target_len = config.short_kind_target

        entity_description = context.get('entity_description', '')

        # Get domain context
        detected_domains = self._extract_domains_from_context(data, context)
        domain_context = self._get_domain_context(data, detected_domains)

        semantic_info = self._extract_element_semantics(element_name, kind, entity_description)

        logger.info(f"🎯 {kind.upper()}: {element_name}")
        logger.info(f"   Domain: {detected_domains[0] if detected_domains else 'default'}")

        prompt = self._build_kind_prompt(semantic_info, kind, max_len, domain_context)

        logger.info(f"   Prompt: {prompt}")

        try:
            desc = self._make_api_call(prompt, config.kind_tokens)
            logger.info(f"   Raw: '{desc}'")

            desc = clean_description_response(desc)
            desc = refine_ai_description(desc)

            # Pass kind parameter to quality assessment
            quality_result = self._assess_description_quality(desc, element_name, element_name, kind)

            if (len(desc) <= max_len and
                    quality_result['should_include'] and
                    len(desc.split()) >= 2):
                final_desc = normalize_description(desc, line_length=config.line_length,
                                                   make_token_efficient=True)
                logger.info(f"✅ SUCCESS: '{final_desc}' ({len(final_desc)} chars)")
                return final_desc

            # Retry with concise prompt
            shorter_prompt = self._build_concise_kind_prompt(semantic_info, kind, target_len, domain_context)
            # FIX: Use config-based calculation for shorter tokens
            shorter_tokens = max(config.kind_tokens // 3, int(target_len / 4))

            desc_short = self._make_api_call(shorter_prompt, shorter_tokens)

            desc_short = clean_description_response(desc_short)
            desc_short = refine_ai_description(desc_short)

            # Pass kind parameter to quality assessment for retry
            quality_result_short = self._assess_description_quality(desc_short, element_name, element_name, kind)

            if quality_result_short['should_include'] and desc_short and len(desc_short.split()) >= 2:
                final_desc_short = normalize_description(desc_short, line_length=config.line_length,
                                                         make_token_efficient=True)
                logger.info(f"✅ RETRY SUCCESS: '{final_desc_short}' ({len(final_desc_short)} chars)")
                return final_desc_short

            logger.error(f"❌ FAILED: {element_name} ({kind})")
            return ""

        except Exception as e:
            logger.error(f"❌ API ERROR for {kind} '{element_name}': {e}")
            return ""

    def _is_self_explanatory(self, field_name: str) -> bool:
        # Use same normalization as the rest of the system
        normalized_parts = self._split_field_name(field_name)
        normalized_field = '_'.join(normalized_parts)

        # Check against compiled self-explanatory patterns from config
        for pattern in config.compiled_self_explanatory_patterns:
            if pattern.match(normalized_field):
                return True

    @staticmethod
    def _build_acronym_expansion_prompt(field_name: str, _field_type: str,
                                        acronym_expansions: Dict[str, str], _domain_context: str) -> str:
        """Build ULTRA-AGGRESSIVE prompt for acronym expansion with hard limits."""
        expansions_text = ", ".join([f"{acronym.upper()}={meaning}" for acronym, meaning in acronym_expansions.items()])

        return f"""EXPAND ACRONYMS ONLY: '{field_name}'
Acronyms: {expansions_text}
RULES:
- MAXIMUM 50 CHARACTERS TOTAL
- USE NATURAL LANGUAGE WITH SPACES
- NO UNDERSCORES OR TECHNICAL FORMATTING
- USE PROPER CAPITALIZATION
- NO 'CONTAINS', 'STORES', 'REPRESENTS'
Example: 'Payment Card Industry compliance status'
RESPOND WITH NATURAL LANGUAGE:"""

    @staticmethod
    def _build_technical_translation_prompt(field_name: str, _field_type: str,
                                            technical_terms: List[str], _domain_context: str) -> str:
        """Build ULTRA-AGGRESSIVE prompt for technical translation."""
        terms_text = ", ".join(technical_terms)

        return f"""TRANSLATE TECHNICAL TERMS: '{field_name}'
    Technical: {terms_text}
    RULES:
    - MAXIMUM 50 CHARACTERS
    - BUSINESS TERMS ONLY
    - NO EXPLANATIONS
    - NO 'CONTAINS', 'STORES' 
    Example: 'Central Processing Unit usage percentage'
    50 CHARS MAX:"""

    @staticmethod
    def _build_domain_context_prompt(field_name: str, _field_type: str,
                                     _domain_terms: List[str], _context: Dict, _domain_context: str) -> str:
        """Build ULTRA-AGGRESSIVE prompt for domain clarification."""

        return f"""CLARIFY DOMAIN TERM: '{field_name}'
    RULES:
    - MAXIMUM 40 CHARACTERS
    - SPECIFY EXACT TYPE
    - NO GENERIC TERMS
    Example: 'Credit risk assessment score'
    40 CHARS MAX:"""

    @staticmethod
    def _build_concise_field_prompt(semantic_info: Dict[str, Any], _field_type: str, _target_len: int,
                                    _domain_context: str) -> str:
        """Build ULTRA-CONCISE prompt."""
        name = semantic_info["name"]

        return f"'{name}' means: [MAX 30 CHARS]"

    def _find_technical_terms_needing_translation(self, field_name: str) -> List[str]:
        """Identify technical terms that would benefit from business translation."""
        # field_lower = field_name.lower()
        components = self._split_field_name(field_name)

        technical_terms_map = {
            # Infrastructure/System terms
            'cpu': 'Central Processing Unit',
            'ram': 'Random Access Memory',
            'ssd': 'Solid State Drive',
            'gpu': 'Graphics Processing Unit',
            'nic': 'Network Interface Card',
            'uuid': 'Universally Unique Identifier',
            'guid': 'Globally Unique Identifier',
            'fqdn': 'Fully Qualified Domain Name',
            'cidr': 'Classless Inter-Domain Routing',
            'vlan': 'Virtual Local Area Network',
            'dhcp': 'Dynamic Host Configuration Protocol',

            # Security terms
            'tls': 'Transport Layer Security',
            'ssl': 'Secure Sockets Layer',
            'cert': 'Certificate',
            'auth': 'Authentication',
            'authz': 'Authorization',
            'rbac': 'Role-Based Access Control',
            'acl': 'Access Control List',
            'pki': 'Public Key Infrastructure',

            # Protocol/Network terms
            'tcp': 'Transmission Control Protocol',
            'udp': 'User Datagram Protocol',
            'http': 'HyperText Transfer Protocol',
            'https': 'HTTP Secure',
            'ftp': 'File Transfer Protocol',
            'sftp': 'Secure File Transfer Protocol',
            'smtp': 'Simple Mail Transfer Protocol',
            'dns': 'Domain Name System',
            'ip': 'Internet Protocol',

            # Database/Storage terms
            'db': 'Database',
            'sql': 'Structured Query Language',
            'nosql': 'Not Only SQL',
            'blob': 'Binary Large Object',
            'json': 'JavaScript Object Notation',
            'xml': 'eXtensible Markup Language',
            'csv': 'Comma-Separated Values',

            # Measurement terms
            'pct': 'Percentage',
            'avg': 'Average',
            'min': 'Minimum',
            'max': 'Maximum',
            'std': 'Standard',
            'dev': 'Deviation',
            'ms': 'Milliseconds',
            'kb': 'Kilobytes',
            'mb': 'Megabytes',
            'gb': 'Gigabytes',
            'tb': 'Terabytes'
        }

        found_terms = []
        for component in components:
            if component.lower() in technical_terms_map:
                found_terms.append(component.lower())

        return found_terms

    @staticmethod
    def _assess_domain_context_value(field_name: str, _context: Dict) -> Dict[str, Any]:
        """Assess if domain context would add value to field understanding."""
        field_lower = field_name.lower()

        # Domain-specific terms that benefit from context
        domain_terms = {
            'rate': 'Could for example: be interest rate, exchange rate, or risk rate',
            'limit': 'Could for example: be credit limit, transaction limit, or regulatory limit',
            'score': 'Could for example: be credit score, risk score, compliance score, threat score, or vulnerability score',
            'level': 'Could for example: be threat level, access level, severity level, care level, severity level, or access level',
            'status': 'Could be for example: security status, compliance status, threat status, patient status, treatment status, or care status',
            'type': 'Could for example: be threat type, attack type, or security type, patient type, procedure type, or care type',
            'category': 'Could for example: be risk category, threat category, or incident category',
            'code': 'Could be for example: diagnosis code, procedure code, or billing code',
        }

        found_terms = []

        for term, explanation in domain_terms.items():
            if term in field_lower:
                found_terms.append(term)

        if found_terms:
            return {
                'adds_value': True,
                'explanation': f'Domain context clarifies ambiguous terms: {", ".join(found_terms)}',
                'terms': found_terms
            }

        return {
            'adds_value': False,
            'explanation': 'No domain-specific terms needing clarification',
            'terms': []
        }


    def _generate_field_description_attempt_with_value_context(self, field_data: Dict[str, Any],
                                                               context: Dict[str, Any], attempt: int,
                                                               value_assessment: Dict[str, Any]) -> Optional[str]:
        """
        Generate field description with specific guidance based on identified value-add opportunity.
        """
        field_name = field_data.get('name', '')
        field_type = field_data.get('type', '')
        entity_name = context.get('entity_name', context.get('parent_name', ''))
        domain = context.get('domain', 'default')

        # Get domain context
        domain_context = self._get_domain_context({}, [domain])

        # Build prompt based on the specific value-add reason
        reason = value_assessment['reason']
        acronym_expansions = value_assessment.get('acronym_expansions', {})

        if reason == 'acronym_expansion':
            prompt = self._build_acronym_expansion_prompt(field_name, field_type, acronym_expansions, domain_context)
        elif reason == 'technical_translation':
            technical_terms = value_assessment.get('technical_terms', [])
            prompt = self._build_technical_translation_prompt(field_name, field_type, technical_terms, domain_context)
        elif reason == 'domain_context':
            domain_terms = value_assessment.get('domain_terms', [])
            prompt = self._build_domain_context_prompt(field_name, field_type, domain_terms, context, domain_context)
        elif reason == 'ambiguous_name':
            clarity_issues = value_assessment.get('clarity_issues', [])
            prompt = self._build_clarification_prompt(field_name, field_type, clarity_issues, domain_context)
        else:
            # Fallback to standard enhanced prompt
            enhanced_semantics = self._analyze_field_semantics_enhanced(field_name, field_type, entity_name)
            business_context = enhanced_semantics.get('business_intent', 'supports business operations')
            prompt = self._build_enhanced_prompt_with_acronyms(
                field_name, field_type, business_context, domain_context,
                getattr(config, 'field_desc_max_length', 120), acronym_expansions
            )

        # Add attempt-specific guidance
        if attempt == 1:
            prompt += " Previous attempt was too generic. Be more specific about the business meaning."
        elif attempt == 2:
            prompt += " Final attempt. Focus on the core business concept this field represents."

        try:
            # FIX: Use config.field_tokens instead of hardcoded value
            desc = self._make_api_call(prompt, config.field_tokens)
            return desc

        except Exception as e:
            logger.error(f"❌ API ERROR: {e}")
            return None

    @staticmethod
    def _build_clarification_prompt(field_name: str, _field_type: str,
                                    clarity_issues: List[str], domain_context: str) -> str:
        """Build prompt for clarifying unclear field names."""
        issues_text = ", ".join(clarity_issues)

        return f"Clarify unclear field '{field_name}'. Issues: {issues_text}. {domain_context} Explain what business concept this represents clearly and specifically."

    def _generate_field_description_attempt_with_acronyms(self, field_data: Dict[str, Any],
                                                          context: Dict[str, Any], attempt: int,
                                                          acronym_expansions: Dict[str, str]) -> Optional[str]:
        """
        Generate field description with acronym expansions provided to AI upfront.
        """
        field_name = field_data.get('name', '')
        field_type = field_data.get('type', '')
        entity_name = context.get('entity_name', context.get('parent_name', ''))
        domain = context.get('domain', 'default')

        enhanced_semantics = self._analyze_field_semantics_enhanced(
            field_name, field_type, entity_name
        )

        # Get domain context
        domain_context = self._get_domain_context({}, [domain])

        # Build enhanced prompt with acronym expansions
        business_context = enhanced_semantics.get('business_intent', 'supports business operations')
        prompt = self._build_enhanced_prompt_with_acronyms(
            field_name, field_type, business_context, domain_context,
            getattr(config, 'field_desc_max_length', 120), acronym_expansions
        )

        # Add attempt-specific guidance
        if attempt == 1:
            prompt += " Previous attempt was too generic. Focus on specific business or technical value."
            if context.get('rejected_patterns'):
                rejected = context['rejected_patterns']
                if 'Circular description' in str(rejected):
                    prompt += " AVOID generic storage language like 'stores the', 'contains the', 'represents the'."
                if 'redundant entity references' in str(rejected):
                    prompt += " DO NOT mention the entity name or 'the application'."
                if 'No clear business' in str(rejected):
                    prompt += " MUST explain business impact, operational purpose, or technical function."
        elif attempt == 2:
            prompt += " Final attempt. Be very specific about business value. Start with action verb like: enables, controls, manages, governs, determines, validates, configures."

        try:
            # FIX: Use config.field_tokens instead of hardcoded value
            desc = self._make_api_call(prompt, config.field_tokens)
            return desc

        except Exception as e:
            logger.error(f"❌ API ERROR: {e}")
            return None

    @staticmethod
    def _get_quality_assessment(score: int) -> str:
        """Get qualitative assessment based on score."""
        if score >= 80:
            return "High quality - clear business value and specific purpose"
        elif score >= 60:
            return "Acceptable - provides useful context with minor issues"
        elif score >= 40:
            return "Marginal - limited value, some generic language"
        elif score >= 20:
            return "Poor - mostly generic with little business context"
        else:
            return "Rejected - circular, redundant, or meaningless"

    @staticmethod
    def _analyze_field_semantics_enhanced(field_name: str, field_type: str, _entity_name: str) -> Dict[
        str, Any]:
        """Enhanced semantic analysis with business intent detection."""
        name_lower = field_name.lower()

        # Business process patterns
        process_patterns = {
            'approval': {
                'purpose': 'workflow control point',
                'business_focus': 'governs progression through approval stages',
                'value_proposition': 'ensures compliance and authorization'
            },
            'threshold': {
                'purpose': 'decision boundary',
                'business_focus': 'triggers automated actions or alerts',
                'value_proposition': 'enables rule-based automation'
            },
            'priority': {
                'purpose': 'resource allocation driver',
                'business_focus': 'influences processing order and resource assignment',
                'value_proposition': 'optimizes operational efficiency'
            },
            'category': {
                'purpose': 'classification system',
                'business_focus': 'enables grouping and specialized handling',
                'value_proposition': 'supports targeted business strategies'
            }
        }

        # Check for pattern matches
        for pattern, info in process_patterns.items():
            if pattern in name_lower:
                return {
                    'semantic_type': 'process_control',
                    'business_intent': info['purpose'],
                    'operational_value': info['business_focus'],
                    'strategic_value': info['value_proposition']
                }

        # Type-specific analysis
        if 'Array' in field_type:
            return {
                'semantic_type': 'collection',
                'business_intent': 'aggregate related information',
                'operational_value': 'supports complex business relationships',
                'strategic_value': 'enables comprehensive data analysis'
            }

        return {
            'semantic_type': 'data_attribute',
            'business_intent': 'data attribute requiring analysis',
            'operational_value': 'supports operational processes',
            'strategic_value': 'contributes to business intelligence'
        }

    def is_technical_name_sufficient(self, name: str, element_type: str = 'field') -> bool:
        """
        Determine if technical name is clear enough to skip business description.

        Args:
            name: Technical name to evaluate
            element_type: Type of element ('field', 'entity', etc.)

        Returns:
            True if technical name is sufficiently descriptive
        """
        if not name or len(name) < 3:
            return False

        # Clean and analyze name
        clean_name = self._clean_technical_name(name)
        words = self._extract_words_from_name(clean_name)

        # Check clarity indicators
        has_clear_words = len([w for w in words if len(w) > 2 and self._is_english_word(w)]) >= len(words) * 0.7
        has_good_length = 3 <= len(clean_name) <= 50
        not_cryptic = not self._is_cryptic_name(clean_name)
        descriptive_pattern = self._matches_descriptive_pattern(clean_name, element_type)

        is_sufficient = has_clear_words and has_good_length and not_cryptic and descriptive_pattern

        if is_sufficient:
            logger.debug(f"Technical name '{name}' is sufficient - skipping AI description")

        return is_sufficient

    @staticmethod
    def _clean_technical_name(name: str) -> str:
        """Remove technical prefixes/suffixes and normalize."""
        cleaned = re.sub(r'_(id|key|ref|fk|pk)$', '', name.lower())
        cleaned = re.sub(r'^(tbl_|vw_|sp_|fn_)', '', cleaned)
        return cleaned

    @staticmethod
    def _extract_words_from_name(name: str) -> List[str]:
        """Extract individual words from camelCase or snake_case names."""
        if '_' in name:
            return [word for word in name.split('_') if word]
        return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|$)', name)

    @staticmethod
    def _is_english_word(word: str) -> bool:
        """Check if word appears to be English (basic heuristic)."""
        common_words = {
            'user', 'name', 'email', 'phone', 'address', 'date', 'time', 'created', 'updated',
            'status', 'type', 'code', 'number', 'amount', 'total', 'count', 'active', 'deleted',
            'first', 'last', 'middle', 'full', 'start', 'end', 'begin', 'finish', 'order',
            'customer', 'product', 'service', 'account', 'payment', 'invoice', 'transaction',
            'application', 'system', 'server', 'network', 'device', 'resource', 'organization',
            'company', 'department', 'employee', 'manager', 'project', 'task', 'schedule'
        }
        return word.lower() in common_words or len(word) > 3

    @staticmethod
    def _is_cryptic_name(name: str) -> bool:
        """Check if name appears cryptic or abbreviated."""
        vowels = sum(1 for c in name.lower() if c in 'aeiou')
        consonants = sum(1 for c in name.lower() if c.isalpha() and c not in 'aeiou')

        if len(name) > 0:
            vowel_ratio = vowels / len(name)
            return vowel_ratio < 0.2 or consonants > vowels * 3
        return True

    @staticmethod
    def _matches_descriptive_pattern(name: str, element_type: str) -> bool:
        """Check if name follows descriptive patterns."""
        if element_type == 'field':
            good_patterns = [
                r'.*_(date|time|at)',
                r'.*_(name|title|desc)',
                r'.*_(status|state|flag)',
                r'.*_(email|phone|address)',
                r'.*_(amount|total|count|number)'
            ]
            return any(re.match(pattern, name.lower()) for pattern in good_patterns)
        elif element_type == 'entity':
            return len(name) > 4 and not name.lower().endswith(('_tmp', '_temp', '_bak'))
        return True

    @staticmethod
    def _extract_domains_from_context(data: Dict, context: Dict) -> List[str]:
        """Extract detected domains from data and context."""
        domains = []

        # Check for IT/Enterprise management indicators
        name = data.get('name', context.get('name', ''))
        if name:
            name_lower = name.lower()
            if any(indicator in name_lower for indicator in
                   ['application', 'system', 'server', 'network', 'it', 'enterprise']):
                domains.append('it_management')
            elif any(indicator in name_lower for indicator in ['organization', 'company', 'department', 'employee']):
                domains.append('enterprise')

        return domains[:2]

    def generate_field_description(self, field_data: Dict, context: Dict) -> str:
        """
        Generate a description for a field using explicit business context.

        Args:
            field_data: Dictionary containing field information
            context: Context information

        Returns:
            Generated description or empty string if generation fails
        """
        field_name = field_data.get('name')
        if not field_name:
            return ""

        # Check if technical name is sufficient
        if self.is_technical_name_sufficient(field_name, 'field'):
            return ""

        max_len = config.field_desc_max_length
        target_len = config.short_field_target
        parent_name = context.get('parent_name', '')
        # parent_kind = context.get('ancestor_kind', '')
        field_type_formatted = self._format_type(field_data.get('type', field_data.get('outputType')))

        entity_description = context.get('entity_description', '')

        # Get domain context
        detected_domains = self._extract_domains_from_context(field_data, context)
        domain_context = self._get_domain_context(field_data, detected_domains)

        semantic_info = self._extract_field_semantics(field_name, parent_name, entity_description)

        logger.info(f"🎯 FIELD DESCRIPTION: {parent_name}.{field_name}")
        logger.info(f"   Domain: {detected_domains[0] if detected_domains else 'default'}")

        prompt = self._build_field_prompt(semantic_info, field_type_formatted, max_len, domain_context)

        logger.info(f"   Prompt: {prompt}")

        try:
            desc = self._make_api_call(prompt, config.field_tokens)
            logger.info(f"   Raw: '{desc}'")

            desc = clean_description_response(desc)
            desc = refine_ai_description(desc)

            if (len(desc) <= max_len and
                    self._validate_description(desc, set(), "Field", field_name) and
                    len(desc.split()) >= 2):
                final_desc = normalize_description(desc, line_length=config.field_desc_max_length,
                                                   make_token_efficient=True)
                logger.info(f"✅ SUCCESS: '{final_desc}' ({len(final_desc)} chars)")
                return final_desc

            # Retry with concise prompt
            shorter_prompt = self._build_concise_field_prompt(semantic_info, field_type_formatted, target_len,
                                                              domain_context)
            # FIX: Use config-based calculation for shorter tokens
            shorter_tokens = max(config.field_tokens // 3, int(target_len / 8))

            desc_short = self._make_api_call(shorter_prompt, shorter_tokens)

            desc_short = clean_description_response(desc_short)
            desc_short = refine_ai_description(desc_short)

            if (self._validate_description(desc_short, set(), "Field", field_name) and
                    desc_short and len(desc_short.split()) >= 2):
                final_desc_short = normalize_description(desc_short, line_length=config.field_desc_max_length,
                                                         make_token_efficient=True)
                logger.info(f"✅ RETRY SUCCESS: '{final_desc_short}' ({len(final_desc_short)} chars)")
                return final_desc_short

            logger.error(f"❌ FAILED: {parent_name}.{field_name}")
            return ""

        except Exception as e:
            logger.error(f"❌ API ERROR for field '{field_name}': {e}")
            return ""

    @staticmethod
    def _extract_element_semantics(element_name: str, kind: str, entity_description: str) -> Dict[
        str, Any]:
        """Extract business semantics for schema elements using explicit business context."""
        return {
            "name": element_name,
            "kind": kind,
            "entity_description": entity_description
        }

    def _extract_field_semantics(self, field_name: str, entity_name: str, entity_description: str) -> Dict[str, Any]:
        """Extract business meaning using enhanced semantic analysis."""
        if not field_name:
            return {
                "business_context": "data attribute requiring further analysis",
                "entity_description": entity_description
            }

        # Use enhanced semantic analysis
        enhanced_semantics = self._analyze_field_semantics_enhanced(field_name, "", entity_name)

        components = self._split_field_name(field_name)

        # Keep your existing semantic checks but enhance with new analysis
        is_identifier = self._is_identifier_field(components)
        is_reference = self._is_reference_field(components)
        is_status = self._is_status_field(components)
        is_count = self._is_count_field(components)
        is_timestamp = self._is_timestamp_field(components)
        is_flag = self._is_flag_field(components)

        # Use enhanced business context if available, otherwise fall back to existing logic
        if enhanced_semantics.get('business_intent') != 'data attribute requiring analysis':
            business_context = enhanced_semantics['business_intent']
        else:
            business_context = self._build_business_context_from_explicit_info(
                field_name, entity_name, components, '',
                is_identifier, is_reference, is_status, is_count, is_timestamp, is_flag
            )

            # If we still can't build meaningful context, skip generation
            if not business_context:
                return {
                    "business_context": None,  # Signal to skip generation
                    "parent_name": entity_name,
                    "name": field_name,
                    "entity_description": entity_description,
                    "should_skip": True
                }

        return {
            "business_context": business_context,
            "parent_name": entity_name,
            "name": field_name,
            "entity_description": entity_description,
            "enhanced_semantics": enhanced_semantics,  # Add this for richer context
            "is_identifier": is_identifier,
            "is_reference": is_reference,
            "is_status": is_status,
            "is_count": is_count,
            "is_timestamp": is_timestamp,
            "is_flag": is_flag,
            "components": components
        }

    def _build_business_context_from_explicit_info(self, field_name: str, entity_name: str, components: List[str],
                                                   business_role: str,
                                                   is_identifier: bool, is_reference: bool, is_status: bool,
                                                   is_count: bool, is_timestamp: bool, is_flag: bool) -> str:
        """Build business context using explicit use case and entity description."""
        field_lower = field_name.lower()

        if is_flag:
            return self._build_flag_context(field_lower, business_role, entity_name)
        elif is_status:
            return f"current state of this {entity_name}"
        elif is_count:
            return self._build_count_context(field_lower, components, business_role, entity_name)
        elif is_timestamp:
            return self._build_timestamp_context(field_lower, components, business_role, entity_name)
        elif is_identifier and is_reference:
            return f"identifies another entity related to this {entity_name}"
        elif is_identifier:
            return f"unique identifier for this {entity_name}"
        elif is_reference:
            return f"connects this {entity_name} to another entity"
        else:
            context = self._build_data_field_context(field_lower, components, business_role, entity_name)
            # If we can't build meaningful context, return None to skip generation
            return context if context else None

    @staticmethod
    def _is_identifier_field(components: List[str]) -> bool:
        """Check if field represents an identifier."""
        id_patterns = {'id', 'identifier', 'key', 'uid', 'uuid', 'guid', 'pk'}
        return any(comp in id_patterns for comp in components)

    def _is_reference_field(self, components: List[str]) -> bool:
        """Check if field represents a reference to another entity."""
        ref_patterns = {'ref', 'reference', 'fk', 'foreign', 'link'}
        return (any(comp in ref_patterns for comp in components) or
                (self._is_identifier_field(components) and len(components) > 1))

    @staticmethod
    def _is_status_field(components: List[str]) -> bool:
        """Check if field represents status information."""
        status_patterns = {'status', 'state', 'condition', 'phase', 'stage'}
        return any(comp in status_patterns for comp in components)

    @staticmethod
    def _is_count_field(components: List[str]) -> bool:
        """Check if field represents a count or quantity."""
        count_patterns = {'count', 'total', 'num', 'number', 'quantity', 'amount', 'size'}
        return any(comp in count_patterns for comp in components)

    @staticmethod
    def _is_timestamp_field(components: List[str]) -> bool:
        """Check if field represents timestamp information."""
        timestamp_patterns = {'time', 'timestamp', 'date', 'at', 'on', 'when', 'created', 'updated', 'modified'}
        return any(comp in timestamp_patterns for comp in components)

    @staticmethod
    def _is_flag_field(components: List[str]) -> bool:
        """Check if field represents a boolean flag."""
        flag_patterns = {'is', 'has', 'can', 'should', 'will', 'enabled', 'disabled', 'active', 'inactive', 'verified',
                         'approved'}
        return any(comp in flag_patterns for comp in components)

    @staticmethod
    def _format_type(type_str: Any) -> str:
        """Format type information for display."""
        if not type_str or not isinstance(type_str, str):
            return "UnknownType"

        is_nullable = not type_str.endswith('!')
        base_type = type_str.rstrip('!')

        if base_type.startswith('[') and base_type.endswith(']'):
            inner = base_type[1:-1].rstrip('!')
            return f"Array of {inner} ({'nullable' if is_nullable else 'non-nullable'})"

        return f"{base_type} ({'nullable' if is_nullable else 'non-nullable'})"

    @staticmethod
    def _validate_description(description: str, _domain_keywords: Set[str], _kind: str, name: str) -> bool:
        """Validate that a description meets basic quality criteria."""
        if not description or not description.strip():
            return False

        redundant_patterns = [
            f"the {name.lower()}",
            f"this {name.lower()}",
            f"{name.lower()} field",
            "here are some options",
            "this field represents"
        ]

        desc_lower = description.lower()
        for pattern in redundant_patterns:
            if pattern in desc_lower:
                logger.debug(f"Description contains redundant pattern '{pattern}': {description}")

        return True

    @staticmethod
    def _get_domain_context(_entity_data: Dict, _detected_domains: List[str]) -> str:
        """Get domain-specific context for prompt enhancement."""
        # Since we're not using domain prompts anymore, just return the system prompt context
        return config.system_prompt or "Focus on business purpose and data relationships."

    def get_cache_performance(self) -> Optional[Dict[str, Any]]:
        """Get cache performance statistics."""
        if self.cache:
            return self.cache.get_cache_stats()
        return None

    def log_cache_performance(self):
        """Log cache performance statistics."""
        if not self.cache:
            logger.info("📊 Caching disabled")
            return

        stats = self.cache.get_cache_stats()
        logger.info("📊 CACHE PERFORMANCE:")
        logger.info(f"   Hit Rate: {stats['hit_rate']:.1%}")
        logger.info(f"   Exact Hits: {stats['exact_hits']}")
        logger.info(f"   Similarity Hits: {stats['similarity_hits']}")
        logger.info(f"   Cache Size: {stats['cache_size']} descriptions")
        logger.info(f"   API Calls Saved: {stats['api_calls_saved']}")

        if stats['api_calls_saved'] > 0:
            estimated_time_saved = stats['api_calls_saved'] * 2  # Assume 2 seconds per API call
            estimated_cost_saved = stats['api_calls_saved'] * 0.01  # Rough estimate
            logger.info(f"   💰 Estimated savings: ~{estimated_time_saved}s, ~${estimated_cost_saved:.2f}")

    @staticmethod
    def _should_skip_field(field_name: str, _field_data: Dict[str, Any]) -> bool:
        """Determine if a field should be skipped for description generation."""
        field_name_lower = field_name.lower()

        # Check against configured skip patterns
        for pattern in config.skip_field_patterns:
            if re.match(pattern, field_name_lower):
                return True

        return False
