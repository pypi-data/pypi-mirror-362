#!/usr/bin/env python3

"""
Relationship mapping and context generation for schema entities.
Builds comprehensive relationship maps and provides context for description enhancement.
Only processes relationships between ObjectTypes that are queryable (have Models or Query Commands).

ENHANCED: Added FK-aware shared field filtering to prevent redundant relationships.
"""

import logging
import os
import re
from typing import Dict, List, Optional, Any, Tuple, Set

from .detector import RelationshipDetector
from .generator import RelationshipGenerator
from ..config import config
from ..schema.metadata_collector import create_metadata_collector

logger = logging.getLogger(__name__)


class RelationshipMapper:
    """
    Builds comprehensive relationship maps and provides relationship context.

    This class takes detected relationships and creates structured maps that can be
    used to enhance entity descriptions with relationship information and generate
    relationship definitions for the schema.

    Only processes relationships between ObjectTypes that are queryable (have Models or Query Commands).
    ENHANCED: Filters shared field relationships when FK relationships already exist between entities.
    """

    def __init__(self, relationship_detector=None, relationship_generator=None, metadata_collector=None):
        """
        Initialize the relationship mapper.

        Args:
            relationship_detector: Optional RelationshipDetector instance (will create new if None)
            relationship_generator: Optional RelationshipGenerator instance (will create new if None)
            metadata_collector: Optional MetadataCollector instance (will create new if None)
        """
        # Use dependency injection when available, otherwise create new instances
        self.relationship_detector = relationship_detector or RelationshipDetector()
        self.relationship_generator = relationship_generator or RelationshipGenerator()
        self.metadata_collector = metadata_collector or create_metadata_collector()

    def _build_entities_map(self, schema_metadata: Dict[str, Dict], input_dir: str) -> Dict[str, Dict]:
        """
        Build a unified entities map from file metadata.

        Analyzes each file to determine which ObjectTypes are queryable (have associated Models or Query Commands)
        and marks them appropriately in the entity information.

        ENHANCED: Now includes Command field resolution to ensure Commands have proper fields for relationship detection.
        OPTIMIZED: Builds field lookup dictionaries for fast hash-based field access.
        """
        entities_map = {}
        total_entities = 0

        for file_path, file_metadata in schema_metadata.items():
            subgraph = file_metadata.get('subgraph')

            # CRITICAL: Resolve Command fields before proceeding with relationship analysis
            # This ensures Commands have their output fields populated from referenced ObjectTypes
            logger.debug(f"Resolving Command fields for file: {file_path}")
            self.metadata_collector.resolve_command_fields(file_metadata)

            # First pass: collect all ObjectTypes
            object_types = {}
            for entity_data in file_metadata.get('entities', []):
                if entity_data.get('kind') == 'ObjectType':
                    object_type_name = entity_data.get('name')
                    if object_type_name:
                        object_types[object_type_name] = entity_data

            # Second pass: identify which ObjectTypes have Models OR Query Commands
            models_for_object_types = set()
            query_commands_for_object_types = set()

            # Models - use existing working logic with processed metadata
            for entity_data in file_metadata.get('entities', []):
                entity_kind = entity_data.get('kind')

                if entity_kind == 'Model':
                    # Existing Model detection logic (WORKS FINE)
                    model_object_type = entity_data.get('model_info', {}).get('object_type')

                    # Fallback to definition.objectType for compatibility
                    if not model_object_type:
                        model_object_type = entity_data.get('definition', {}).get('objectType')

                    if model_object_type:
                        models_for_object_types.add(model_object_type)
                        logger.debug(f"Found Model for ObjectType: {model_object_type}")

                elif entity_kind == "Command":
                    # NEW: Query Command detection logic - re-read YAML for proper Command data
                    try:
                        from ..utils.yaml_utils import load_yaml_documents
                        full_file_path = os.path.join(input_dir, file_path)
                        documents = load_yaml_documents(full_file_path)

                        # Find this specific command in the raw YAML
                        command_definition = None
                        entity_name = entity_data.get('name')

                        for doc in documents:
                            if (isinstance(doc, dict) and
                                    doc.get('kind') == 'Command' and
                                    doc.get('definition', {}).get('name') == entity_name):
                                command_definition = doc.get('definition', {})
                                break

                        if command_definition:
                            graphql_info = command_definition.get('graphql', {})
                            root_field_kind = graphql_info.get('rootFieldKind')

                            logger.debug(f"Found Command: name={entity_name}, rootFieldKind={root_field_kind}")

                            if root_field_kind == 'Query':
                                # Determine how Query Commands reference ObjectTypes
                                command_object_type = command_definition.get('objectType')

                                # If no explicit objectType, try to derive from outputType
                                if not command_object_type:
                                    output_type = command_definition.get('outputType', '')
                                    command_object_type = self.metadata_collector.parse_graphql_output_type(
                                        output_type)

                                if command_object_type:
                                    query_commands_for_object_types.add(command_object_type)
                                    logger.debug(f"Found Query Command for ObjectType: {command_object_type}")
                            else:
                                logger.debug(
                                    f"Skipping Command {entity_name} - not a Query (rootFieldKind: {root_field_kind})")
                        else:
                            logger.warning(f"Could not find Command definition for {entity_name} in {file_path}")

                    except Exception as e:
                        logger.error(f"Error re-reading YAML for Command {entity_data.get('name')}: {e}")

            # Combine both sets - these ObjectTypes are queryable
            queryable_object_types = models_for_object_types.union(query_commands_for_object_types)
            logger.debug(f"Queryable ObjectTypes found: {queryable_object_types}")
            logger.debug(f"  - Via Models: {models_for_object_types}")
            logger.debug(f"  - Via Query Commands: {query_commands_for_object_types}")

            # Debug: Check for overlap
            both_model_and_command = models_for_object_types.intersection(query_commands_for_object_types)
            command_only = query_commands_for_object_types - models_for_object_types
            model_only = models_for_object_types - query_commands_for_object_types
            logger.debug(f"  - Model only: {model_only}")
            logger.debug(f"  - Command only: {command_only}")
            logger.debug(f"  - Both Model and Command: {both_model_and_command}")

            # Third pass: build entity map with queryability info
            for entity_data in file_metadata.get('entities', []):
                total_entities += 1
                entity_name = entity_data.get('name')
                entity_kind = entity_data.get('kind', 'UnknownKind')

                if not entity_name:
                    continue

                # Build qualified name
                qnk = RelationshipMapper._build_qualified_name(entity_name, entity_kind, subgraph)

                # Enhance entity data with file path and queryability
                enhanced_entity_data = {**entity_data, 'file_path': file_path}

                # OPTIMIZATION: Build field lookup dictionaries for fast access
                self._build_field_lookup_dictionaries(enhanced_entity_data)

                # Determine if this entity is queryable
                if entity_kind == 'ObjectType':
                    is_queryable = entity_name in queryable_object_types
                    enhanced_entity_data['is_queryable'] = is_queryable
                    if is_queryable:
                        enhanced_entity_data['queryable_via'] = []
                        if entity_name in models_for_object_types:
                            enhanced_entity_data['queryable_via'].append('Model')
                        if entity_name in query_commands_for_object_types:
                            enhanced_entity_data['queryable_via'].append('Query')
                        logger.debug(
                            f"ObjectType {entity_name} is queryable via: {enhanced_entity_data['queryable_via']}")

                        # Debug: Check if this is Command-only
                        queryable_via = enhanced_entity_data['queryable_via']
                        if 'Query' in queryable_via and 'Model' not in queryable_via:
                            logger.debug(
                                f"COMMAND-ONLY ObjectType detected: {entity_name} - should NOT be relationship target")
                    else:
                        logger.debug(f"ObjectType {entity_name} is not queryable")

                elif entity_kind == 'Model':
                    # Models themselves are queryable if they have an ObjectType (use existing logic)
                    object_type_name = entity_data.get('model_info', {}).get('object_type')
                    if not object_type_name:
                        object_type_name = entity_data.get('definition', {}).get('objectType')

                    enhanced_entity_data['is_queryable'] = bool(object_type_name)
                    if object_type_name:
                        enhanced_entity_data['associated_object_type'] = object_type_name

                elif entity_kind == 'Command':
                    # Commands need to be checked from raw YAML since processed metadata loses the info
                    try:
                        from ..utils.yaml_utils import load_yaml_documents
                        full_file_path = os.path.join(input_dir, file_path)
                        documents = load_yaml_documents(full_file_path)

                        for doc in documents:
                            if (isinstance(doc, dict) and
                                    doc.get('kind') == 'Command' and
                                    doc.get('definition', {}).get('name') == entity_name):

                                definition = doc.get('definition', {})
                                graphql_info = definition.get('graphql', {})
                                root_field_kind = graphql_info.get('rootFieldKind')
                                enhanced_entity_data['is_queryable'] = (root_field_kind == 'Query')

                                if enhanced_entity_data['is_queryable']:
                                    # Store the ObjectType this Query Command returns (same as command name)
                                    command_object_type = definition.get('name')
                                    if command_object_type:
                                        enhanced_entity_data['associated_object_type'] = command_object_type
                                break
                    except Exception as e:
                        logger.error(f"Error re-reading Command {entity_name} from {file_path}: {e}")
                        enhanced_entity_data['is_queryable'] = False  # Default fallback

                else:
                    # Other kinds (TypePermissions, BooleanExpressionType, etc.) are not queryable
                    enhanced_entity_data['is_queryable'] = False

                entities_map[qnk] = enhanced_entity_data

        # Log statistics
        queryable_entities = sum(1 for info in entities_map.values() if info.get('is_queryable', False))
        non_queryable_entities = len(entities_map) - queryable_entities

        # Log Command field resolution statistics
        commands_with_fields = sum(1 for info in entities_map.values()
                                   if info.get('kind') == 'Command' and info.get('associated_object_type'))
        total_commands = sum(1 for info in entities_map.values() if info.get('kind') == 'Command')

        # Log field optimization statistics
        entities_with_optimized_lookups = sum(1 for info in entities_map.values()
                                              if 'field_name_lookup' in info)

        logger.info(f"Built entities map with {len(entities_map)} unique entities from {total_entities} total")
        logger.info(
            f"Queryability analysis: {queryable_entities} queryable entities, {non_queryable_entities} non-queryable entities")
        logger.info(f"Command field resolution: {commands_with_fields}/{total_commands} Commands now have fields")
        logger.info(
            f"Field lookup optimization: {entities_with_optimized_lookups}/{len(entities_map)} entities have optimized field lookups")

        return entities_map

    def _build_field_lookup_dictionaries(self, entity_data: Dict) -> None:
        """
        Build optimized field lookup dictionaries for fast hash-based field access.

        Adds the following lookup structures to entity_data:
        - field_name_lookup: {field_name.lower(): field_info} for case-insensitive lookups
        - field_types_lookup: {field_name.lower(): field_type} for quick type checking
        - field_names_snake_lookup: {snake_case_name: original_name} for snake_case conversions
        - primary_keys_snake_set: {snake_case_pk1, snake_case_pk2, ...} for fast PK checks

        Args:
            entity_data: Entity data dictionary to enhance with lookup structures
        """
        # Initialize lookup dictionaries
        entity_data['field_name_lookup'] = {}
        entity_data['field_types_lookup'] = {}
        entity_data['field_names_snake_lookup'] = {}

        # Build field lookups
        for field in entity_data.get('fields', []):
            field_name = field.get('name', '')
            field_type = field.get('type', '')

            if field_name:
                field_name_lower = field_name.lower()
                field_name_snake = self._camel_to_snake_case(field_name)

                # Build hash lookups for O(1) access
                entity_data['field_name_lookup'][field_name_lower] = field
                entity_data['field_types_lookup'][field_name_lower] = field_type
                entity_data['field_names_snake_lookup'][field_name_snake] = field_name

        # Pre-compute snake_case primary keys set for fast lookups
        primary_keys = entity_data.get('primary_keys', [])
        entity_data['primary_keys_snake_set'] = {
            self._camel_to_snake_case(pk) for pk in primary_keys
        }

        # Log optimization details for debugging
        field_count = len(entity_data.get('fields', []))
        pk_count = len(primary_keys)
        entity_name = entity_data.get('name', 'unknown')

        logger.debug(f"Built field lookups for {entity_name}: {field_count} fields, {pk_count} primary keys optimized")

    @staticmethod
    def _camel_to_snake_case(field_name: str) -> str:
        """
        Convert camelCase field names to snake_case for analysis only.

        Examples:
        - lastUsedFileName → last_used_file_name
        - userId → user_id
        - companyId → company_id
        - XMLHttpRequest → xml_http_request

        Args:
            field_name: Original field name (it may be camelCase or snake_case)

        Returns:
            snake_case version of the field name
        """
        if not field_name:
            return field_name

        # If already contains underscores, likely already snake_case
        if '_' in field_name:
            return field_name.lower()

        # Handle sequences of capitals (like XMLHttp → xml_http)
        # Insert underscore before capitals that follow lowercase or are followed by lowercase
        snake_case = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', field_name)
        snake_case = re.sub(r'([A-Z])([A-Z][a-z])', r'\1_\2', snake_case)

        # Convert to lowercase and remove any leading underscores
        return snake_case.lower().lstrip('_')

    def clear_existing_context(self):
        """
        Clear any cached or existing relationship context for rebuild mode.
        This ensures fresh relationship generation without influence from existing data.
        """
        # Clear the relationship detector's existing signatures
        if hasattr(self, 'relationship_detector') and hasattr(self.relationship_detector,
                                                              'existing_relationships_signatures'):
            self.relationship_detector.existing_relationships_signatures = set()
            logger.debug("🔄 REBUILD MODE: Cleared relationship detector signatures")

        # This method can be expanded later if other state needs clearing
        logger.debug("🔄 REBUILD MODE: Cleared existing relationship context")

    def build_relationship_map(self,
                               schema_metadata: Dict[str, Dict],
                               input_dir: str,
                               fix_existing_conflicts: bool = True,
                               remove_existing_invalid_targets: bool = True) -> Dict[str, Any]:
        """
        Build a comprehensive relationship map from collected schema metadata.

        FIXED: Properly handles rebuild_all_relationships flag throughout the process.
        ENHANCED: Added FK-aware shared field filtering to prevent redundant relationships.

        Args:
            input_dir:
            schema_metadata: Dictionary mapping file paths to their metadata
            fix_existing_conflicts: Whether to fix existing relationship name conflicts
            remove_existing_invalid_targets: Whether to remove existing relationships with invalid targets
        """

        # FIXED: Check rebuild flag early and skip existing relationship operations
        rebuild_mode = config.rebuild_all_relationships
        if rebuild_mode:
            logger.info("🔄 REBUILD MODE: Ignoring all existing relationships and building from scratch")
            fix_existing_conflicts = False
            remove_existing_invalid_targets = False

        # Extract file paths for file-based operations
        file_paths = [os.path.join(input_dir, file_path) for file_path in list(schema_metadata.keys())]

        # STEP 1: Extract and organize entities, identifying which are queryable
        entities_map = self._build_entities_map(schema_metadata, input_dir)

        # STEP 2: Remove existing invalid relationship targets if requested (skip in rebuild mode)
        invalid_removal_stats = None
        if remove_existing_invalid_targets and not rebuild_mode:
            logger.info("=== REMOVING EXISTING INVALID RELATIONSHIP TARGETS ===")
            invalid_removal_stats = self._remove_existing_invalid_relationships(file_paths, entities_map)
            if invalid_removal_stats and invalid_removal_stats.get('relationships_removed', 0) > 0:
                logger.info(f"Removed {invalid_removal_stats['relationships_removed']} existing invalid relationships")
            else:
                logger.info("No existing invalid relationship targets found")

        # STEP 3: Fix existing relationship conflicts if requested (skip in rebuild mode)
        conflict_fix_stats = None
        if fix_existing_conflicts and not rebuild_mode:
            logger.info("=== FIXING EXISTING RELATIONSHIP CONFLICTS ===")

            # Now that generator has loaded relationship data, use existing conflict resolution
            conflict_fix_stats = RelationshipGenerator.fix_existing_relationship_conflicts(file_paths)

            if conflict_fix_stats and conflict_fix_stats.get('conflicts_fixed', 0) > 0:
                logger.info(f"Fixed {conflict_fix_stats['conflicts_fixed']} existing conflicts in memory")
                # Use the modified metadata going forward
                schema_metadata = conflict_fix_stats.get('modified_metadata', schema_metadata)
            else:
                logger.info("No existing relationship conflicts found")

        # STEP 4: Initialize generator with existing relationships (skip in rebuild mode)
        existing_signatures = set()
        if not rebuild_mode:
            logger.info("=== INITIALIZING WITH EXISTING RELATIONSHIPS ===")
            RelationshipGenerator.initialize_with_existing_relationships(file_paths)

            # STEP 5: Scan for existing relationship signatures for deduplication
            existing_signatures = self.relationship_detector.scan_for_existing_relationships(file_paths)
            logger.info(f"Found {len(existing_signatures)} existing relationship signatures")
        else:
            logger.info("🔄 REBUILD MODE: Skipping existing relationship initialization")
            # Clear any existing relationship data in the generator
            if hasattr(RelationshipGenerator, 'clear_used_names'):
                RelationshipGenerator.clear_used_names()

        # Log statistics about queryability
        total_entities = len(entities_map)
        queryable_entities = sum(1 for info in entities_map.values() if info.get('is_queryable', False))
        logger.info(f"Entity analysis: {queryable_entities}/{total_entities} entities are queryable")

        # STEP 6: Detect relationships with FK-aware filtering
        logger.info("=== DETECTING NEW RELATIONSHIPS (FK-AWARE) ===")
        all_relationships = []

        # 1. Foreign key relationships (detect first)
        logger.info("Detecting foreign key relationships...")
        fk_relationships = self.relationship_detector.detect_foreign_key_relationships(entities_map)
        all_relationships.extend(fk_relationships)
        logger.info(f"Detected {len(fk_relationships)} FK relationships")

        # 2. Build connected entities map from FK relationships
        connected_entity_pairs = self._build_connected_entities_map(fk_relationships)
        logger.info(
            f"Built connected entities map: {len(connected_entity_pairs)} entity pairs already connected via FK")

        # Log some examples of connected pairs for debugging
        if connected_entity_pairs:
            sample_pairs = list(connected_entity_pairs)[:5]  # Show first 5
            logger.info(f"Example FK-connected pairs: {sample_pairs}")

        # 3. Shared field relationships (filtered to exclude FK-connected entities)
        logger.info("Detecting shared field relationships (excluding FK-connected entities)...")
        shared_relationships = self.relationship_detector.detect_shared_field_relationships(
            entities_map,
            exclude_connected_pairs=connected_entity_pairs
        )
        all_relationships.extend(shared_relationships)
        logger.info(f"Detected {len(shared_relationships)} shared field relationships (after FK filtering)")

        # 4. Naming pattern relationships
        logger.info("Detecting naming pattern relationships...")
        naming_relationships = self.relationship_detector.detect_naming_pattern_relationships(entities_map)
        all_relationships.extend(naming_relationships)
        logger.info(f"Detected {len(naming_relationships)} naming pattern relationships")

        # Log filtering effectiveness
        total_detected = len(fk_relationships) + len(shared_relationships) + len(naming_relationships)
        logger.info(
            f"Total relationships detected: {total_detected} (FK filtering prevented redundant shared field relationships)")

        # Deduplicate relationships
        unique_relationships = self._deduplicate_relationships(all_relationships)

        # STEP 7: Generate relationship YAML definitions
        if rebuild_mode:
            logger.info("🔄 REBUILD MODE: Generating fresh relationship YAML without existing signature checking")
        else:
            logger.info("=== GENERATING NEW RELATIONSHIP YAML ===")

        generated_yaml = self._generate_relationship_yaml(unique_relationships, entities_map, existing_signatures)

        # STEP 7.5: FINAL CLEANUP - Remove relationships targeting Commands/Command-only ObjectTypes
        logger.info("=== FINAL CLEANUP: REMOVING INVALID RELATIONSHIP TARGETS ===")
        generated_yaml = self._remove_invalid_relationship_targets(generated_yaml, entities_map)

        # STEP 8: Build the final relationship map
        relationship_map = {
            'entities': entities_map,
            'relationships': unique_relationships,
            'generated_yaml': generated_yaml,
            'statistics': self._calculate_map_statistics(entities_map, unique_relationships),
            'conflict_fix_stats': conflict_fix_stats,
            'invalid_removal_stats': invalid_removal_stats,
            'modified_schema_metadata': schema_metadata,
            'rebuild_mode': rebuild_mode,  # Track rebuild mode in output
            'fk_filtering_stats': {
                'fk_connected_pairs': len(connected_entity_pairs),
                'fk_relationships': len(fk_relationships),
                'shared_relationships_after_filtering': len(shared_relationships)
            }
        }

        # Summary logging
        logger.info("=== RELATIONSHIP MAPPING COMPLETE ===")
        if rebuild_mode:
            logger.info("🔄 REBUILD MODE: Generated all relationships from scratch")
        else:
            if invalid_removal_stats:
                logger.info(
                    f"Existing invalid relationships removed: {invalid_removal_stats.get('relationships_removed', 0)}")
            if conflict_fix_stats:
                logger.info(f"Existing conflicts fixed: {conflict_fix_stats.get('conflicts_fixed', 0)}")

        logger.info(f"New relationships detected: {len(unique_relationships)}")
        logger.info(f"  - FK relationships: {len(fk_relationships)}")
        logger.info(f"  - Shared field relationships (post-FK filtering): {len(shared_relationships)}")
        logger.info(
            f"  - FK-connected entity pairs excluded from shared field detection: {len(connected_entity_pairs)}")
        logger.info(f"New YAML definitions generated: {len(generated_yaml)}")

        return relationship_map

    @staticmethod
    def _build_connected_entities_map(fk_relationships: List[Dict[str, Any]]) -> Set[frozenset]:
        """
        Build a map of entity pairs that are already connected via FK relationships.

        This is used to filter out redundant shared field relationships between entities
        that already have a semantic FK connection.

        Args:
            fk_relationships: List of detected foreign key relationships

        Returns:
            Set of frozensets, each containing a pair of connected entity QNKs
        """
        connected_pairs = set()

        for fk_rel in fk_relationships:
            from_entity = fk_rel.get('from_entity')
            to_entity = fk_rel.get('to_entity')

            if from_entity and to_entity:
                # Use frozenset to handle bidirectional connections
                # (A,B) and (B,A) will be the same frozenset
                connected_pairs.add(frozenset([from_entity, to_entity]))

        logger.debug(f"Built connected entities map with {len(connected_pairs)} entity pairs")

        # Log some examples for debugging
        if connected_pairs and logger.isEnabledFor(logging.DEBUG):
            sample_pairs = list(connected_pairs)[:3]  # Show first 3
            for pair in sample_pairs:
                pair_list = list(pair)
                if len(pair_list) == 2:
                    entity1_name = pair_list[0].split('/')[-1] if '/' in pair_list[0] else pair_list[0]
                    entity2_name = pair_list[1].split('/')[-1] if '/' in pair_list[1] else pair_list[1]
                    logger.debug(f"Connected pair example: {entity1_name} ↔ {entity2_name}")

        return connected_pairs

    def _remove_existing_invalid_relationships(self, file_paths: List[str], entities_map: Dict[str, Dict]) -> Dict[
        str, Any]:
        """
        Remove existing relationships that target Commands or Command-only ObjectTypes.

        Scans all YAML files for existing relationships and validates their targets using
        the in-memory entities_map data structure.

        Args:
            file_paths: List of full file paths to scan
            entities_map: Map of entity qualified names to entity info with backing analysis

        Returns:
            Dictionary with removal statistics
        """
        from ..utils.yaml_utils import load_yaml_documents, save_yaml_documents

        logger.info(f"Scanning {len(file_paths)} files for existing relationships with invalid targets...")

        # Track removals and modifications
        relationships_removed = 0
        removal_details = []
        files_modified = set()

        # Process each file
        for file_path in file_paths:
            try:
                documents = load_yaml_documents(file_path)
                file_modified = False

                # Process documents in reverse order to safely remove items
                for doc_idx in range(len(documents) - 1, -1, -1):
                    doc = documents[doc_idx]

                    if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                        definition = doc.get('definition', {})
                        source_type = definition.get('sourceType', 'unknown')
                        rel_name = definition.get('name', 'unknown')
                        target_info = definition.get('target', {}).get('model', {})
                        target_name = target_info.get('name', '')

                        if not target_name:
                            logger.warning(f"Skipping relationship {source_type}.{rel_name} - no target name")
                            continue

                        # Check if target is valid using in-memory entities_map
                        if not self._is_valid_target_from_entities_map(target_name, entities_map):
                            # Invalid target - remove this relationship
                            logger.info(
                                f"REMOVING existing relationship: {source_type}.{rel_name} -> {target_name} (invalid target)")

                            # Remove the document
                            documents.pop(doc_idx)
                            file_modified = True
                            relationships_removed += 1

                            removal_details.append({
                                'source': source_type,
                                'name': rel_name,
                                'target': target_name,
                                'file': file_path,
                                'reason': 'Command or Command-only ObjectType target'
                            })
                        else:
                            logger.debug(
                                f"Keeping existing relationship: {source_type}.{rel_name} -> {target_name} (valid target)")

                # Save file if modified
                if file_modified:
                    save_yaml_documents(documents, file_path)
                    files_modified.add(file_path)
                    logger.debug(f"Saved modifications to {file_path}")

            except Exception as e:
                logger.error(f"Error processing file {file_path} for invalid relationship removal: {e}")

        # Log results
        if relationships_removed > 0:
            logger.info(
                f"Removed {relationships_removed} existing relationships with invalid targets from {len(files_modified)} files")
            for detail in removal_details:
                logger.debug(
                    f"  Removed: {detail['source']}.{detail['name']} -> {detail['target']} from {detail['file']}")
        else:
            logger.info("No existing relationships with invalid targets found")

        statistics = {
            'relationships_removed': relationships_removed,
            'removal_details': removal_details,
            'files_modified': len(files_modified),
            'files_scanned': len(file_paths)
        }

        logger.info(
            f"Invalid relationship removal complete: {relationships_removed} relationships removed from {len(files_modified)} files")
        return statistics

    @staticmethod
    def _is_valid_target_from_entities_map(target_name: str, entities_map: Dict[str, Dict]) -> bool:
        """
        Check if a target entity is valid using the in-memory entities_map.

        Args:
            target_name: Name of the target entity
            entities_map: Map of entity qualified names to entity info

        Returns:
            True if target is valid (Model or Model-backed ObjectType), False if invalid
        """
        # Find the target entity in entities_map by name (across all QNKs)
        target_entity = None
        for qnk, entity_info in entities_map.items():
            if entity_info.get('name') == target_name:
                target_entity = entity_info
                break

        if not target_entity:
            logger.warning(f"Target entity '{target_name}' not found in entities_map")
            return False

        # Use the same validation logic as other parts of the system
        entity_kind = target_entity.get('kind')
        queryable_via = target_entity.get('queryable_via', [])
        is_queryable = target_entity.get('is_queryable', False)

        # Must be queryable to be a valid target
        if not is_queryable:
            logger.debug(f"Target '{target_name}' is not queryable")
            return False

        # Commands cannot be relationship targets
        if entity_kind == 'Command':
            logger.debug(f"Target '{target_name}' is invalid: Command")
            return False

        # ObjectTypes must be Model-backed to be valid targets
        if entity_kind == 'ObjectType':
            if 'Model' not in queryable_via:
                logger.debug(f"Target '{target_name}' is invalid: Command-only ObjectType")
                return False
            else:
                logger.debug(f"Target '{target_name}' is valid: Model-backed ObjectType")
                return True

        # Models are always valid targets
        if entity_kind == 'Model':
            logger.debug(f"Target '{target_name}' is valid: Model")
            return True

        # For any other kind, default to false for safety
        logger.debug(f"Target '{target_name}' has unexpected kind '{entity_kind}' - rejecting for safety")
        return False

    def _remove_invalid_relationship_targets(self, generated_yaml: List[Dict[str, Any]],
                                             entities_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Final cleanup pass to remove relationships targeting Commands or Command-only ObjectTypes.

        This method uses the in-memory entities_map to validate relationship targets.

        Args:
            generated_yaml: List of generated relationship YAML definitions
            entities_map: Map of entity qualified names to entity info

        Returns:
            Cleaned list of relationship YAML definitions
        """
        if not generated_yaml:
            return generated_yaml

        cleaned_yaml = []
        removed_count = 0
        removed_details = []

        logger.info(f"Scanning {len(generated_yaml)} generated relationships for invalid targets...")

        for rel_item in generated_yaml:
            try:
                # Extract relationship details
                rel_def = rel_item.get('relationship_definition', {}).get('definition', {})
                source_type = rel_def.get('sourceType', 'unknown')
                rel_name = rel_def.get('name', 'unknown')
                target_info = rel_def.get('target', {}).get('model', {})
                target_name = target_info.get('name', '')
                file_path = rel_item.get('target_file_path', '')

                if not target_name:
                    logger.warning(f"Skipping relationship {source_type}.{rel_name} - missing target name")
                    cleaned_yaml.append(rel_item)
                    continue

                # Check if target is valid using in-memory entities_map
                if self._is_valid_target_from_entities_map(target_name, entities_map):
                    # Valid target - keep the relationship
                    cleaned_yaml.append(rel_item)
                else:
                    # Invalid target - remove the relationship
                    removed_count += 1
                    removed_details.append({
                        'source': source_type,
                        'name': rel_name,
                        'target': target_name,
                        'file': file_path,
                        'reason': 'Command or Command-only ObjectType target'
                    })
                    logger.info(f"REMOVED: {source_type}.{rel_name} -> {target_name} (Command/Command-only target)")

            except Exception as e:
                logger.warning(f"Error processing relationship for cleanup: {e}")
                # On error, keep the relationship to avoid losing valid ones
                cleaned_yaml.append(rel_item)

        # Log cleanup results
        if removed_count > 0:
            logger.info(f"Final cleanup: REMOVED {removed_count} relationships with invalid targets")
            for detail in removed_details:
                logger.debug(
                    f"  Removed: {detail['source']}.{detail['name']} -> {detail['target']} ({detail['reason']})")
        else:
            logger.info("Final cleanup: No invalid relationship targets found")

        logger.info(f"Final cleanup complete: {len(cleaned_yaml)} relationships remaining")
        return cleaned_yaml

    def _generate_relationship_yaml(self, relationships: List[Dict[str, Any]],
                                    entities_map: Dict[str, Dict],
                                    existing_signatures: Set[Tuple]) -> List[Dict[str, Any]]:
        """
        Generate YAML definitions for all relationships.

        ENHANCED: Now passes existing signatures for proper deduplication.
        """
        generated_yaml = []

        # Separate relationships by type
        fk_relationships = [r for r in relationships if r['relationship_type'].startswith('foreign_key')]
        shared_relationships = [r for r in relationships if r['relationship_type'] == 'shared_field']

        if fk_relationships:
            logger.info(f"Generating {len(fk_relationships)} foreign key relationships...")
            # Generate foreign key relationships (with existing signature awareness)
            fk_yaml = self.relationship_generator.generate_foreign_key_relationships(
                fk_relationships, entities_map, existing_signatures
            )
            logger.info(f"Generated {len(fk_yaml)} FK YAML definitions, now adding descriptions...")
            # Generate descriptions for the relationships
            fk_yaml = self.relationship_generator.generate_relationship_descriptions(fk_yaml, entities_map)
            logger.info(f"After description generation: {len(fk_yaml)} FK YAML definitions")
            generated_yaml.extend(fk_yaml)

        if shared_relationships:
            logger.info(f"Generating {len(shared_relationships)} shared field relationships...")
            # Generate shared field relationships (with existing signature awareness)
            shared_yaml = self.relationship_generator.generate_shared_field_relationships(
                shared_relationships, entities_map, existing_signatures
            )
            # Generate descriptions for the relationships
            shared_yaml = self.relationship_generator.generate_relationship_descriptions(shared_yaml, entities_map)
            generated_yaml.extend(shared_yaml)

        logger.info(f"Generated {len(generated_yaml)} total relationship YAML definitions for queryable entities")
        return generated_yaml

    def get_entity_relationships(self, entity_name: str, entity_kind: str,
                                 subgraph: Optional[str],
                                 relationship_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get all relationships for a specific entity.

        Only returns relationships that were actually created as YAML definitions,
        filtering out phantom relationships that were detected but not generated.
        Also ensures the entity itself is queryable.

        Args:
            entity_name: Name of the entity
            entity_kind: Kind of the entity
            subgraph: Subgraph of the entity
            relationship_map: The comprehensive relationship map

        Returns:
            List of relationships involving this entity
        """
        # Build qualified name for lookup
        entity_qnk = RelationshipMapper._build_qualified_name(entity_name, entity_kind, subgraph)

        if entity_qnk not in relationship_map.get('entities', {}):
            logger.warning(f"Entity {entity_qnk} not found in relationship map")
            return []

        # Check if this entity is queryable
        entity_info = relationship_map['entities'][entity_qnk]
        if not entity_info.get('is_queryable', False):
            logger.debug(f"Entity {entity_qnk} is not queryable - no relationships available")
            return []

        # Create a set of relationship signatures that were actually generated as YAML
        generated_signatures = set()
        for yaml_rel in relationship_map.get('generated_yaml', []):
            signature = self._extract_yaml_relationship_signature(yaml_rel, entity_qnk)
            if signature:
                generated_signatures.add(signature)

        relationships = []

        # Only include relationships that have corresponding YAML definitions
        for rel in relationship_map.get('relationships', []):
            # Check if this relationship was actually generated as YAML
            rel_signature = self._create_relationship_signature_from_detected(rel, entity_qnk)
            if rel_signature and rel_signature in generated_signatures:
                enriched_rel = self._enrich_relationship_for_entity(rel, entity_qnk, relationship_map)
                if enriched_rel:
                    relationships.append(enriched_rel)

        # Deduplicate and sort
        unique_relationships = self._deduplicate_entity_relationships(relationships)

        logger.debug(f"Entity {entity_qnk}: {len(unique_relationships)} actual relationships "
                     f"(filtered from {len([r for r in relationship_map.get('relationships', []) if entity_qnk in (r.get('from_entity'), r.get('to_entity'))])} detected)")

        return unique_relationships

    @staticmethod
    def _extract_yaml_relationship_signature(yaml_rel_item: Dict[str, Any], _entity_qnk: str) -> Optional[Tuple]:
        """
        Extract a signature from a generated YAML relationship for matching with detected relationships.

        Args:
            yaml_rel_item: Generated YAML relationship item
            _entity_qnk: Qualified name of the entity we're checking for

        Returns:
            Signature tuple for matching, or None if not relevant to this entity
        """
        try:
            # Get the relationship definition
            if 'relationship_definition' in yaml_rel_item:
                rel_def = yaml_rel_item['relationship_definition'].get('definition', {})
            else:
                rel_def = yaml_rel_item.get('definition', {})

            source_type = rel_def.get('sourceType')
            mapping = rel_def.get('mapping', [])

            if not source_type or not mapping:
                return None

            # Extract field mappings
            for m_item in mapping:
                if isinstance(m_item, dict):
                    source_fp = m_item.get('source', {}).get('fieldPath', [])
                    target_block = m_item.get('target', {})
                    target_fp = target_block.get('modelField', target_block.get('fieldPath', []))

                    source_field = source_fp[0].get('fieldName') if source_fp and isinstance(source_fp[0], dict) else (
                        source_fp[0] if source_fp else None)
                    target_field = target_fp[0].get('fieldName') if target_fp and isinstance(target_fp[0], dict) else (
                        target_fp[0] if target_fp else None)

                    if source_field and target_field:
                        # Create a signature that can match with detected relationships
                        # Format: (source_type, source_field, target_field, relationship_type)
                        return source_type.lower(), source_field.lower(), target_field.lower(), 'generated'

        except Exception as e:
            logger.debug(f"Could not extract YAML relationship signature: {e}")

        return None

    @staticmethod
    def _create_relationship_signature_from_detected(rel: Dict[str, Any], entity_qnk: str) -> Optional[Tuple]:
        """
        Create a signature from a detected relationship for matching with YAML.

        Args:
            rel: Detected relationship dictionary
            entity_qnk: Qualified name of the entity we're checking for

        Returns:
            Signature tuple for matching, or None if not relevant to this entity
        """
        try:
            from_entity = rel.get('from_entity')
            to_entity = rel.get('to_entity')

            # Only create signature if this entity is involved
            if entity_qnk not in (from_entity, to_entity):
                return None

            rel_type = rel.get('relationship_type', '')

            if rel_type == 'shared_field':
                # For shared field relationships
                shared_field = rel.get('shared_field', '')

                # Get entity names from QNKs
                from_name = from_entity.split('/')[-1] if from_entity else ''
                to_name = to_entity.split('/')[-1] if to_entity else ''

                # For the entity that matches entity_qnk, create appropriate signature
                if from_entity == entity_qnk:
                    return from_name.lower(), shared_field.lower(), shared_field.lower(), 'generated'
                elif to_entity == entity_qnk:
                    return to_name.lower(), shared_field.lower(), shared_field.lower(), 'generated'

            elif rel_type.startswith('foreign_key'):
                # For foreign key relationships
                from_field = rel.get('from_field', '')
                to_field = rel.get('to_field_name', '')

                # Get entity names from QNKs
                from_name = from_entity.split('/')[-1] if from_entity else ''

                # Create signature for the source entity (where the FK relationship is defined)
                if from_entity == entity_qnk:
                    return from_name.lower(), from_field.lower(), to_field.lower(), 'generated'

        except Exception as e:
            logger.debug(f"Could not create detected relationship signature: {e}")

        return None

    def format_relationships_for_prompt(self, relationships: List[Dict[str, Any]],
                                        relationship_map: Dict[str, Any],
                                        _current_entity_qnk: str) -> str:
        """
        Format relationships for inclusion in AI prompts.

        Args:
            relationships: List of relationships to format
            relationship_map: The comprehensive relationship map
            _current_entity_qnk: Qualified name of the current entity

        Returns:
            Formatted string describing the relationships
        """
        if not relationships:
            return ""

        # Group relationships by type and direction
        outgoing_fk = []
        incoming_fk = []
        shared_fields = []
        other_rels = []

        for rel in relationships:
            rel_type = rel.get('relationship_type', 'unknown')
            direction = rel.get('direction', 'unknown')

            if rel_type.startswith('foreign_key') and direction == 'outgoing':
                outgoing_fk.append(rel)
            elif rel_type.startswith('foreign_key') and direction == 'incoming':
                incoming_fk.append(rel)
            elif rel_type == 'shared_field':
                shared_fields.append(rel)
            else:
                other_rels.append(rel)

        # Format each group
        sections = []

        if outgoing_fk:
            section = self._format_outgoing_relationships(outgoing_fk, relationship_map)
            sections.append(f"Outgoing References (->):\n{section}")

        if incoming_fk:
            section = self._format_incoming_relationships(incoming_fk, relationship_map)
            sections.append(f"Incoming References (<-):\n{section}")

        if shared_fields:
            section = self._format_shared_field_relationships(shared_fields, relationship_map)
            sections.append(f"Shared Fields (<->):\n{section}")

        if other_rels:
            section = self._format_other_relationships(other_rels, relationship_map)
            sections.append(f"Other Relationships:\n{section}")

        return "\n\n".join(sections) if sections else ""

    @staticmethod
    def _build_qualified_name(entity_name: str, entity_kind: str,
                              subgraph: Optional[str]) -> str:
        """Build a qualified name for an entity."""
        if subgraph:
            return f"{subgraph}/{entity_kind}/{entity_name}"
        else:
            return f"{entity_kind}/{entity_name}"

    @staticmethod
    def _deduplicate_relationships(relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate relationships based on their characteristics."""
        unique_relationships = []
        seen_keys = set()

        for rel in relationships:
            # Create a unique key based on relationship characteristics
            if rel['relationship_type'] == 'shared_field':
                # For shared fields, key by entities and field name
                key = (
                    tuple(sorted([rel['from_entity'], rel['to_entity']])),
                    rel.get('shared_field'),
                    rel['relationship_type']
                )
            else:
                # For other relationships, key by from/to entities and fields
                key = (
                    rel['from_entity'],
                    rel.get('from_field'),
                    rel['to_entity'],
                    rel.get('to_field_name'),
                    rel['relationship_type']
                )

            if key not in seen_keys:
                seen_keys.add(key)
                unique_relationships.append(rel)

        logger.debug(f"Deduplicated {len(relationships)} to {len(unique_relationships)} relationships")
        return unique_relationships

    @staticmethod
    def _calculate_map_statistics(entities_map: Dict[str, Dict],
                                  relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate basic statistics for the relationship map."""
        queryable_entities = sum(1 for info in entities_map.values() if info.get('is_queryable', False))

        return {
            'total_entities': len(entities_map),
            'queryable_entities': queryable_entities,
            'non_queryable_entities': len(entities_map) - queryable_entities,
            'total_relationships': len(relationships),
            'fk_relationships': len([r for r in relationships if r['relationship_type'].startswith('foreign_key')]),
            'shared_field_relationships': len([r for r in relationships if r['relationship_type'] == 'shared_field']),
            'cross_subgraph_relationships': len([r for r in relationships if r.get('cross_subgraph', False)])
        }

    @staticmethod
    def _enrich_relationship_for_entity(rel: Dict[str, Any], entity_qnk: str,
                                        relationship_map: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Enrich a relationship with entity-specific context."""
        from_qnk = rel.get('from_entity')
        to_qnk = rel.get('to_entity')
        entities_map = relationship_map.get('entities', {})

        enriched_rel = rel.copy()

        # Determine direction relative to the current entity
        if from_qnk == entity_qnk:
            enriched_rel['direction'] = 'outgoing'
            # Add target entity info
            target_info = entities_map.get(to_qnk, {})
            enriched_rel.update({
                'to_entity_simple_name': target_info.get('name', '?'),
                'to_entity_kind': target_info.get('kind', '?'),
                'to_entity_subgraph': target_info.get('subgraph'),
                'to_entity_is_queryable': target_info.get('is_queryable', False)
            })
            return enriched_rel

        elif to_qnk == entity_qnk:
            enriched_rel['direction'] = 'incoming'
            # Add source entity info
            source_info = entities_map.get(from_qnk, {})
            enriched_rel.update({
                'from_entity_simple_name': source_info.get('name', '?'),
                'from_entity_kind': source_info.get('kind', '?'),
                'from_entity_subgraph': source_info.get('subgraph'),
                'from_entity_is_queryable': source_info.get('is_queryable', False)
            })
            return enriched_rel

        elif rel.get('relationship_type') == 'shared_field':
            # For shared fields, determine the other entity
            other_qnk = from_qnk if to_qnk == entity_qnk else to_qnk
            if other_qnk != entity_qnk:
                enriched_rel['direction'] = 'shared_field'
                enriched_rel['other_entity_qnk'] = other_qnk

                other_info = entities_map.get(other_qnk, {})
                enriched_rel.update({
                    'other_entity_simple_name': other_info.get('name', '?'),
                    'other_entity_kind': other_info.get('kind', '?'),
                    'other_entity_subgraph': other_info.get('subgraph'),
                    'other_entity_is_queryable': other_info.get('is_queryable', False)
                })
                return enriched_rel

        return None

    @staticmethod
    def _deduplicate_entity_relationships(relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate relationships for a specific entity."""
        unique_relationships = []
        seen_keys = set()

        for rel in relationships:
            # Create unique key based on relationship characteristics
            key_parts = [
                rel.get('relationship_type'),
                rel.get('direction'),
                rel.get('to_entity') if rel.get('direction') in ('outgoing', 'shared_field') else rel.get(
                    'from_entity'),
                rel.get('from_field'),
                rel.get('to_field_name'),
                rel.get('shared_field')
            ]

            key = tuple(key_parts)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_relationships.append(rel)

        return unique_relationships

    @staticmethod
    def _format_outgoing_relationships(relationships: List[Dict[str, Any]],
                                       _relationship_map: Dict[str, Any]) -> str:
        """Format outgoing foreign key relationships."""
        lines = []
        for rel in relationships:
            from_field = rel.get('from_field', '?')
            target_name = rel.get('to_entity_simple_name', '?')
            target_subgraph = rel.get('to_entity_subgraph', '')
            target_pk = rel.get('to_field_name', 'id')
            is_queryable = rel.get('to_entity_is_queryable', False)

            target_prefix = f"{target_subgraph}." if target_subgraph else ""
            queryable_indicator = " [Queryable]" if is_queryable else " [Not Queryable]"
            lines.append(f"- {from_field} -> {target_prefix}{target_name}.{target_pk}{queryable_indicator}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_incoming_relationships(relationships: List[Dict[str, Any]],
                                       _relationship_map: Dict[str, Any]) -> str:
        """Format incoming foreign key relationships."""
        lines = []
        for rel in relationships:
            source_name = rel.get('from_entity_simple_name', '?')
            source_subgraph = rel.get('from_entity_subgraph', '')
            source_fk = rel.get('from_field', '?')
            current_pk = rel.get('to_field_name', 'id')
            is_queryable = rel.get('from_entity_is_queryable', False)

            source_prefix = f"{source_subgraph}." if source_subgraph else ""
            queryable_indicator = " [Queryable]" if is_queryable else " [Not Queryable]"
            lines.append(f"- {source_prefix}{source_name}.{source_fk} <- {current_pk}{queryable_indicator}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_shared_field_relationships(relationships: List[Dict[str, Any]],
                                           _relationship_map: Dict[str, Any]) -> str:
        """Format shared field relationships."""
        lines = []
        for rel in relationships:
            shared_field = rel.get('shared_field', '?')
            other_name = rel.get('other_entity_simple_name', '?')
            other_subgraph = rel.get('other_entity_subgraph', '')
            is_queryable = rel.get('other_entity_is_queryable', False)

            other_prefix = f"{other_subgraph}." if other_subgraph else ""
            queryable_indicator = " [Queryable]" if is_queryable else " [Not Queryable]"
            lines.append(f"- {shared_field} <-> {other_prefix}{other_name}.{shared_field}{queryable_indicator}")

        return "\n".join(sorted(list(set(lines))))

    @staticmethod
    def _format_other_relationships(relationships: List[Dict[str, Any]],
                                    _relationship_map: Dict[str, Any]) -> str:
        """Format other types of relationships."""
        lines = []
        for rel in relationships:
            rel_type = rel.get('relationship_type', 'unknown')
            direction = rel.get('direction', 'unknown')

            if direction == 'outgoing':
                target_name = rel.get('to_entity_simple_name', '?')
                is_queryable = rel.get('to_entity_is_queryable', False)
                queryable_indicator = " [Queryable]" if is_queryable else " [Not Queryable]"
                lines.append(f"- {rel_type} -> {target_name}{queryable_indicator}")
            elif direction == 'incoming':
                source_name = rel.get('from_entity_simple_name', '?')
                is_queryable = rel.get('from_entity_is_queryable', False)
                queryable_indicator = " [Queryable]" if is_queryable else " [Not Queryable]"
                lines.append(f"- {rel_type} <- {source_name}{queryable_indicator}")
            else:
                lines.append(f"- {rel_type} relationship")

        return "\n".join(sorted(list(set(lines))))


def create_relationship_mapper() -> RelationshipMapper:
    """
    Create a RelationshipMapper instance.

    Returns:
        Configured RelationshipMapper instance
    """
    return RelationshipMapper()
