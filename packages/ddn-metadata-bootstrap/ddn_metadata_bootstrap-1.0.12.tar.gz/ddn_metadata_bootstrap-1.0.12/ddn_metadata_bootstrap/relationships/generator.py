#!/usr/bin/env python3

"""
Relationship YAML generation for creating OpenDD relationship definitions.
Converts detected relationships into proper YAML relationship structures.
Only generates relationships between ObjectTypes that are queryable (have Models or Query Commands).
Enhanced to minimize repetitive language and generate concise relationship descriptions.
"""

import logging
import os
import re
import json
import datetime
from typing import Dict, List, Any, Optional, Set, Tuple

from ..config import config
from ..utils.text_utils import to_camel_case, smart_pluralize

logger = logging.getLogger(__name__)


class RelationshipDebugger:
    """Debug specific entity relationship generation"""

    def __init__(self, debug_file_path="relationship_debug.log"):
        self.debug_file = debug_file_path
        self.target_entities = {
            'itmapp_snow_bam_business_application_dimension',
            'itmapp_business_service_conformed'
        }
        self.debug_data = []

    def log_debug(self, event, **kwargs):
        """Log debug event with timestamp"""
        entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'event': event,
            **kwargs
        }
        self.debug_data.append(entry)

    def write_debug_file(self):
        """Write all debug data to file"""

        def convert_sets_to_lists(obj):
            if isinstance(obj, (set, frozenset)):
                return list(obj)
            elif isinstance(obj, dict):
                return {k: convert_sets_to_lists(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets_to_lists(item) for item in obj]
            else:
                return obj

        with open(self.debug_file, 'w') as f:
            for entry in self.debug_data:
                json_safe_entry = convert_sets_to_lists(entry)
                f.write(json.dumps(json_safe_entry, indent=2) + "\n" + "=" * 80 + "\n")

    def is_target_entity(self, entity_name):
        """Check if entity is one we're debugging"""
        if not entity_name:
            return False
        simple_name = entity_name.split('/')[-1] if '/' in entity_name else entity_name
        return simple_name in self.target_entities


# Create global debugger instance
debugger = RelationshipDebugger()


def to_snake_case(text: str) -> str:
    """
    Convert text to snake_case.

    Args:
        text: Input text to convert

    Returns:
        snake_case version of the text
    """
    if not text:
        return text

    # Handle camelCase/PascalCase by inserting underscores before capitals
    snake_text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', text)
    snake_text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', snake_text)

    # Convert to lowercase and clean up multiple underscores
    snake_text = snake_text.lower()
    snake_text = re.sub(r'_+', '_', snake_text)
    snake_text = snake_text.strip('_')

    return snake_text


def smart_pluralize_snake(text: str) -> str:
    """
    Apply smart pluralization to snake_case text.

    Args:
        text: snake_case text to pluralize

    Returns:
        Pluralized snake_case text
    """
    if not text:
        return text

    parts = text.split('_')
    if parts:
        last_word_camel = to_camel_case(parts[-1], first_char_lowercase=True)
        pluralized_camel = smart_pluralize(last_word_camel)
        parts[-1] = to_snake_case(pluralized_camel)

    return '_'.join(parts)


class RelationshipGenerator:
    """
    Generates YAML relationship definitions from detected relationship patterns.

    Takes output from relationship detection and creates properly formatted
    OpenDD Relationship kind definitions with concise, meaningful descriptions.
    """

    _used_names_per_entity: Dict[str, Set[str]] = {}

    def __init__(self):
        """Initialize the relationship generator."""
        self.generated_relationships: List[Dict[str, Any]] = []
        self.relationship_signatures: Set[Tuple] = set()
        self.input_dir = config.input_dir

    def _generate_shared_field_relationship(self, source_qnk: str, target_qnk: str,
                                            shared_field: str,
                                            entities_map: Dict[str, Dict],
                                            is_target_rel: bool = False,
                                            direction: str = "") -> Optional[Dict[str, Any]]:
        """
        Generate shared field relationship with enhanced debugging.
        OPTIMIZED: Uses hash-based field lookups instead of linear searches.
        """
        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if is_target_rel:
            debugger.log_debug(f"VALIDATION_START_{direction}",
                               source_qnk=source_qnk,
                               target_qnk=target_qnk,
                               source_name=source_name,
                               target_name=target_name,
                               shared_field=shared_field)

        if not source_name or not target_name:
            return None

        # Validate target
        if not self._is_valid_relationship_target(target_qnk, target_info):
            logger.debug(f"Skipping shared field relationship - invalid target {target_qnk}")
            return None

        # Validate source
        if not source_info.get('is_queryable', False):
            logger.debug(f"Skipping shared field relationship - non-queryable source {source_qnk}")
            return None

        # OPTIMIZED: Use hash-based field lookups instead of _find_original_field_name
        source_field_name = self._find_original_field_name_optimized(shared_field, source_info)
        target_field_name = self._find_original_field_name_optimized(shared_field, target_info)

        if not source_field_name or not target_field_name:
            return None

        # Generate relationship name
        base_target_name = self.generate_relationship_name(target_name, "multiple")
        shared_field_suffix = to_snake_case(shared_field)
        base_rel_name = f"{base_target_name}_by_{shared_field_suffix}"

        # Resolve naming conflicts
        if source_name not in RelationshipGenerator._used_names_per_entity:
            RelationshipGenerator._used_names_per_entity[source_name] = set()

        existing_names = self._get_all_existing_names(source_info)
        final_rel_name = self._resolve_naming_conflict(
            base_rel_name, existing_names, target_name, source_name
        )

        RelationshipGenerator._used_names_per_entity[source_name].add(final_rel_name)

        # Build target block
        target_block = {
            "name": target_name,
            "relationshipType": "Array"
        }

        # Add subgraph if cross-subgraph relationship
        if target_info.get('subgraph') and target_info.get('subgraph') != source_info.get('subgraph'):
            target_block['subgraph'] = target_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": final_rel_name,
            "sourceType": source_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": source_field_name}]},
                "target": {"modelField": [{"fieldName": target_field_name}]}
            }]
        }

        return {
            'target_file_path': source_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    @staticmethod
    def _find_original_field_name_optimized(field_name_lower: str, entity_info: Dict) -> Optional[str]:
        """
        Find the original case field name from entity info using hash lookup.
        OPTIMIZED: Uses pre-computed field lookup dictionary instead of linear search.

        Args:
            field_name_lower: Field name in lowercase or snake_case
            entity_info: Entity information dictionary with field_name_lookup

        Returns:
            Original case field name if found, None otherwise
        """
        # First try direct lookup (for exact lowercase matches)
        field_name_lookup = entity_info.get('field_name_lookup', {})
        field_info = field_name_lookup.get(field_name_lower)
        if field_info:
            return field_info.get('name')

        # If not found, try snake_case lookup
        field_names_snake_lookup = entity_info.get('field_names_snake_lookup', {})
        original_name = field_names_snake_lookup.get(field_name_lower)
        if original_name:
            return original_name

        return None

    @staticmethod
    def _get_all_existing_names(entity_info: Dict) -> Set[str]:
        """
        Get all existing relationship and field names for conflict detection.
        OPTIMIZED: Uses pre-computed field lookup instead of iterating through fields.
        """
        existing_relationship_names = set([
            name
            for names in RelationshipGenerator._used_names_per_entity.values()
            for name in names
        ])

        # OPTIMIZED: Use pre-computed field lookup keys instead of iterating
        field_name_lookup = entity_info.get('field_name_lookup', {})
        existing_field_names = set(field_name_lookup.keys())  # Already lowercase

        return existing_relationship_names.union(existing_field_names)

    def _is_valid_relationship_target(self, target_qnk: str, target_info: Dict) -> bool:
        """
        Check if entity can be a valid relationship target.

        Re-reads original YAML files to make validation decisions.

        Args:
            target_qnk: Qualified name of target entity
            target_info: Target entity information

        Returns:
            True if entity can be a relationship target, False otherwise
        """
        is_target_entity = debugger.is_target_entity(target_qnk)

        if is_target_entity:
            debugger.log_debug("TARGET_VALIDATION_START",
                               target_qnk=target_qnk,
                               target_info_keys=list(target_info.keys()),
                               input_dir=self.input_dir)

        if not self.input_dir:
            error_msg = "Generator input_dir not set - cannot validate relationship targets"
            if is_target_entity:
                debugger.log_debug("TARGET_VALIDATION_FAIL_NO_INPUT_DIR", error=error_msg)
            raise ValueError(error_msg)

        entity_name = target_qnk.split('/')[-1] if '/' in target_qnk else target_qnk
        file_path = target_info.get('file_path')

        if is_target_entity:
            debugger.log_debug("TARGET_VALIDATION_FILE_INFO",
                               entity_name=entity_name,
                               file_path=file_path)

        if not entity_name or not file_path:
            error_msg = f"Cannot validate {target_qnk} - missing entity name or file path"
            if is_target_entity:
                debugger.log_debug("TARGET_VALIDATION_FAIL_MISSING_INFO", error=error_msg)
            raise ValueError(error_msg)

        try:
            from ..utils.yaml_utils import load_yaml_documents

            full_file_path = os.path.join(self.input_dir, file_path)
            documents = load_yaml_documents(str(full_file_path))

            entities_in_file = {}
            for doc in documents:
                if isinstance(doc, dict) and doc.get('kind') in ['ObjectType', 'Model', 'Command']:
                    doc_name = doc.get('definition', {}).get('name') or doc.get('name')
                    if doc_name:
                        kind = doc.get('kind')
                        if doc_name not in entities_in_file:
                            entities_in_file[doc_name] = set()
                        entities_in_file[doc_name].add(kind)

            if entity_name not in entities_in_file:
                raise ValueError(f"Entity {entity_name} not found in file {full_file_path}")

            entity_kinds = entities_in_file[entity_name]

            # Commands cannot be relationship targets
            if 'Command' in entity_kinds and len(entity_kinds) == 1:
                logger.info(f"BLOCKED pure Command {target_qnk} - cannot be relationship target")
                return False

            # Command-only ObjectTypes cannot be relationship targets
            if 'ObjectType' in entity_kinds and 'Command' in entity_kinds and 'Model' not in entity_kinds:
                logger.debug(f"BLOCKED Command-only ObjectType {target_qnk} - no Model backing")
                return False

            # Models are valid targets
            if 'Model' in entity_kinds:
                logger.debug(f"ALLOWED Model {target_qnk} as relationship target")
                return True

            # Model-backed ObjectTypes are valid targets
            if 'ObjectType' in entity_kinds and 'Model' in entity_kinds:
                logger.debug(f"ALLOWED Model-backed ObjectType {target_qnk} as relationship target")
                return True

            # Pure ObjectTypes are not valid targets
            if 'ObjectType' in entity_kinds and len(entity_kinds) == 1:
                logger.info(f"BLOCKED pure ObjectType {target_qnk} - no backing")
                return False

            logger.warning(f"BLOCKED {target_qnk} - unexpected entity combination: {entity_kinds}")
            return False

        except Exception as e:
            raise Exception(f"Cannot validate relationship target {target_qnk}: {e}") from e

    def _generate_forward_relationship(self, fk_rel: Dict[str, Any],
                                       entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Generate forward (many-to-one or one-to-one) relationship."""
        source_qnk = fk_rel['from_entity']
        target_qnk = fk_rel['to_entity']
        from_field = fk_rel['from_field']
        to_field = fk_rel['to_field_name']

        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if not source_name or not target_name:
            return None

        # Validate target
        if not self._is_valid_relationship_target(target_qnk, target_info):
            logger.info(f"Skipping forward relationship to invalid target {target_qnk}")
            return None

        # Validate source
        if not source_info.get('is_queryable', False):
            logger.info(f"Skipping forward relationship from non-queryable source {source_qnk}")
            return None

        # Generate relationship name
        base_rel_name = self.generate_relationship_name_from_field(
            from_field, target_name, "single"
        )

        # Resolve naming conflicts
        if source_name not in RelationshipGenerator._used_names_per_entity:
            RelationshipGenerator._used_names_per_entity[source_name] = set()

        existing_names = self._get_all_existing_names(source_info)
        final_rel_name = self._resolve_naming_conflict(
            base_rel_name, existing_names, target_name, source_name
        )

        RelationshipGenerator._used_names_per_entity[source_name].add(final_rel_name)

        # Build target block
        target_block = {
            "name": target_name,
            "relationshipType": "Object"
        }

        # Add subgraph if cross-subgraph relationship
        if target_info.get('subgraph') and target_info.get('subgraph') != source_info.get('subgraph'):
            target_block['subgraph'] = target_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": final_rel_name,
            "sourceType": source_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": from_field}]},
                "target": {"modelField": [{"fieldName": to_field}]}
            }]
        }

        logger.debug(f"Generated forward relationship: {source_name}.{final_rel_name} -> {target_name}")

        return {
            'target_file_path': source_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    def _generate_reverse_relationship(self, fk_rel: Dict[str, Any],
                                       entities_map: Dict[str, Dict]) -> Optional[Dict[str, Any]]:
        """Generate reverse (one-to-many) relationship."""
        source_qnk = fk_rel['from_entity']
        target_qnk = fk_rel['to_entity']
        from_field = fk_rel['from_field']
        to_field = fk_rel['to_field_name']

        source_info = entities_map.get(source_qnk, {})
        target_info = entities_map.get(target_qnk, {})

        source_name = source_info.get('name')
        target_name = target_info.get('name')

        if not source_name or not target_name:
            return None

        # Validate source as target for reverse relationship
        if not self._is_valid_relationship_target(source_qnk, source_info):
            logger.debug(f"Skipping reverse relationship - invalid target {source_qnk}")
            return None

        # Validate target as source for reverse relationship
        if not target_info.get('is_queryable', False):
            logger.debug(f"Skipping reverse relationship - non-queryable source {target_qnk}")
            return None

        # Generate reverse relationship name
        base_source_name = self._clean_field_name_for_relationship(from_field)
        if base_source_name:
            source_snake = to_snake_case(source_name)
            base_source_snake = to_snake_case(base_source_name)
            base_rel_name = f"{smart_pluralize_snake(source_snake)}_by_{base_source_snake}"
        else:
            base_rel_name = self.generate_relationship_name(source_name, "multiple")

        # Resolve naming conflicts
        if target_name not in RelationshipGenerator._used_names_per_entity:
            RelationshipGenerator._used_names_per_entity[target_name] = set()

        existing_names = self._get_all_existing_names(target_info)
        final_rel_name = self._resolve_naming_conflict(
            base_rel_name, existing_names, source_name, target_name
        )

        RelationshipGenerator._used_names_per_entity[target_name].add(final_rel_name)

        # Build target block
        target_block = {
            "name": source_name,
            "relationshipType": "Array"
        }

        # Add subgraph if cross-subgraph relationship
        if source_info.get('subgraph') and source_info.get('subgraph') != target_info.get('subgraph'):
            target_block['subgraph'] = source_info.get('subgraph')

        # Build relationship definition
        relationship_def = {
            "name": final_rel_name,
            "sourceType": target_name,
            "target": {"model": target_block},
            "mapping": [{
                "source": {"fieldPath": [{"fieldName": to_field}]},
                "target": {"modelField": [{"fieldName": from_field}]}
            }]
        }

        logger.debug(f"Generated reverse relationship: {target_name}.{final_rel_name} -> {source_name}[]")

        return {
            'target_file_path': source_info.get('file_path'),
            'relationship_definition': self.create_relationship_yaml_structure(relationship_def)
        }

    def generate_foreign_key_relationships(self, fk_relationships: List[Dict[str, Any]],
                                           entities_map: Dict[str, Dict],
                                           existing_signatures: Set[Tuple] = None) -> List[Dict[str, Any]]:
        """Generate relationship YAML definitions for foreign key relationships."""
        generated = []

        for fk_rel in fk_relationships:
            # Generate forward relationship
            forward_rel = self._generate_forward_relationship(fk_rel, entities_map)
            if forward_rel:
                target_qnk = fk_rel.get('to_entity')
                target_info = entities_map.get(target_qnk, {})
                if self._is_valid_relationship_target(target_qnk, target_info):
                    generated.append(forward_rel)

            # Generate reverse relationship
            reverse_rel = self._generate_reverse_relationship(fk_rel, entities_map)
            if reverse_rel:
                target_qnk = fk_rel.get('from_entity')
                target_info = entities_map.get(target_qnk, {})
                if self._is_valid_relationship_target(target_qnk, target_info):
                    generated.append(reverse_rel)

        # Deduplicate against existing relationships
        if existing_signatures and not config.rebuild_all_relationships:
            generated = self.deduplicate_relationships(generated, existing_signatures)

        logger.info(f"Generated {len(generated)} foreign key relationship definitions")
        return generated

    def generate_shared_field_relationships(self, shared_relationships: List[Dict[str, Any]],
                                            entities_map: Dict[str, Dict],
                                            existing_signatures: Set[Tuple] = None) -> List[Dict[str, Any]]:
        """Generate shared field relationships with enhanced debugging."""
        generated = []

        for shared_rel in shared_relationships:
            from_entity = shared_rel['from_entity']
            to_entity = shared_rel['to_entity']
            shared_field = shared_rel['shared_field']

            is_target_rel = (debugger.is_target_entity(from_entity) or
                             debugger.is_target_entity(to_entity))

            # Generate bidirectional relationships
            rel1 = self._generate_shared_field_relationship(
                from_entity, to_entity, shared_field, entities_map, is_target_rel, "DIRECTION_1"
            )
            if rel1:
                generated.append(rel1)

            rel2 = self._generate_shared_field_relationship(
                to_entity, from_entity, shared_field, entities_map, is_target_rel, "DIRECTION_2"
            )
            if rel2:
                generated.append(rel2)

        debugger.write_debug_file()

        if existing_signatures and not config.rebuild_all_relationships:
            generated = self.deduplicate_relationships(generated, existing_signatures)

        logger.info(f"Generated {len(generated)} shared field relationship definitions")
        return generated

    @staticmethod
    def _resolve_naming_conflict(base_name: str, existing_names: Set[str],
                                 target_name: str, source_name: str) -> str:
        """Resolve naming conflicts efficiently."""
        final_name = base_name

        if base_name.lower() in {name.lower() for name in existing_names}:
            # Try with target suffix
            target_suffix = to_snake_case(target_name)
            base_snake = to_snake_case(base_name)
            final_name = f"{base_snake}_{target_suffix}"

            # If still conflicts, add numbered suffix
            counter = 2
            original_final = final_name
            while final_name.lower() in {name.lower() for name in existing_names}:
                final_name = f"{original_final}_{counter}"
                counter += 1
                if counter > 50:
                    logger.warning(f"Could not resolve naming conflict for {source_name}.{base_name}")
                    break

        return final_name

    @classmethod
    def fix_existing_relationship_conflicts(cls, file_paths: List[str]) -> Dict[str, Any]:
        """Fix existing relationship conflicts by reading and modifying files directly."""
        from ..utils.yaml_utils import load_yaml_documents, save_yaml_documents

        logger.info("Scanning files for existing relationship conflicts...")

        conflicts_found = 0
        conflicts_fixed = 0
        conflict_details = []
        files_modified = set()

        relationships_by_entity = {}
        file_documents = {}

        # First pass: scan files and group relationships
        for file_path in file_paths:
            try:
                documents = load_yaml_documents(file_path)
                file_documents[file_path] = documents

                for doc_idx, doc in enumerate(documents):
                    if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                        definition = doc.get('definition', {})
                        source_type = definition.get('sourceType')
                        rel_name = definition.get('name')

                        if source_type and rel_name:
                            if source_type not in relationships_by_entity:
                                relationships_by_entity[source_type] = {}

                            if rel_name not in relationships_by_entity[source_type]:
                                relationships_by_entity[source_type][rel_name] = []

                            location_info = {
                                'file_path': file_path,
                                'doc_index': doc_idx,
                                'document': doc,
                                'definition': definition,
                                'target_name': definition.get('target', {}).get('model', {}).get('name', 'unknown')
                            }

                            relationships_by_entity[source_type][rel_name].append(location_info)

            except Exception as e:
                logger.error(f"Error scanning file {file_path}: {e}")

        # Second pass: find and fix conflicts
        for source_type, relationships_by_name in relationships_by_entity.items():
            for rel_name, rel_instances in relationships_by_name.items():
                if len(rel_instances) > 1:
                    conflicts_found += 1
                    target_names = [inst['target_name'] for inst in rel_instances]

                    logger.info(
                        f"Conflict: {source_type}.{rel_name} ({len(rel_instances)} instances) -> {', '.join(target_names)}")

                    prioritized_instances = cls._prioritize_existing_relationship_instances(rel_instances, rel_name)
                    entity_used_names = set(relationships_by_name.keys())

                    for i, instance in enumerate(prioritized_instances):
                        if i == 0:
                            logger.info(f"  Keeping: {source_type}.{rel_name} -> {instance['target_name']}")
                            continue

                        # Generate new name
                        target_name = instance['target_name']
                        if target_name:
                            rel_name_snake = to_snake_case(rel_name)
                            target_snake = to_snake_case(target_name)
                            new_name = f"{rel_name_snake}_{target_snake}"
                        else:
                            new_name = f"{to_snake_case(rel_name)}_{i + 1}"

                        # Ensure uniqueness
                        counter = 2
                        original_new_name = new_name
                        while new_name.lower() in {name.lower() for name in entity_used_names}:
                            new_name = f"{original_new_name}_{counter}"
                            counter += 1

                        # Update document
                        instance['document']['definition']['name'] = new_name
                        entity_used_names.add(new_name)
                        files_modified.add(instance['file_path'])

                        conflicts_fixed += 1
                        conflict_details.append({
                            'entity': source_type,
                            'old_name': rel_name,
                            'new_name': new_name,
                            'target': target_name,
                            'file': instance['file_path']
                        })

                        logger.info(f"  Renamed: {source_type}.{rel_name} -> {source_type}.{new_name}")

        # Save modified files
        if conflicts_fixed > 0:
            files_saved = 0
            for file_path in files_modified:
                try:
                    documents = file_documents[file_path]
                    save_yaml_documents(documents, file_path)
                    files_saved += 1
                except Exception as e:
                    logger.error(f"Error saving {file_path}: {e}")

            logger.info(f"Saved fixes to {files_saved} files")

        return {
            'conflicts_found': conflicts_found,
            'conflicts_fixed': conflicts_fixed,
            'conflict_details': conflict_details,
            'files_modified': len(files_modified)
        }

    @classmethod
    def _prioritize_existing_relationship_instances(cls, instances: List[Dict[str, Any]],
                                                    rel_name: str) -> List[Dict[str, Any]]:
        """Prioritize relationship instances to determine which keeps the simple name."""

        def priority_score(instance):
            definition = instance['definition']
            target_name = definition.get('target', {}).get('model', {}).get('name', '')

            if not target_name:
                return 999, target_name, instance['file_path']

            target_lower = target_name.lower()
            rel_name_lower = rel_name.lower()

            # Exact match gets highest priority
            if target_lower == rel_name_lower:
                return 0, target_name, instance['file_path']

            # Contains relationship name
            if rel_name_lower in target_lower:
                return 1, target_name, instance['file_path']

            # Relationship name contains target
            if target_lower in rel_name_lower:
                return 2, target_name, instance['file_path']

            # Alphabetical order
            return 3, target_name, instance['file_path']

        return sorted(instances, key=priority_score)

    @classmethod
    def initialize_with_existing_relationships(cls, file_paths: List[str]):
        """Initialize used names tracking with existing relationships."""
        if config.rebuild_all_relationships:
            logger.info("REBUILD MODE: Skipping existing relationship initialization")
            return

        from ..utils.yaml_utils import load_yaml_documents

        cls._used_names_per_entity.clear()

        logger.info(f"Scanning {len(file_paths)} files for existing relationships...")

        existing_count = 0
        for file_path in file_paths:
            try:
                documents = load_yaml_documents(file_path)
                for doc in documents:
                    if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                        definition = doc.get('definition', {})
                        source_type = definition.get('sourceType')
                        rel_name = definition.get('name')

                        if source_type and rel_name:
                            if source_type not in cls._used_names_per_entity:
                                cls._used_names_per_entity[source_type] = set()

                            cls._used_names_per_entity[source_type].add(rel_name)
                            existing_count += 1

            except Exception as e:
                logger.error(f"Error scanning {file_path}: {e}")

        logger.info(f"Loaded {existing_count} existing relationship names")

    @classmethod
    def get_used_names_statistics(cls) -> Dict[str, Any]:
        """Get statistics about currently tracked used names."""
        total_entities = len(cls._used_names_per_entity)
        total_names = sum(len(names) for names in cls._used_names_per_entity.values())

        return {
            'entities_with_relationships': total_entities,
            'total_relationship_names': total_names,
            'average_relationships_per_entity': total_names / total_entities if total_entities > 0 else 0,
            'entities_with_most_relationships': sorted(
                [(entity, len(names)) for entity, names in cls._used_names_per_entity.items()],
                key=lambda x: x[1], reverse=True
            )[:5]
        }

    @staticmethod
    def generate_relationship_name_from_field(field_name: str, target_entity_name: str,
                                              relationship_type: str = "single") -> str:
        """Generate relationship name based on foreign key field name."""
        if not field_name:
            return RelationshipGenerator.generate_relationship_name(target_entity_name, relationship_type)

        cleaned_name = RelationshipGenerator._clean_field_name_for_relationship(field_name)

        if not cleaned_name:
            return RelationshipGenerator.generate_relationship_name(target_entity_name, relationship_type)

        snake_name = to_snake_case(cleaned_name)

        if relationship_type == "multiple":
            return smart_pluralize_snake(snake_name)
        else:
            return snake_name

    @staticmethod
    def generate_relationship_name(target_entity_name: str,
                                   relationship_type: str = "single") -> str:
        """Generate relationship names based on target entity and cardinality."""
        if not target_entity_name:
            return ""

        base_name = to_snake_case(target_entity_name)

        if relationship_type == "multiple":
            return smart_pluralize_snake(base_name)
        else:
            return base_name

    @staticmethod
    def _clean_field_name_for_relationship(field_name: str) -> str:
        """Clean field name to create semantic relationship name."""
        if not field_name:
            return ""

        cleaned = field_name.lower().strip()

        # Remove common foreign key suffixes
        suffixes_to_remove = ['_id', '_key', '_ref', '_fk', '_foreign_key', 'id', 'key', 'ref']

        for suffix in suffixes_to_remove:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
                break

        if not cleaned:
            return ""

        return cleaned.rstrip('_')

    @staticmethod
    def create_relationship_yaml_structure(relationship_def: Dict[str, Any]) -> Dict[str, Any]:
        """Create the complete YAML structure for a relationship definition."""
        return {
            "kind": "Relationship",
            "version": "v1",
            "definition": relationship_def
        }

    def deduplicate_relationships(self, relationships: List[Dict[str, Any]],
                                  existing_signatures: Set[Tuple]) -> List[Dict[str, Any]]:
        """Remove duplicate relationships based on their signatures."""
        deduplicated = []
        seen_signatures = existing_signatures.copy()

        for rel_item in relationships:
            signature = self.extract_relationship_signature(rel_item)
            if signature and signature not in seen_signatures:
                deduplicated.append(rel_item)
                seen_signatures.add(signature)
            elif not signature:
                logger.warning("Could not create signature for relationship, including anyway")
                deduplicated.append(rel_item)

        logger.info(f"Deduplicated {len(relationships)} relationships to {len(deduplicated)}")
        return deduplicated

    def generate_relationship_descriptions(self, relationships: List[Dict[str, Any]],
                                           _entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Generate concise descriptions for relationship definitions."""
        enhanced_relationships = []
        descriptions_added = 0

        for rel_item in relationships:
            enhanced_rel = rel_item.copy()

            rel_def = rel_item.get('relationship_definition', {}).get('definition', {})
            rel_name = rel_def.get('name', '')
            source_type = rel_def.get('sourceType', '')
            target_info = rel_def.get('target', {}).get('model', {})
            target_name = target_info.get('name', '')
            relationship_type = target_info.get('relationshipType', 'Object')

            existing_description = None
            if 'relationship_definition' in enhanced_rel:
                existing_description = enhanced_rel['relationship_definition']['definition'].get('description')

            if not existing_description:
                description = self._generate_relationship_description(
                    rel_name, source_type, target_name, relationship_type
                )

                if description:
                    if 'relationship_definition' in enhanced_rel:
                        enhanced_rel['relationship_definition']['definition']['description'] = description
                    else:
                        if 'definition' not in enhanced_rel:
                            enhanced_rel['definition'] = {}
                        enhanced_rel['definition']['description'] = description

                    descriptions_added += 1

            enhanced_relationships.append(enhanced_rel)

        logger.info(f"Added {descriptions_added} relationship descriptions")
        return enhanced_relationships

    @staticmethod
    def _generate_relationship_description(_rel_name: str, _source_type: str,
                                           target_name: str, relationship_type: str) -> str:
        """Generate concise description for a relationship."""
        if relationship_type == "Array":
            return f"Associated {target_name} entities."
        else:
            return f"Associated {target_name} entity."

    @staticmethod
    def _find_original_field_name(field_name_lower: str, entity_info: Dict) -> Optional[str]:
        """Find the original case field name from entity info."""
        for field in entity_info.get('fields', []):
            if field.get('name', '').lower() == field_name_lower:
                return field.get('name')
        return None

    @staticmethod
    def extract_relationship_signature(rel_item: Dict[str, Any]) -> Optional[Tuple]:
        """Extract a unique signature from a relationship definition."""
        try:
            if 'relationship_definition' in rel_item:
                rel_def = rel_item['relationship_definition']
            else:
                rel_def = rel_item

            definition = rel_def.get('definition', {})
            source_type = definition.get('sourceType')
            mapping = definition.get('mapping', [])

            if not source_type or not mapping:
                return None

            canonical_mapping_parts = []
            for m_item in mapping:
                if isinstance(m_item, dict):
                    source_fp = m_item.get('source', {}).get('fieldPath', [])
                    target_block = m_item.get('target', {})
                    target_fp = target_block.get('modelField', target_block.get('fieldPath', []))

                    source_tuple = tuple(fp.get('fieldName', fp) if isinstance(fp, dict) else fp for fp in source_fp)
                    target_tuple = tuple(fp.get('fieldName', fp) if isinstance(fp, dict) else fp for fp in target_fp)

                    canonical_mapping_parts.append((source_tuple, target_tuple))

            canonical_mapping_parts.sort()
            return source_type, frozenset(canonical_mapping_parts)

        except Exception as e:
            logger.warning(f"Could not create relationship signature: {e}")
            return None


def create_relationship_generator(_input_dir: str = None) -> RelationshipGenerator:
    """
    Create a RelationshipGenerator instance.

    Args:
        _input_dir: Base directory for schema files

    Returns:
        Configured RelationshipGenerator instance
    """
    return RelationshipGenerator()
