#!/usr/bin/env python3

"""
Schema metadata collection for analyzing YAML/HML document structures.
Orchestrates the collection of comprehensive schema information for processing.
"""

import logging
import traceback
import re
from typing import Dict, List, Any, Optional

from .domain_analyzer import DomainAnalyzer
from .field_analyzer import FieldAnalyzer
from ..config import config

logger = logging.getLogger(__name__)


class MetadataCollector:
    """
    Collects and organizes metadata from schema documents.

    This class orchestrates the analysis of YAML/HML documents to extract
    comprehensive metadata about entities, fields, relationships, and
    domain context for use in description generation and relationship mapping.
    """

    def __init__(self):
        """Initialize the metadata collector with analyzer components."""
        self.field_analyzer = FieldAnalyzer()
        self.domain_analyzer = DomainAnalyzer()

    def collect_schema_metadata(self, data: Any, metadata: Dict,
                                subgraph: Optional[str] = None,
                                parent_path: str = "") -> None:
        """
        Collect schema metadata from a data structure recursively.

        Args:
            data: YAML data structure to analyze
            metadata: Metadata dictionary to populate
            subgraph: Optional subgraph name
            parent_path: Current path in the data structure
        """
        try:
            if isinstance(data, dict):
                self._collect_from_dict(data, metadata, subgraph, parent_path)
            elif isinstance(data, list):
                self._collect_from_list(data, metadata, subgraph, parent_path)
        except Exception as e:
            logger.error(f"Error in collect_schema_metadata at {parent_path} for {type(data)}: {e}")
            logger.debug(f"Full traceback: {traceback.format_exc()}")

    def update_metadata_with_descriptions(self, data: Dict, metadata: Dict,
                                          parent_path: str = "") -> None:
        """
        Update metadata with description information from enhanced documents.

        Args:
            data: Enhanced document data
            metadata: Metadata dictionary to update
            parent_path: Current path in the data structure
        """
        if isinstance(data, dict):
            self._update_descriptions_from_dict(data, metadata, parent_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    self.update_metadata_with_descriptions(item, metadata, f"{parent_path}[{i}]")

    def resolve_command_fields(self, metadata: Dict) -> None:
        """
        Resolve Command fields by copying from referenced ObjectTypes.

        Commands reference ObjectTypes via their outputType. This method resolves
        those references and copies the appropriate fields to the Command entities
        so they can participate in relationship detection.

        Args:
            metadata: Metadata dictionary containing all collected entities
        """
        entities = metadata.get('entities', [])

        # Build a lookup map of ObjectTypes by name within the same subgraph/file
        object_types_by_name = {}
        # current_subgraph = metadata.get('subgraph')
        # current_file = metadata.get('file_path')

        for entity in entities:
            if entity.get('kind') == 'ObjectType':
                entity_name = entity.get('name')
                entity_subgraph = entity.get('subgraph')
                entity_file = entity.get('file_path')

                # Create lookup key that includes context for proper matching
                lookup_key = f"{entity_subgraph or 'None'}/{entity_file or 'None'}/{entity_name}"
                object_types_by_name[entity_name] = entity
                object_types_by_name[lookup_key] = entity

        # Resolve Command fields
        commands_resolved = 0
        for entity in entities:
            if entity.get('kind') == 'Command':
                current_fields = entity.get('fields', [])

                # Only resolve if Command has no fields currently
                if not current_fields:
                    referenced_type = self._parse_command_output_type(entity)

                    if referenced_type:
                        # Try to find the referenced ObjectType
                        source_entity = None

                        # First try exact name match within same context
                        entity_subgraph = entity.get('subgraph')
                        entity_file = entity.get('file_path')
                        context_key = f"{entity_subgraph or 'None'}/{entity_file or 'None'}/{referenced_type}"

                        if context_key in object_types_by_name:
                            source_entity = object_types_by_name[context_key]
                        elif referenced_type in object_types_by_name:
                            source_entity = object_types_by_name[referenced_type]

                        if source_entity:
                            # Copy fields from the referenced ObjectType
                            source_fields = source_entity.get('fields', [])
                            if source_fields:
                                entity['fields'] = [field.copy() for field in source_fields]
                                entity['referenced_object_type'] = referenced_type
                                entity['field_source'] = 'resolved_from_object_type'
                                commands_resolved += 1

                                logger.debug(f"Resolved {len(source_fields)} fields for Command {entity.get('name')} "
                                             f"from ObjectType {referenced_type}")
                            else:
                                logger.warning(
                                    f"Referenced ObjectType {referenced_type} has no fields for Command {entity.get('name')}")
                        else:
                            logger.warning(
                                f"Could not find referenced ObjectType '{referenced_type}' for Command {entity.get('name')}")

                            # Debug: List available ObjectTypes
                            available_types = [name for name in object_types_by_name.keys() if '/' not in name]
                            logger.debug(f"Available ObjectTypes: {available_types}")
                else:
                    logger.debug(
                        f"Command {entity.get('name')} already has {len(current_fields)} fields - skipping resolution")

        logger.debug(f"Resolved fields for {commands_resolved} Commands from their referenced ObjectTypes")

    def _parse_command_output_type(self, command_entity: Dict) -> Optional[str]:
        """
        Parse Command outputType to extract referenced ObjectType name.

        Handles various GraphQL type notations:
        - '[gcp_vm_configurations!]!' -> 'gcp_vm_configurations'
        - 'gcp_vm_configurations!' -> 'gcp_vm_configurations'
        - 'gcp_vm_configurations' -> 'gcp_vm_configurations'

        Args:
            command_entity: Command entity dictionary

        Returns:
            Referenced ObjectType name or None
        """
        # First try to get outputType from the entity definition
        output_type = None

        # Look in various possible locations for outputType
        if 'definition' in command_entity:
            definition = command_entity['definition']
            if isinstance(definition, dict):
                output_type = definition.get('outputType')

        # Fallback: check if it's stored directly
        if not output_type:
            output_type = command_entity.get('outputType')

        if not output_type or not isinstance(output_type, str):
            logger.debug(f"No outputType found for Command {command_entity.get('name')}")
            return None

        # Parse the GraphQL type notation
        parsed_type = self.parse_graphql_output_type(output_type)

        logger.debug(f"Command {command_entity.get('name')} outputType '{output_type}' -> ObjectType '{parsed_type}'")
        return parsed_type

    @staticmethod
    def parse_graphql_output_type(output_type: str) -> Optional[str]:
        """
        Parse GraphQL output type notation to extract base ObjectType name.

        Examples:
        - '[gcp_vm_configurations!]!' -> 'gcp_vm_configurations'
        - 'UserProfile!' -> 'UserProfile'
        - '[String]' -> 'String'
        - 'Int' -> 'Int'

        Args:
            output_type: GraphQL type string

        Returns:
            Base ObjectType name or None
        """
        if not output_type or not isinstance(output_type, str):
            return None

        # Remove whitespace
        cleaned = output_type.strip()

        # Handle array notation: [Type] or [Type!]
        if cleaned.startswith('[') and ']' in cleaned:
            # Find the matching closing bracket
            bracket_content = cleaned[1:cleaned.find(']')]
            cleaned = bracket_content

        # Remove non-null indicators (!)
        cleaned = cleaned.rstrip('!')

        # Final validation - should be a valid identifier
        if cleaned and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', cleaned):
            return cleaned

        logger.warning(f"Could not parse GraphQL output type: '{output_type}' -> '{cleaned}'")
        return None

    def extract_entity_summary(self, entities: List[Dict]) -> Dict[str, Any]:
        """
        Extract summary information from collected entities.

        Args:
            entities: List of entity metadata dictionaries

        Returns:
            Summary dictionary with statistics and insights
        """
        summary = {
            'total_entities': len(entities),
            'by_kind': {},
            'by_subgraph': {},
            'field_patterns': {},
            'relationship_candidates': [],
            'domain_insights': {},
            'command_resolution_stats': {
                'total_commands': 0,
                'commands_with_fields': 0,
                'commands_resolved': 0
            }
        }

        all_field_names = []

        for entity in entities:
            # Count by kind
            kind = entity.get('kind', 'Unknown')
            summary['by_kind'][kind] = summary['by_kind'].get(kind, 0) + 1

            # Count by subgraph
            subgraph = entity.get('subgraph', 'None')
            summary['by_subgraph'][subgraph] = summary['by_subgraph'].get(subgraph, 0) + 1

            # Track Command resolution statistics
            if kind == 'Command':
                summary['command_resolution_stats']['total_commands'] += 1
                fields = entity.get('fields', [])
                if fields:
                    summary['command_resolution_stats']['commands_with_fields'] += 1
                    if entity.get('field_source') == 'resolved_from_object_type':
                        summary['command_resolution_stats']['commands_resolved'] += 1

            # Collect field names for pattern analysis
            fields = entity.get('fields', [])
            entity_field_names = [f.get('name') for f in fields if f.get('name')]
            all_field_names.extend(entity_field_names)

            # Analyze relationships
            potential_fks = entity.get('potential_foreign_keys', [])
            for fk in potential_fks:
                summary['relationship_candidates'].append({
                    'source_entity': entity.get('name'),
                    'source_field': fk,
                    'entity_kind': kind,
                    'subgraph': subgraph
                })

        # Analyze field patterns across all entities
        if all_field_names:
            summary['field_patterns'] = self.field_analyzer.identify_field_patterns(all_field_names)

        # Domain analysis
        domains, keywords = self.domain_analyzer.detect_domains_from_terms(all_field_names)
        summary['domain_insights'] = {
            'detected_domains': list(domains),
            'domain_keywords': list(keywords)[:20],  # Limit to top 20
            'total_unique_fields': len(set(all_field_names))
        }

        return summary

    def _collect_from_dict(self, data: Dict, metadata: Dict,
                           subgraph: Optional[str], parent_path: str) -> None:
        """Collect metadata from a dictionary structure."""
        current_name = data.get('definition', {}).get('name', data.get('name', ''))
        current_segment = current_name if current_name else data.get('kind', 'dict_node')

        if 'kind' in data:
            entity_kind = data.get('kind')

            # Skip excluded kinds
            if entity_kind in config.excluded_kinds:
                return

            # Extract entity information
            entity_name = data.get('definition', {}).get('name', data.get('name'))
            if not entity_name and entity_kind in config.opendd_kinds:
                entity_name = f"Unnamed{entity_kind}_{len(metadata.get('entities', []))}"
                logger.warning(f"Unnamed {entity_kind} at {parent_path}/{current_segment}, using: {entity_name}")

            if entity_name and entity_kind:
                entity_info = self._extract_entity_info(data, entity_name, entity_kind,
                                                        subgraph, parent_path, current_segment, metadata)

                # Check for duplicates before adding
                if not self._is_duplicate_entity(entity_info, metadata.get('entities', [])):
                    metadata.setdefault('entities', []).append(entity_info)

        # Recurse into nested structures
        new_parent_path = f"{parent_path}/{current_segment}".strip('/')
        for key, value in data.items():
            # Avoid infinite recursion in deeply nested definitions
            if key == 'definition' and parent_path.count('/definition') > 2:
                continue
            self.collect_schema_metadata(value, metadata, subgraph, new_parent_path)

    def _collect_from_list(self, data: List, metadata: Dict,
                           subgraph: Optional[str], parent_path: str) -> None:
        """Collect metadata from a list structure."""
        for i, item in enumerate(data):
            self.collect_schema_metadata(item, metadata, subgraph, f"{parent_path}[{i}]")

    def _extract_entity_info(self, data: Dict, entity_name: str, entity_kind: str,
                             subgraph: Optional[str], parent_path: str,
                             current_segment: str, metadata: Dict) -> Dict[str, Any]:
        """Extract comprehensive information about an entity."""
        # Collect fields
        fields_collected = []

        if 'definition' in data and isinstance(data['definition'], dict):
            definition = data['definition']

            # Extract fields from definition.fields
            if 'fields' in definition and isinstance(definition['fields'], list):
                for field in definition['fields']:
                    if isinstance(field, dict) and 'name' in field:
                        field_info = self._extract_field_info(field)
                        fields_collected.append(field_info)

            # Log Model-ObjectType relationship
            if entity_kind == "Model" and 'objectType' in definition:
                logger.debug(f"Model '{entity_name}' refers to objectType '{definition['objectType']}'.")

            # Extract fields from Model source properties
            if ('source' in definition and isinstance(definition['source'], dict) and
                    'properties' in definition['source'] and
                    isinstance(definition['source']['properties'], list)):

                for prop in definition['source']['properties']:
                    if isinstance(prop, dict) and 'name' in prop:
                        prop_info = self._extract_field_info(prop)
                        # Avoid duplicates
                        if not any(f['name'] == prop_info['name'] for f in fields_collected):
                            fields_collected.append(prop_info)

        # Fallback: collect related fields if no direct fields found
        if not fields_collected:
            fields_collected.extend(self._collect_related_fields(data))

        # Analyze keys - ensure safe string operations
        key_analysis = self.field_analyzer.analyze_for_keys(data)

        # Build entity information
        entity_info = {
            'name': entity_name,
            'kind': entity_kind,
            'path': f"{parent_path}/{current_segment}".strip('/'),
            'subgraph': subgraph,
            'file_path': metadata.get('file_path'),
            'fields': fields_collected,
            'primary_keys': key_analysis.get('potential_primary_keys', []),
            'potential_foreign_keys': key_analysis.get('potential_foreign_keys', []),
            'field_count': len(fields_collected),
            'permissions_info': self._collect_permissions_info(data),
            'model_info': self._collect_model_info(data),
            'command_info': self._collect_command_info(data) if entity_kind == 'Command' else {}
        }

        # Add domain context - ensure safe operations
        try:
            domain_context, domain_keywords = self.domain_analyzer.extract_domain_context(data)
            entity_info.update({
                'domain_context': domain_context,
                'domain_keywords': list(domain_keywords) if domain_keywords else []
            })
        except Exception as e:
            logger.warning(f"Failed to extract domain context for entity {entity_name}: {e}")
            entity_info.update({
                'domain_context': {},
                'domain_keywords': []
            })

        return entity_info

    def _extract_field_info(self, field: Dict) -> Dict[str, Any]:
        """Extract comprehensive information about a field."""
        field_info = {
            'name': field.get('name', ''),
            'type': field.get('type', ''),
            'description': field.get('description', ''),
            'type_info': {},
            'semantic_analysis': None
        }

        # Safely get field type info
        try:
            field_info['type_info'] = self.field_analyzer.get_field_type_info(field)
        except Exception as e:
            logger.warning(f"Failed to get type info for field {field_info['name']}: {e}")
            field_info['type_info'] = {}

        # Add semantic analysis if we have field name and type - with safety checks
        if field_info['name'] and isinstance(field_info['name'], str):
            try:
                field_info['semantic_analysis'] = self.domain_analyzer.analyze_field_semantics(
                    field_info['name'], field_info['type']
                )
            except Exception as e:
                logger.warning(f"Failed to analyze field semantics for {field_info['name']}: {e}")
                field_info['semantic_analysis'] = None

        return field_info

    @staticmethod
    def _collect_related_fields(_data: Dict) -> List[Dict]:
        """Collect fields from related structures (placeholder for extension)."""
        # This method can be extended to collect fields from related sources
        # For now, return empty list
        return []

    @staticmethod
    def _collect_permissions_info(data: Dict) -> Dict[str, Any]:
        """Collect permissions-related information from entity data."""
        permissions_info = {
            'has_permissions': False,
            'permission_types': [],
            'roles_referenced': []
        }

        definition = data.get('definition', {})
        if isinstance(definition, dict):
            # Check for permissions in various locations
            if 'permissions' in definition:
                permissions_info['has_permissions'] = True
                permissions = definition['permissions']

                if isinstance(permissions, list):
                    for perm in permissions:
                        if isinstance(perm, dict):
                            if 'role' in perm:
                                permissions_info['roles_referenced'].append(perm['role'])
                            # Identify permission types
                            for perm_type in ['select', 'insert', 'update', 'delete']:
                                if perm_type in perm:
                                    permissions_info['permission_types'].append(perm_type)

        return permissions_info

    @staticmethod
    def _collect_model_info(data: Dict) -> Dict[str, Any]:
        """Collect Model-specific information."""
        model_info = {
            'is_model': data.get('kind') == 'Model',
            'object_type': None,
            'data_connector': None,
            'source_collection': None
        }

        if model_info['is_model']:
            definition = data.get('definition', {})
            if isinstance(definition, dict):
                model_info['object_type'] = definition.get('objectType')

                source = definition.get('source', {})
                if isinstance(source, dict):
                    model_info['data_connector'] = source.get('dataConnectorName')
                    model_info['source_collection'] = source.get('collection')

        return model_info

    @staticmethod
    def _collect_command_info(data: Dict) -> Dict[str, Any]:
        """Collect Command-specific information."""
        command_info = {
            'is_command': data.get('kind') == 'Command',
            'output_type': None,
            'data_connector': None,
            'graphql_info': {}
        }

        definition = data.get('definition', {})
        if isinstance(definition, dict):
            command_info['output_type'] = definition.get('outputType')

            # Extract data connector info
            source = definition.get('source', {})
            if isinstance(source, dict):
                command_info['data_connector'] = source.get('dataConnectorName')

            # Extract GraphQL info
            graphql = definition.get('graphql', {})
            if isinstance(graphql, dict):
                command_info['graphql_info'] = {
                    'root_field_name': graphql.get('rootFieldName'),
                    'root_field_kind': graphql.get('rootFieldKind')
                }

        return command_info

    @staticmethod
    def _is_duplicate_entity(entity_info: Dict, existing_entities: List[Dict]) -> bool:
        """Check if an entity is already in the collection."""
        for existing in existing_entities:
            if (existing.get('name') == entity_info.get('name') and
                    existing.get('kind') == entity_info.get('kind') and
                    existing.get('subgraph') == entity_info.get('subgraph') and
                    existing.get('file_path') == entity_info.get('file_path')):
                return True
        return False

    def _update_descriptions_from_dict(self, data: Dict, metadata: Dict,
                                       parent_path: str) -> None:
        """Update metadata with descriptions from enhanced documents."""
        current_name = data.get('definition', {}).get('name', data.get('name', ''))

        if 'kind' in data:
            entity_kind = data.get('kind')
            entity_name = data.get('definition', {}).get('name', data.get('name'))

            if entity_name and entity_kind:
                # Extract description (removing any relationship markers)
                description = data.get('definition', {}).get('description', data.get('description', ''))
                if description and config.relationship_marker in description:
                    description = description.replace(f"\n{config.relationship_marker}", "").replace(
                        config.relationship_marker, "")

                subgraph_context = metadata.get('subgraph')

                # Find and update the corresponding entity in metadata
                for entity_meta in metadata.get('entities', []):
                    if (entity_meta.get('name') == entity_name and
                            entity_meta.get('kind') == entity_kind and
                            entity_meta.get('subgraph') == subgraph_context and
                            entity_meta.get('file_path') == metadata.get('file_path')):
                        entity_meta['description'] = description
                        break

        # Recurse into nested structures
        new_parent_path = f"{parent_path}/{current_name if current_name else data.get('kind', 'dict_node')}".strip('/')
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                self.update_metadata_with_descriptions(value, metadata, new_parent_path)

    @staticmethod
    def get_collection_statistics(metadata: Dict) -> Dict[str, Any]:
        """
        Get statistics about the collected metadata.

        Args:
            metadata: Metadata dictionary

        Returns:
            Statistics dictionary
        """
        entities = metadata.get('entities', [])

        stats = {
            'total_entities': len(entities),
            'entities_with_descriptions': 0,
            'total_fields': 0,
            'fields_with_descriptions': 0,
            'entities_by_kind': {},
            'entities_by_subgraph': {},
            'avg_fields_per_entity': 0.0,
            'command_stats': {
                'total_commands': 0,
                'commands_with_fields': 0,
                'commands_resolved': 0,
                'avg_fields_per_command': 0.0
            }
        }

        total_fields = 0
        fields_with_descriptions = 0
        command_field_total = 0

        for entity in entities:
            # Count entities with descriptions
            if entity.get('description'):
                stats['entities_with_descriptions'] += 1

            # Count by kind
            kind = entity.get('kind', 'Unknown')
            stats['entities_by_kind'][kind] = stats['entities_by_kind'].get(kind, 0) + 1

            # Count by subgraph
            subgraph = entity.get('subgraph') or 'None'
            stats['entities_by_subgraph'][subgraph] = stats['entities_by_subgraph'].get(subgraph, 0) + 1

            # Count fields
            fields = entity.get('fields', [])
            total_fields += len(fields)

            # Track Command-specific statistics
            if kind == 'Command':
                stats['command_stats']['total_commands'] += 1
                if fields:
                    stats['command_stats']['commands_with_fields'] += 1
                    command_field_total += len(fields)
                    if entity.get('field_source') == 'resolved_from_object_type':
                        stats['command_stats']['commands_resolved'] += 1

            for field in fields:
                if field.get('description'):
                    fields_with_descriptions += 1

        stats['total_fields'] = total_fields
        stats['fields_with_descriptions'] = fields_with_descriptions

        if stats['total_entities'] > 0:
            stats['avg_fields_per_entity'] = total_fields / stats['total_entities']

        if stats['command_stats']['commands_with_fields'] > 0:
            stats['command_stats']['avg_fields_per_command'] = command_field_total / stats['command_stats'][
                'commands_with_fields']

        return stats


def create_metadata_collector() -> MetadataCollector:
    """
    Create a MetadataCollector instance.

    Returns:
        Configured MetadataCollector instance
    """
    return MetadataCollector()
