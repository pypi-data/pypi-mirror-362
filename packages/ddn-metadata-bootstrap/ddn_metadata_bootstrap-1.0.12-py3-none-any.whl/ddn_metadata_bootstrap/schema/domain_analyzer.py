#!/usr/bin/env python3

"""
Domain analysis and term extraction for schema elements.
Analyzes schema content to identify domain-specific terms and context.
Enhanced to minimize repetitive language and provide concise domain context.
"""

import logging
import re
from typing import Dict, List, Set, Tuple, Any, Optional

from ..config import config

logger = logging.getLogger(__name__)


class DomainAnalyzer:
    """
    Analyzes schema content to extract domain-specific terms and context.

    Identifies business domain concepts from schema names, field names, and use case
    descriptions to provide concise context for AI-generated descriptions.
    """

    def __init__(self):
        """
        Initialize the domain analyzer.

        Args:

        """

        self.extracted_names: List[str] = []
        self.domain_keywords: Set[str] = set()
        self.detected_domains: Set[str] = set()

    def extract_domain_terms(self, yaml_data: Dict) -> None:
        """
        Extract domain-specific terms from YAML data structure.

        Analyzes YAML structure to find entity names, field names, and other identifiers
        that indicate business domain context.

        Args:
            yaml_data: YAML data structure to analyze
        """
        names = []
        domain_keywords = set()

        def extract_names_recursive(data, names_list):
            """Recursively extract 'name' fields from nested structures."""
            if isinstance(data, dict):
                if 'name' in data:
                    name_value = data['name']
                    if isinstance(name_value, str):
                        names_list.append(name_value)
                    elif isinstance(name_value, dict):
                        if 'name' in name_value:
                            names_list.append(str(name_value['name']))
                        elif 'column' in name_value and isinstance(name_value['column'], dict):
                            if 'name' in name_value['column']:
                                names_list.append(str(name_value['column']['name']))

                for _, value in data.items():
                    extract_names_recursive(value, names_list)
            elif isinstance(data, list):
                for item in data:
                    extract_names_recursive(item, names_list)

        extract_names_recursive(yaml_data, names)
        self.extracted_names.extend(names)

        # Process names to extract domain terms
        for name in names:
            if isinstance(name, str):
                name_parts = self._split_compound_name(name)

                # Add meaningful parts as domain keywords
                for part in name_parts:
                    if len(part) > 3 and part.lower() not in self._get_common_stopwords():
                        domain_keywords.add(part.lower())

        self.domain_keywords.update(domain_keywords)

        logger.debug(f"Extracted {len(domain_keywords)} domain keywords from schema")

    def detect_domains_from_terms(self, terms: List[str]) -> Tuple[Set[str], Set[str]]:
        """
        Detect business domains based on extracted terms.

        Uses configured domain mappings to identify likely business domains.

        Args:
            terms: List of terms to analyze

        Returns:
            Tuple of (detected_domains, matching_keywords)
        """
        detected_domains = set()
        domain_keywords = set()

        if not terms:
            return detected_domains, domain_keywords

        # Convert terms to lowercase for matching
        lower_terms = []
        for t in terms:
            if isinstance(t, str):
                lower_terms.append(t.lower())
            elif isinstance(t, dict):
                if 'name' in t:
                    lower_terms.append(str(t['name']).lower())
            else:
                lower_terms.append(str(t).lower())

        # Check against domain identifiers
        for term in lower_terms:
            for identifier in config.domain_identifiers:
                if identifier.lower() in term:
                    detected_domains.add('identifiers')
                    domain_keywords.add(identifier)

        self.detected_domains.update(detected_domains)
        return detected_domains, domain_keywords

    def extract_domain_context(self, data: Dict) -> Tuple[str, Set[str]]:
        """
        Extract domain context from a schema element.

        Analyzes schema element to determine business domain context and relevant keywords.

        Args:
            data: Schema element data

        Returns:
            Tuple of (context_description, domain_keywords)
        """
        context_parts = []
        domain_keywords = set()
        domains: Optional[set[str]] = None

        # Extract element name and analyze it
        element_name = self._get_element_name(data)
        if element_name:
            name_parts = self._split_compound_name(element_name)

            # Check for domain indicators in name
            domains, keywords = self.detect_domains_from_terms(name_parts)
            domain_keywords.update(keywords)

            if domains:
                primary_domain = list(domains)[0]
                context_parts.append(f"Related to {primary_domain}")

        # Extract field names if this is a structured element
        field_names = self._extract_field_names(data)
        if field_names and domains:
            field_domains, field_keywords = self.detect_domains_from_terms(field_names)
            domain_keywords.update(field_keywords)

            if field_domains:
                field_domain = list(field_domains)[0]
                if field_domain not in [d for d in domains if d in context_parts[0]] if context_parts else True:
                    context_parts.append(f"Contains {field_domain} fields")

        # Check for specific patterns
        patterns = self._identify_patterns(data)
        if patterns:
            context_parts.extend(patterns[:2])  # Limit to top 2 patterns

        # Build concise context description
        if context_parts:
            context_description = ". ".join(context_parts[:3]) + "."  # Limit to 3 parts
        else:
            context_description = "Business data entity."

        # Limit keyword count
        if len(domain_keywords) > config.max_domain_keywords:
            domain_keywords = set(list(domain_keywords)[:config.max_domain_keywords])

        return context_description, domain_keywords

    def get_domain_summary(self) -> Dict[str, Any]:
        """
        Get a summary of domain analysis results.

        Returns:
            Dictionary containing domain analysis summary
        """
        return {
            'extracted_names': len(self.extracted_names),
            'domain_keywords': len(self.domain_keywords),
            'detected_domains': list(self.detected_domains),
        }

    @staticmethod
    def _split_compound_name(name: str) -> List[str]:
        """
        Split compound names (snake_case, camelCase, PascalCase) into parts.

        Args:
            name: Name to split

        Returns:
            List of name parts
        """
        if not name:
            return []

        # Handle snake_case
        if '_' in name:
            parts = name.split('_')
        else:
            # Handle camelCase and PascalCase
            parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|$)', name)

        # Filter out empty parts and single characters
        return [part for part in parts if len(part) > 1]

    def _extract_terms_from_text(self, text: str) -> List[str]:
        """
        Extract meaningful terms from free text.

        Args:
            text: Text to analyze

        Returns:
            List of extracted terms
        """
        words = re.findall(r'\b\w+\b', text.lower())
        stopwords = self._get_common_stopwords()

        return [word for word in words if word not in stopwords and len(word) > 3]

    @staticmethod
    def _get_common_stopwords() -> Set[str]:
        """Get set of common English stopwords to filter out."""
        return {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 'they', 'them',
            'have', 'been', 'were', 'are', 'will', 'can', 'could', 'would',
            'should', 'may', 'might', 'must', 'shall', 'does', 'did', 'has',
            'had', 'was', 'his', 'her', 'its', 'our', 'your', 'their',
            'into', 'over', 'under', 'above', 'below', 'through', 'during',
            'before', 'after', 'between', 'among', 'within'
        }

    @staticmethod
    def _get_element_name(data: Dict) -> Optional[str]:
        """
        Extract the name of a schema element.

        Args:
            data: Schema element data

        Returns:
            Element name or None
        """
        if isinstance(data.get('definition'), dict):
            name = data['definition'].get('name')
            if isinstance(name, str):
                return name
            elif isinstance(name, dict):
                if 'name' in name:
                    return str(name['name'])

        name = data.get('name')
        if isinstance(name, str):
            return name
        elif isinstance(name, dict):
            if 'name' in name:
                return str(name['name'])

        return None

    @staticmethod
    def _extract_field_names(data: Dict) -> List[str]:
        """
        Extract field names from a schema element.

        Args:
            data: Schema element data

        Returns:
            List of field names
        """
        field_names = []

        # Check in definition.fields
        if isinstance(data.get('definition'), dict):
            definition = data['definition']

            # Fields array
            fields = definition.get('fields', [])
            if isinstance(fields, list):
                for field in fields:
                    if isinstance(field, dict) and 'name' in field:
                        name_value = field['name']
                        if isinstance(name_value, str):
                            field_names.append(name_value)
                        elif isinstance(name_value, dict):
                            if 'name' in name_value:
                                field_names.append(str(name_value['name']))
                            elif 'column' in name_value and isinstance(name_value['column'], dict):
                                if 'name' in name_value['column']:
                                    field_names.append(str(name_value['column']['name']))

            # Source properties (for Models)
            source = definition.get('source', {})
            if isinstance(source, dict):
                properties = source.get('properties', [])
                if isinstance(properties, list):
                    for prop in properties:
                        if isinstance(prop, dict) and 'name' in prop:
                            name_value = prop['name']
                            if isinstance(name_value, str):
                                field_names.append(name_value)
                            elif isinstance(name_value, dict):
                                if 'name' in name_value:
                                    field_names.append(str(name_value['name']))

        return field_names

    def _identify_patterns(self, data: Dict) -> List[str]:
        """
        Identify common patterns in schema elements.

        Args:
            data: Schema element data

        Returns:
            List of identified patterns
        """
        patterns = []

        kind = data.get('kind')
        element_name = self._get_element_name(data)
        field_names = self._extract_field_names(data)

        # Entity pattern detection
        if kind == 'ObjectType' or kind == 'Model':
            # Check for audit fields
            audit_fields = {'created_at', 'updated_at', 'created_by', 'updated_by'}
            if any(field.lower() in audit_fields for field in field_names):
                patterns.append("Includes audit tracking")

            # Check for ID patterns
            id_fields = [f for f in field_names if f.lower().endswith('id') or f.lower() == 'id']
            if len(id_fields) > 2:
                patterns.append("Multiple identifiers")

            # Check for status/state fields
            status_fields = {'status', 'state', 'active', 'enabled', 'deleted'}
            if any(field.lower() in status_fields for field in field_names):
                patterns.append("Status management")

        # Naming pattern detection
        if element_name:
            name_lower = element_name.lower()

            # Aggregate patterns
            if any(agg in name_lower for agg in ['total', 'count', 'sum', 'avg', 'max', 'min']):
                patterns.append("Aggregate data")

            # Relationship patterns
            if any(rel in name_lower for rel in ['relationship', 'mapping', 'link', 'join']):
                patterns.append("Relationship entity")

            # Configuration patterns
            if any(config_term in name_lower for config_term in ['config', 'setting', 'preference', 'option']):
                patterns.append("Configuration data")

        return patterns[:3]  # Limit to top 3 patterns

    def analyze_field_semantics(self, field_name: str, _field_type: str = None) -> Dict[str, Any]:
        """
        Analyze the semantic meaning of a field based on its name and type.

        Args:
            field_name: Name of the field
            _field_type: Optional type information

        Returns:
            Dictionary with semantic analysis results
        """
        analysis = {
            'likely_purpose': None,
            'data_category': None,
            'business_domain': None,
            'sensitivity': 'normal'
        }

        if not isinstance(field_name, str):
            return analysis

        field_lower = field_name.lower()

        # Identify purpose patterns
        if any(id_pattern in field_lower for id_pattern in ['id', 'key', 'uuid', 'guid']):
            analysis['likely_purpose'] = 'identifier'
        elif any(time_pattern in field_lower for time_pattern in ['date', 'time', 'created', 'updated', 'modified']):
            analysis['likely_purpose'] = 'temporal'
        elif any(desc_pattern in field_lower for desc_pattern in ['desc', 'description', 'comment', 'note']):
            analysis['likely_purpose'] = 'descriptive'
        elif any(qty_pattern in field_lower for qty_pattern in ['count', 'quantity', 'amount', 'total', 'sum']):
            analysis['likely_purpose'] = 'quantitative'
        elif any(status_pattern in field_lower for status_pattern in ['status', 'state', 'active', 'enabled']):
            analysis['likely_purpose'] = 'status'

        # Identify data categories
        if any(contact_pattern in field_lower for contact_pattern in ['email', 'phone', 'address', 'contact']):
            analysis['data_category'] = 'contact_info'
            analysis['sensitivity'] = 'sensitive'
        elif any(financial_pattern in field_lower for financial_pattern in
                 ['price', 'cost', 'amount', 'salary', 'payment']):
            analysis['data_category'] = 'financial'
        elif any(personal_pattern in field_lower for personal_pattern in ['name', 'age', 'birth', 'ssn', 'passport']):
            analysis['data_category'] = 'personal'
            analysis['sensitivity'] = 'sensitive'

        # Check domain mappings
        domains, _ = self.detect_domains_from_terms(field_name.split('_'))
        if domains:
            analysis['business_domain'] = list(domains)[0]

        return analysis


def create_domain_analyzer() -> DomainAnalyzer:
    """
    Create a DomainAnalyzer instance.

    Args:


    Returns:
        Configured DomainAnalyzer instance
    """
    return DomainAnalyzer()
