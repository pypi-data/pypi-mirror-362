import hashlib
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Any

from ddn_metadata_bootstrap import config

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
