#!/usr/bin/env python3

"""
YAML document structure enhancement for adding AI-generated descriptions.
Handles the traversal and enhancement of YAML/HML document structures.
Enhanced to evaluate technical name quality and minimize redundant descriptions.
"""

import logging
from typing import Dict, List, Any, Optional

from ..relationships import RelationshipDetector
from ..ai.description_generator import DescriptionGenerator
from ..config import config
from ..schema.field_analyzer import FieldAnalyzer

logger = logging.getLogger(__name__)


class DocumentEnhancer:
    """
    Enhances YAML document structures by adding AI-generated descriptions.

    Traverses YAML/HML document structures, identifies elements that can have descriptions,
    evaluates technical name quality, generates appropriate descriptions using AI, and
    integrates relationship information into descriptions.
    """

    def __init__(self, description_generator: DescriptionGenerator):
        """
        Initialize the document enhancer.

        Args:
            description_generator: AI description generator instance
        """
        self.description_generator = description_generator
        self.field_analyzer = FieldAnalyzer()

    def enhance_yaml_structure(self, data: Any, parent_path: str = "",
                               parent_info: Optional[Dict] = None,
                               dict_key: Optional[str] = None) -> Any:
        """
        Enhance a YAML structure by adding descriptions to eligible elements.
        In relationships-only mode, skips all field processing entirely.
        OPTIMIZED: Hash-based lookups for kind checking.
        """
        if parent_info is None:
            parent_info = {}

        # DEBUG: Log the mode on first call
        if parent_path == "":
            if config.relationships_only:
                # logger.info(f"🔧 PROCESSING MODE: relationships_only = {config.relationships_only}")
                # logger.info("   SKIPPING ALL FIELD PROCESSING - RELATIONSHIPS ONLY")
                pass

        # OPTIMIZED: Use hash-based excluded kinds checking
        excluded_kinds_set = getattr(config, '_excluded_kinds_set', None)
        if excluded_kinds_set is None:
            excluded_kinds_set = set(getattr(config, 'excluded_kinds', []))
            setattr(config, '_excluded_kinds_set', excluded_kinds_set)

        # Skip excluded kinds entirely
        if parent_info.get('kind') in excluded_kinds_set:
            return data

        # Skip if current element is excluded
        if isinstance(data, dict) and data.get('kind') in excluded_kinds_set:
            return data

        if isinstance(data, dict):
            return self._enhance_dict_structure(data, parent_path, parent_info, dict_key)
        elif isinstance(data, list):
            return self._enhance_list_structure(data, parent_path, parent_info, dict_key)
        else:
            return data

    def _enhance_dict_structure(self, data: Dict, parent_path: str,
                                parent_info: Dict, dict_key: Optional[str]) -> Dict:
        """Enhance a dictionary structure.
        OPTIMIZED: Hash-based lookups for OpenDD kinds."""
        current_kind = data.get('kind')
        current_name = data.get('definition', {}).get('name', data.get('name', ''))

        # OPTIMIZED: Use hash-based OpenDD kinds checking
        opendd_kinds_set = getattr(config, '_opendd_kinds_set', None)
        if opendd_kinds_set is None:
            opendd_kinds_set = set(getattr(config, 'opendd_kinds', []))
            setattr(config, '_opendd_kinds_set', opendd_kinds_set)

        # Build current path segment
        if current_kind in opendd_kinds_set:
            current_path_segment = current_name if current_name else current_kind
        elif dict_key:
            current_path_segment = dict_key
        else:
            current_path_segment = current_name if current_name else "dict_node"

        current_description = self._get_current_description(data)

        # Build the current path
        current_path = f"{parent_path}/{current_path_segment}".strip('/') if parent_path else current_path_segment

        # Determine effective kind and ancestor kind
        ancestor_kind = current_kind if current_kind in opendd_kinds_set else parent_info.get('ancestor_kind')

        # Build current element context
        current_element_context = {
            'name': current_name,
            'description': current_description,
            'kind': current_kind,
            'type': data.get('type', data.get('outputType')),
            'parent_name': parent_info.get('name'),
            'parent_kind': parent_info.get('kind'),
            'ancestor_kind': ancestor_kind,
            'path': current_path,
            'parent_path': parent_path,
            'entity_name': parent_info.get('name', current_name),
            'domain': 'default'
        }

        # Handle OpenDD kinds specially
        if current_kind in opendd_kinds_set:
            return self._enhance_opendd_kind(data.copy(), current_element_context)

        # ROOT-LEVEL FIX: Skip field-like processing entirely in relationships-only mode
        is_field_like = self._is_field_like_element(data, current_kind)
        if is_field_like and config.relationships_only:
            logger.debug(f"⏭️ SKIPPING field-like element '{current_name}' - relationships-only mode")
            # Return the data unchanged, but still process nested structures
            enhanced_dict = {}
            for key, value in data.items():
                enhanced_dict[key] = self.enhance_yaml_structure(
                    value, current_path, current_element_context, key
                )
            return enhanced_dict

        # Handle field-like objects (only if not in relationships-only mode)
        if is_field_like:
            return self._enhance_field_like_element(data.copy(), current_element_context)

        # Handle regular dictionaries
        enhanced_dict = {}
        for key, value in data.items():
            enhanced_dict[key] = self.enhance_yaml_structure(
                value, current_path, current_element_context, key
            )

        return enhanced_dict

    def _enhance_opendd_kind(self, data_copy: Dict, context: Dict) -> Dict:
        """Enhance an OpenDD kind element.
        OPTIMIZED: Hash-based lookups for OpenDD kinds."""
        kind = context.get('kind')

        # OPTIMIZED: Use cached OpenDD kinds set
        opendd_kinds_set = getattr(config, '_opendd_kinds_set', None)
        if opendd_kinds_set is None:
            opendd_kinds_set = set(getattr(config, 'opendd_kinds', []))
            setattr(config, '_opendd_kinds_set', opendd_kinds_set)

        # Ensure definition structure exists for most OpenDD kinds
        if ('definition' not in data_copy and
                kind not in ['Subgraph', 'Supergraph', 'Role'] and
                kind in opendd_kinds_set):
            data_copy['definition'] = {}

        # Move description to definition if needed
        if ('description' in data_copy and
                isinstance(data_copy.get('definition'), dict) and
                'description' not in data_copy['definition']):
            data_copy['definition']['description'] = data_copy.pop('description')

        # Generate description ONLY if not in relationships-only mode
        if (not config.relationships_only and self.should_generate_description(data_copy, context) and
                self.can_have_description(data_copy, context)):

            description_text = self.description_generator.generate_kind_description(data_copy, context)
            if description_text:
                # Add marker to signal that relationships should be added in second pass
                description_with_marker = f"{description_text}\n{config.relationship_marker}"
                self._set_description(data_copy, description_with_marker)

        # Process other keys recursively
        for key, value in list(data_copy.items()):
            if key not in ['kind', 'version', 'name', 'description']:
                data_copy[key] = self.enhance_yaml_structure(
                    value, context['path'], context, key
                )

        return data_copy

    def _process_dict_element_relationships(self, element_data: Dict,
                                            relationship_map: Dict[str, Any],
                                            subgraph: Optional[str],
                                            _current_path_str: str) -> Dict:
        """Process a dictionary element for relationship information.
        OPTIMIZED: Hash-based lookups for excluded kinds."""
        element_kind = element_data.get('kind')

        # OPTIMIZED: Use cached excluded kinds set
        excluded_kinds_set = getattr(config, '_excluded_kinds_set', None)
        if excluded_kinds_set is None:
            excluded_kinds_set = set(getattr(config, 'excluded_kinds', []))
            setattr(config, '_excluded_kinds_set', excluded_kinds_set)

        # Skip excluded kinds entirely
        if element_kind and element_kind in excluded_kinds_set:
            return element_data

        element_name = element_data.get('definition', {}).get('name', element_data.get('name'))

        # Check if this element has a description with marker
        current_description = self._get_current_description(element_data)

        # Ensure current_description is a string before calling replace
        if not isinstance(current_description, str):
            current_description = ""

        has_marker = config.relationship_marker in current_description if current_description else False
        cleaned_description = (current_description.replace(f"\n{config.relationship_marker}", "")
                               .replace(config.relationship_marker, "") if current_description else "")

        final_description_content = cleaned_description

        # Add relationships if this is an OpenDD kind with marker and we have relationships
        if element_kind and element_name and has_marker:
            from ..relationships.mapper import RelationshipMapper
            relationship_mapper = RelationshipMapper(RelationshipDetector())

            entity_relationships = relationship_mapper.get_entity_relationships(
                element_name, element_kind, subgraph, relationship_map
            )

            if entity_relationships:
                current_qnk = (f"{subgraph}/{element_kind}/{element_name}"
                               if subgraph else f"{element_kind}/{element_name}")
                relationship_text = relationship_mapper.format_relationships_for_prompt(
                    entity_relationships, relationship_map, current_qnk
                )

                if relationship_text and relationship_text.strip():
                    separator = "\n\n" if final_description_content.strip() else ""
                    final_description_content += f"{separator}Key Relationships:\n{relationship_text}"

        # Update the element with final description (only if we have meaningful content)
        self._set_description(element_data, final_description_content)

        return element_data

    def should_generate_description(self, data: Dict, context: Dict) -> bool:
        """
        Enhanced logic to determine if description should be generated.

        Considers both existing description status and technical name quality.

        Args:
            data: Element data
            context: Element context

        Returns:
            True if description should be generated
        """
        existing_description = self._get_current_description(data)

        # Always generate if explicitly marked for regeneration
        if existing_description and existing_description.strip().startswith('!'):
            return True

        # Don't generate if description already exists
        if existing_description and existing_description.strip():
            return False

        # Check if technical name is sufficient
        element_name = context.get('name') or data.get('name')
        element_kind = context.get('kind') or data.get('kind')

        if element_name:
            # For field elements
            if not element_kind and ('type' in data or 'outputType' in data):
                if self.field_analyzer.is_technical_name_clear(element_name):
                    logger.debug(f"Skipping field '{element_name}' - technical name is clear")
                    return False

            # For entity elements
            elif element_kind in config.opendd_kinds:
                if self.description_generator.is_technical_name_sufficient(element_name, 'entity'):
                    logger.debug(f"Skipping {element_kind} '{element_name}' - technical name is sufficient")
                    return False

        return True

    def _enhance_field_like_element(self, field_copy: Dict, context: Dict) -> Dict:
        """Enhance a field-like element with quality assessment."""
        # Generate description ONLY if not in relationships-only mode
        # REMOVED: and self.should_generate_description(field_copy, context) ← This method doesn't exist!
        if (not config.relationships_only and
                self.can_have_description(field_copy, context)):

            # The quality check is already built into _generate_field_description
            description = field_copy.get('description')
            if not description:
                description = self._generate_field_description(field_copy, context)

            if description:
                # Add marker to signal that relationships should be added in second pass
                field_copy['description'] = f"{description}\n{config.relationship_marker}"
                logger.info(f"✅ Added description to field '{field_copy.get('name', 'unknown')}'")
            else:
                logger.info(f"⏭️  Skipped field '{field_copy.get('name', 'unknown')}' - quality assessment failed")

        # Process other field properties recursively
        enhanced_dict = {}
        for key, value in field_copy.items():
            if key != 'description':
                enhanced_dict[key] = self.enhance_yaml_structure(
                    value, context['path'], context, key
                )
            else:
                enhanced_dict[key] = field_copy[key]

        return enhanced_dict

    def _generate_field_description(self, field_data: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """
        Generate description for a field using quality assessment.
        Returns None if no quality description can be generated.
        """
        logger.info(f"FIELD NAME: {field_data.get('name', 'unknown')}")
        logger.info(f"   Quality assessment enabled: {config.enable_quality_assessment}")

        if config.enable_quality_assessment:
            # Use the quality-checked method
            return self.description_generator.generate_field_description_with_quality_check(field_data, context)
        else:
            # Fall back to original method
            return self.description_generator.generate_field_description(field_data, context)

    @staticmethod
    def _should_generate_field_description(field: Dict[str, Any]) -> bool:
        """Check if we should generate a description for this field."""
        # Skip if field already has a description
        if field.get('description'):
            return False

        # Skip if field name is not suitable for description
        field_name = field.get('name', '')
        if not field_name or len(field_name) <= 1:
            return False

        return True

    def enhance_with_relationships(self, documents: List[Any],
                                   relationship_map: Dict[str, Any],
                                   subgraph: Optional[str] = None) -> List[Any]:
        """
        Enhance documents by adding relationship information to descriptions.

        Args:
            documents: List of YAML documents to enhance
            relationship_map: Comprehensive relationship map
            subgraph: Optional subgraph context

        Returns:
            List of enhanced documents with relationship information
        """
        enhanced_documents = []

        for doc in documents:
            if doc is None:
                enhanced_documents.append(None)
                continue

            enhanced_doc = self._process_document_for_relationships(
                doc, relationship_map, subgraph
            )
            enhanced_documents.append(enhanced_doc)

        return enhanced_documents

    def can_have_description(self, data: Dict, context: Optional[Dict] = None) -> bool:
        """
        Check if a schema element can have a description.

        Args:
            data: Schema element data
            context: Optional context information

        Returns:
            True if element can have a description
        """
        return self.field_analyzer.can_have_description(data, context)

    def _enhance_list_structure(self, data: List, parent_path: str,
                                parent_info: Dict, dict_key: Optional[str]) -> List:
        """Enhance a list structure."""
        # Incorporate dict_key if provided
        if dict_key:
            list_path = f"{parent_path}/{dict_key}".strip('/')
        else:
            list_path = parent_path

        enhanced_list = []
        for i, item in enumerate(data):
            item_path = f"{list_path}[{i}]"
            enhanced_item = self.enhance_yaml_structure(item, item_path, parent_info, None)
            enhanced_list.append(enhanced_item)

        return enhanced_list

    def _process_document_for_relationships(self, document: Any,
                                            relationship_map: Dict[str, Any],
                                            subgraph: Optional[str]) -> Any:
        """Process a document to add relationship information to descriptions."""

        def process_element(element_data, current_path_str=""):
            if isinstance(element_data, dict):
                element_data = self._process_dict_element_relationships(
                    element_data, relationship_map, subgraph, current_path_str
                )

                # Recursively process nested elements
                element_name = element_data.get('definition', {}).get('name', element_data.get('name'))
                element_kind = element_data.get('kind')
                path_segment = element_name if element_name else element_kind if element_kind else "item"
                new_path = f"{current_path_str}/{path_segment}".strip('/')

                for key, value in list(element_data.items()):
                    if key == 'description' and (isinstance(element_data.get('definition'), dict) or element_kind):
                        continue  # Skip description as it's already processed
                    element_data[key] = process_element(value, new_path)

            elif isinstance(element_data, list):
                element_data = [process_element(item, f"{current_path_str}[{i}]")
                                for i, item in enumerate(element_data)]

            return element_data

        return process_element(document)

    @staticmethod
    def _is_field_like_element(data: Dict, element_kind: Optional[str]) -> bool:
        """Check if element is field-like (has name and type but no kind)."""
        return (
                'name' in data and
                ('type' in data or 'outputType' in data) and
                not element_kind
        )

    @staticmethod
    def _get_current_description(data: Dict) -> str:
        """Get the current description from various possible locations."""
        if isinstance(data.get('definition'), dict):
            return data['definition'].get('description', "")
        elif 'description' in data:
            return data.get('description', "")
        return ""

    @staticmethod
    def _set_description(data: Dict, description: str) -> None:
        """Set description in the appropriate location."""
        # Don't set empty or whitespace-only descriptions
        if not description or not description.strip():
            return

        if isinstance(data.get('definition'), dict):
            data['definition']['description'] = description
        elif 'description' in data or description:
            data['description'] = description

    def get_enhancement_statistics(self, original_data: Any, enhanced_data: Any) -> Dict[str, Any]:
        """
        Get statistics about the enhancement process.

        Args:
            original_data: Original YAML data
            enhanced_data: Enhanced YAML data

        Returns:
            Dictionary with enhancement statistics
        """
        stats = {
            'elements_processed': 0,
            'descriptions_added': 0,
            'descriptions_skipped_clear_names': 0,
            'descriptions_skipped_existing': 0,
            'field_descriptions': 0,
            'kind_descriptions': 0,
            'elements_with_markers': 0
        }

        def count_elements(data, is_enhanced=False, path=""):
            if isinstance(data, dict):
                stats['elements_processed'] += 1

                element_name = data.get('definition', {}).get('name', data.get('name'))
                element_kind = data.get('kind')

                # Check for descriptions
                description = self._get_current_description(data)
                if description:
                    if is_enhanced:
                        if config.relationship_marker in description:
                            stats['elements_with_markers'] += 1

                        # Determine if this is a field or kind description
                        if element_kind:
                            stats['kind_descriptions'] += 1
                        elif 'name' in data and ('type' in data or 'outputType' in data):
                            stats['field_descriptions'] += 1

                # Track skipped descriptions during enhancement
                if is_enhanced and not description and element_name:
                    # Check if skipped due to clear name
                    if not element_kind and ('type' in data or 'outputType' in data):
                        if self.field_analyzer.is_technical_name_clear(element_name):
                            stats['descriptions_skipped_clear_names'] += 1
                    elif element_kind in config.opendd_kinds:
                        if self.description_generator.is_technical_name_sufficient(element_name, 'entity'):
                            stats['descriptions_skipped_clear_names'] += 1

                # Recurse into nested structures
                for key, value in data.items():
                    count_elements(value, is_enhanced, f"{path}/{key}" if path else key)

            elif isinstance(data, list):
                for i, item in enumerate(data):
                    count_elements(item, is_enhanced, f"{path}[{i}]" if path else f"[{i}]")

        # Count original elements
        original_descriptions = 0
        if original_data:
            count_elements(original_data, False)
            original_descriptions = stats['kind_descriptions'] + stats['field_descriptions']

        # Reset counters for enhanced count
        stats['kind_descriptions'] = 0
        stats['field_descriptions'] = 0

        # Count enhanced elements
        if enhanced_data:
            count_elements(enhanced_data, True)

        enhanced_descriptions = stats['kind_descriptions'] + stats['field_descriptions']

        # Calculate final statistics
        stats['descriptions_added'] = max(0, enhanced_descriptions - original_descriptions)
        stats['descriptions_skipped_existing'] = max(0, original_descriptions)

        return stats


def create_document_enhancer(description_generator: DescriptionGenerator) -> DocumentEnhancer:
    """
    Create a DocumentEnhancer instance.

    Args:
        description_generator: AI description generator instance

    Returns:
        Configured DocumentEnhancer instance
    """
    return DocumentEnhancer(description_generator)
