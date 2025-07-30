#!/usr/bin/env python3

"""
Directory processing for metadata bootstrap operations.
Handles the processing of entire directories containing multiple HML/YAML files.
"""

import logging
import os
import shutil
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

from .document_enhancer import DocumentEnhancer
from .file_processor import FileProcessor
from ..config import config
from ..relationships.detector import RelationshipDetector
from ..relationships.generator import RelationshipGenerator
from ..relationships.mapper import RelationshipMapper
from ..schema.domain_analyzer import DomainAnalyzer
from ..schema.metadata_collector import MetadataCollector
from ..utils.path_utils import FileCollector, get_file_stats
from ..utils.yaml_utils import save_yaml_documents

logger = logging.getLogger(__name__)


class DirectoryProcessor:
    """
    Processes entire directories of HML/YAML files through the enhancement workflow.

    This class orchestrates the processing of multiple files in a directory structure,
    handling cross-file relationships, domain analysis across the entire schema,
    and coordinated output generation.
    """

    def __init__(self, metadata_collector: MetadataCollector,
                 domain_analyzer: DomainAnalyzer,
                 relationship_detector: RelationshipDetector,
                 relationship_mapper: RelationshipMapper,
                 relationship_generator: RelationshipGenerator,
                 document_enhancer: DocumentEnhancer):
        """
        Initialize the directory processor with required components.

        Args:
            metadata_collector: Schema metadata collector
            domain_analyzer: Domain analysis component
            relationship_detector: Relationship detection component
            relationship_mapper: Relationship mapping component
            relationship_generator: Relationship generation component
            document_enhancer: Document enhancement component
        """
        self.metadata_collector = metadata_collector
        self.domain_analyzer = domain_analyzer
        self.relationship_detector = relationship_detector
        self.relationship_mapper = relationship_mapper
        self.relationship_generator = relationship_generator
        self.document_enhancer = document_enhancer

        # Create file processor for individual file handling
        self.file_processor = FileProcessor(
            metadata_collector, domain_analyzer, relationship_detector,
            relationship_mapper, relationship_generator, document_enhancer
        )

        # Processing state
        self.schema_metadata: Dict[str, Dict] = {}
        self.enhanced_documents_by_file: Dict[str, List] = {}
        self.generated_relationships: List[Dict] = []
        self.processing_statistics: Dict[str, Any] = {}

    def _scan_for_existing_relationships(self, file_paths: List[str]) -> None:
        """Scan all files for existing relationship definitions.
        FIXED: Skip scanning if rebuild_all_relationships is True."""

        # FIXED: Skip scanning entirely if we're rebuilding all relationships
        if config.rebuild_all_relationships:
            logger.info("🔄 REBUILD MODE: Skipping existing relationship scan - will generate fresh relationships")
            # Initialize empty signatures to force fresh generation
            self.file_processor.existing_relationships_signatures = set()
            return

        # Normal mode: scan for existing relationships
        existing_signatures = self.relationship_detector.scan_for_existing_relationships(file_paths)
        self.file_processor.existing_relationships_signatures = existing_signatures
        logger.info(f"Found {len(existing_signatures)} existing relationship signatures across all files")

    def _build_comprehensive_relationship_map(self, input_dir: str) -> Dict[str, Any]:
        """Build comprehensive relationship map from all collected metadata.
        FIXED: Clear existing relationship context in rebuild mode."""
        logger.info("Building comprehensive relationship map...")

        if not self.schema_metadata:
            logger.warning("No schema metadata available for relationship mapping")
            return {'entities': {}, 'relationships': [], 'generated_yaml': []}

        # FIXED: Clear relationship context if rebuilding
        if config.rebuild_all_relationships:
            logger.info("🔄 REBUILD MODE: Building relationships from scratch without existing context")
            # Clear any cached relationship data in the mapper
            if hasattr(self.relationship_mapper, 'clear_existing_context'):
                self.relationship_mapper.clear_existing_context()

        # Build relationship map using all collected metadata
        relationship_map = self.relationship_mapper.build_relationship_map(self.schema_metadata, input_dir)

        # Store generated relationships for later writing
        self.generated_relationships = relationship_map.get('generated_yaml', [])

        stats = relationship_map.get('statistics', {})

        if config.rebuild_all_relationships:
            logger.info(f"🔄 REBUILD MODE: Generated fresh relationship map: {stats.get('total_entities', 0)} entities, "
                        f"{stats.get('total_relationships', 0)} relationships, "
                        f"{len(self.generated_relationships)} YAML definitions generated")
        else:
            logger.info(f"Relationship map built: {stats.get('total_entities', 0)} entities, "
                        f"{stats.get('total_relationships', 0)} relationships, "
                        f"{len(self.generated_relationships)} YAML definitions generated")

        return relationship_map

    def process_directory(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """
        Process an entire directory of HML files.
        FIXED: Properly handle rebuild mode throughout the process.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path

        Returns:
            Dictionary with comprehensive processing results
        """
        logger.info(f"Starting directory processing: {input_dir} -> {output_dir}")

        # FIXED: Log rebuild mode status early
        if config.rebuild_all_relationships:
            logger.info("🔄 REBUILD MODE ACTIVE: Will generate all relationships from scratch")

        try:
            # Initialize processing
            os.makedirs(output_dir, exist_ok=True)

            # Collect and filter files
            processed_files, excluded_files = self._collect_and_filter_files(input_dir)

            if not processed_files:
                logger.warning("No files to process")
                return self._create_empty_result(input_dir, output_dir)

            # FIXED: Conditional relationship scanning based on rebuild mode
            self._scan_for_existing_relationships(processed_files)

            # Perform first pass: collect metadata and enhance structures
            self._perform_first_pass(processed_files, input_dir, output_dir)

            # FIXED: Build comprehensive relationship map with rebuild awareness
            relationship_map = self._build_comprehensive_relationship_map(input_dir)

            # Perform second pass: add relationship information and save files
            self._perform_second_pass(relationship_map, input_dir, output_dir)

            # FIXED: Write relationship definitions with proper rebuild handling
            self._write_relationship_definitions(output_dir)

            # Copy excluded files
            self._copy_excluded_files(excluded_files, input_dir, output_dir)

            # Calculate final statistics
            return self._calculate_final_statistics(
                input_dir, output_dir, processed_files, excluded_files
            )

        except Exception as e:
            logger.error(f"Error in directory processing: {e}")
            logger.debug("Full traceback:", exc_info=True)

            return {
                'success': False,
                'error': str(e),
                'input_dir': input_dir,
                'output_dir': output_dir
            }

    @staticmethod
    def _collect_and_filter_files(input_dir: str) -> Tuple[List[str], List[str]]:
        """Collect and filter HML files from input directory.
        FIXED: Proper pattern matching for excluded files."""
        import fnmatch

        # Use FileCollector to find and filter files
        collector = FileCollector(input_dir, config.file_glob)

        # OPTIMIZED: Build excluded files set once for O(1) lookups
        excluded_files_set = getattr(config, '_excluded_files_set', None)
        if excluded_files_set is None:
            excluded_files_list = getattr(config, 'excluded_files', [])
            excluded_files_set = {ef for ef in excluded_files_list if ef}  # Skip empty strings
            setattr(config, '_excluded_files_set', excluded_files_set)

        # Add exclusions from configuration using optimized set
        for excluded_file in excluded_files_set:
            collector.add_exclusion(excluded_file)

        # Collect all files
        all_files = collector.collect_files()

        # Separate processed and excluded files using proper pattern matching
        processed_files = []
        excluded_files = []

        for file_path in all_files:
            filename = os.path.basename(file_path)

            # FIXED: Use pattern matching instead of exact string matching
            is_excluded = False
            for pattern in excluded_files_set:
                if fnmatch.fnmatch(filename, pattern):
                    is_excluded = True
                    break

            if is_excluded:
                excluded_files.append(file_path)
            else:
                processed_files.append(file_path)

        logger.info(
            f"Found {len(all_files)} HML files: {len(processed_files)} to process, {len(excluded_files)} excluded")

        # Log subgraph summary
        subgraph_summary = collector.get_subgraph_summary(processed_files)
        logger.info(f"Files by subgraph: {subgraph_summary}")

        return processed_files, excluded_files

    def _clean_relationship_markers_for_save(self, documents: List[Dict]) -> List[Dict]:
        """
        Remove relationship markers from documents for disk writing.
        Keeps markers in memory but cleans them for file output.

        Args:
            documents: List of document dictionaries

        Returns:
            List of cleaned document dictionaries
        """
        import copy

        cleaned_docs = []

        for doc in documents:
            if doc is None:
                cleaned_docs.append(None)
                continue

            # Deep copy to avoid modifying the original
            cleaned_doc = copy.deepcopy(doc)

            # Recursively clean relationship markers
            self._clean_markers_recursive(cleaned_doc)

            cleaned_docs.append(cleaned_doc)

        return cleaned_docs

    def _clean_markers_recursive(self, obj):
        """Recursively clean relationship markers from nested structures."""
        import re

        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    # Remove the relationship markers and clean up whitespace
                    cleaned_value = re.sub(r'\s*\*\*\*ADD_RELATIONSHIPS\*\*\*\s*', '', value).strip()
                    obj[key] = cleaned_value
                elif isinstance(value, (dict, list)):
                    self._clean_markers_recursive(value)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._clean_markers_recursive(item)
                elif isinstance(item, str):
                    # Clean string items in lists too
                    item = re.sub(r'\s*\*\*\*ADD_RELATIONSHIPS\*\*\*\s*', '', item).strip()

    def _perform_first_pass(self, file_paths: List[str], input_dir: str, output_dir: str) -> None:
        """Perform first pass: metadata collection and structure enhancement."""
        logger.info("Starting first pass: metadata collection and structure enhancement")

        self.schema_metadata = {}
        self.enhanced_documents_by_file = {}

        for file_path in file_paths:
            try:
                logger.debug(f"First pass processing: {file_path}")

                # Process file using file processor's first pass logic
                results = self._process_file_first_pass(file_path, input_dir)

                if results:
                    rel_path, enhanced_docs, metadata = results
                    self.schema_metadata[rel_path] = metadata
                    self.enhanced_documents_by_file[rel_path] = enhanced_docs

                    # ADD SAVE CALL HERE:
                    output_path = os.path.join(output_dir, rel_path)  # Need to pass output_dir to this method
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    # Clean markers from descriptions before saving to disk
                    cleaned_docs = self._clean_relationship_markers_for_save(enhanced_docs)
                    save_yaml_documents(cleaned_docs, output_path)

                    logger.debug(f"Saved descriptions for: {output_path}")

            except Exception as e:
                logger.error(f"Error in first pass for {file_path}: {e}")
                logger.debug("Full traceback:", exc_info=True)

        total_entities = sum(len(meta.get('entities', [])) for meta in self.schema_metadata.values())
        logger.info(f"First pass complete: {len(self.schema_metadata)} files, {total_entities} entities")

    def _process_file_first_pass(self, file_path: str, input_dir: str) -> Optional[Tuple[str, List, Dict]]:
        """Process a single file in the first pass."""
        from ..utils.yaml_utils import load_yaml_documents
        from ..utils.path_utils import extract_subgraph_from_path

        try:
            # Load documents
            documents = load_yaml_documents(file_path)
            if not documents or all(d is None for d in documents):
                logger.warning(f"Empty or invalid YAML: {file_path}")
                return None

            # Extract file metadata
            subgraph = extract_subgraph_from_path(file_path)
            rel_path = os.path.relpath(file_path, input_dir)

            # Initialize metadata
            metadata = {
                'entities': [],
                'subgraph': subgraph,
                'file_path': rel_path
            }

            enhanced_documents = []

            # Process each document
            for doc in documents:
                if doc is not None:
                    # Extract domain terms
                    self.domain_analyzer.extract_domain_terms(doc)

                    # Collect schema metadata
                    self.metadata_collector.collect_schema_metadata(doc, metadata, subgraph)

                    # Enhance document structure
                    enhanced_doc = self.document_enhancer.enhance_yaml_structure(doc)
                    enhanced_documents.append(enhanced_doc)

                    # Update metadata with descriptions
                    self.metadata_collector.update_metadata_with_descriptions(enhanced_doc, metadata)
                else:
                    enhanced_documents.append(None)

            return rel_path, enhanced_documents, metadata

        except Exception as e:
            logger.error(f"Error processing file in first pass {file_path}: {e}")
            return None

    def _perform_second_pass(self, relationship_map: Dict[str, Any],
                             input_dir: str, output_dir: str) -> None:
        """Perform second pass: add relationships and save enhanced files."""
        logger.info("Starting second pass: adding relationships and saving files")

        for rel_path, enhanced_docs in self.enhanced_documents_by_file.items():
            try:
                # Extract subgraph from path
                from ..utils.path_utils import extract_subgraph_from_path
                full_path = os.path.join(input_dir, rel_path)
                subgraph = extract_subgraph_from_path(full_path)

                # Add relationship information to descriptions
                final_docs = self.document_enhancer.enhance_with_relationships(
                    enhanced_docs, relationship_map, subgraph
                )

                # Prepare output path
                output_path = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Save enhanced documents
                save_yaml_documents(final_docs, output_path)

                logger.debug(f"Second pass completed and saved: {output_path}")

            except Exception as e:
                logger.error(f"Error in second pass for {rel_path}: {e}")
                logger.debug("Full traceback:", exc_info=True)

        logger.info("Second pass complete: all files enhanced with relationships")

    def _write_relationship_definitions(self, output_dir: str) -> None:
        """Write generated relationship definitions to appropriate files."""
        from ..utils.yaml_utils import load_yaml_documents, save_yaml_documents
        from collections import defaultdict
        import os

        if not self.generated_relationships:
            logger.info("No relationship definitions to write")
            return

        logger.info(f"Writing {len(self.generated_relationships)} relationship definitions...")

        # Check if we're in rebuild mode
        rebuild_all = config.rebuild_all_relationships
        if rebuild_all:
            logger.info("REBUILD MODE: Writing all relationships without deduplication")

        # Group relationships by target file
        relationships_by_file = defaultdict(list)
        for rel_info in self.generated_relationships:
            file_path = rel_info.get('target_file_path')
            if file_path:
                relationships_by_file[file_path].append(rel_info['relationship_definition'])

        # Write relationships to each file
        written_count = 0
        for file_rel_path, relationships in relationships_by_file.items():
            try:
                output_path = os.path.join(output_dir, file_rel_path)

                # Load existing documents
                existing_documents = []
                if os.path.exists(output_path):
                    try:
                        existing_documents = load_yaml_documents(output_path)
                    except Exception as e:
                        logger.error(f"Could not read existing file {output_path}: {e}")
                        existing_documents = []

                # Filter out None documents
                final_documents = [doc for doc in existing_documents if doc is not None]

                # REBUILD MODE: Remove all existing relationships first
                if rebuild_all:
                    # Remove all existing Relationship documents
                    final_documents = [doc for doc in final_documents
                                       if not (isinstance(doc, dict) and doc.get('kind') == 'Relationship')]
                    logger.debug(f"REBUILD MODE: Cleared existing relationships from {output_path}")

                    # Add all new relationships without deduplication
                    final_documents.extend(relationships)
                    written_count += len(relationships)
                    logger.debug(f"REBUILD MODE: Added {len(relationships)} new relationships to {output_path}")

                    # Save updated documents
                    save_yaml_documents(final_documents, output_path)
                else:
                    # NORMAL MODE: Deduplicate and append new relationships
                    unique_relationships = self._deduplicate_relationships_for_file(
                        relationships, final_documents
                    )

                    if unique_relationships:
                        final_documents.extend(unique_relationships)
                        written_count += len(unique_relationships)
                        logger.debug(
                            f"NORMAL MODE: Appended {len(unique_relationships)} unique relationships to {output_path}")

                        # Save updated documents
                        save_yaml_documents(final_documents, output_path)

            except Exception as e:
                logger.error(f"Error writing relationships to {file_rel_path}: {e}")

        if rebuild_all:
            logger.info(
                f"REBUILD MODE: Successfully wrote {written_count} relationship definitions (replaced all existing)")
        else:
            logger.info(f"NORMAL MODE: Successfully wrote {written_count} new relationship definitions")

    @staticmethod
    def _deduplicate_relationships_for_file(new_relationships: List[Dict],
                                            existing_documents: List[Dict]) -> List[Dict]:
        """Deduplicate relationships against existing documents in the file."""
        unique_relationships = []

        # Extract existing relationship signatures from current file
        existing_signatures = set()
        for doc in existing_documents:
            if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                signature = RelationshipGenerator.extract_relationship_signature(doc)
                if signature:
                    existing_signatures.add(signature)

        # Check each new relationship for duplicates
        for rel_def in new_relationships:
            signature = RelationshipGenerator.extract_relationship_signature(rel_def)

            if signature and signature not in existing_signatures:
                unique_relationships.append(rel_def)
                existing_signatures.add(signature)
            elif not signature:
                # Include relationships we can't create signatures for
                logger.warning(f"Could not create signature for relationship, including anyway")
                unique_relationships.append(rel_def)
            else:
                logger.debug(f"Skipping duplicate relationship: {rel_def.get('definition', {}).get('name', 'unnamed')}")

        return unique_relationships

    @staticmethod
    def _copy_excluded_files(excluded_files: List[str],
                             input_dir: str, output_dir: str) -> None:
        """Copy excluded files to output directory without processing."""
        if not excluded_files:
            return

        logger.info(f"Copying {len(excluded_files)} excluded files...")

        for file_path in excluded_files:
            try:
                rel_path = os.path.relpath(file_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)

                # Skip if input and output are the same
                if os.path.abspath(file_path) == os.path.abspath(output_path):
                    logger.debug(f"Skipping copy (same path): {file_path}")
                    continue

                # Create output directory and copy file
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(file_path, output_path)

                logger.debug(f"Copied excluded file: {output_path}")

            except Exception as e:
                logger.error(f"Error copying excluded file {file_path}: {e}")

    @staticmethod
    def _create_empty_result(input_dir: str, output_dir: str) -> Dict[str, Any]:
        """Create result dictionary for empty processing."""
        return {
            'success': True,
            'input_dir': input_dir,
            'output_dir': output_dir,
            'files_processed': 0,
            'files_excluded': 0,
            'entities_found': 0,
            'relationships_generated': 0,
            'warning': 'No files found to process'
        }

    def _calculate_final_statistics(self, input_dir: str, output_dir: str,
                                    processed_files: List[str],
                                    excluded_files: List[str]) -> Dict[str, Any]:
        """Calculate comprehensive final statistics."""
        # Basic file statistics
        stats = {
            'success': True,
            'input_dir': input_dir,
            'output_dir': output_dir,
            'files_processed': len(processed_files),
            'files_excluded': len(excluded_files),
            'total_files_found': len(processed_files) + len(excluded_files)
        }

        # Entity statistics
        total_entities = 0
        entities_by_kind = defaultdict(int)
        entities_by_subgraph = defaultdict(int)

        for metadata in self.schema_metadata.values():
            entities = metadata.get('entities', [])
            total_entities += len(entities)

            for entity in entities:
                kind = entity.get('kind', 'Unknown')
                if isinstance(kind, str):
                    subgraph = entity.get('subgraph', 'None')
                    entities_by_kind[kind] += 1
                    entities_by_subgraph[subgraph] += 1

        stats.update({
            'entities_found': total_entities,
            'entities_by_kind': dict(entities_by_kind),
            'entities_by_subgraph': dict(entities_by_subgraph)
        })

        # Relationship statistics
        stats.update({
            'relationships_generated': len(self.generated_relationships),
            'relationship_files_modified': len(set(
                rel.get('target_file_path') for rel in self.generated_relationships
                if rel.get('target_file_path')
            ))
        })

        # Domain analysis statistics
        if hasattr(self.domain_analyzer, 'get_domain_summary'):
            stats['domain_analysis'] = self.domain_analyzer.get_domain_summary()

        # File statistics
        if processed_files:
            file_stats = get_file_stats(processed_files)
            stats['file_statistics'] = file_stats

        # Processing performance
        stats['processing_summary'] = {
            'files_with_entities': len([m for m in self.schema_metadata.values() if m.get('entities')]),
            'files_with_relationships': len([
                rel.get('target_file_path') for rel in self.generated_relationships
            ]),
            'cross_subgraph_relationships': len([
                rel for rel in self.generated_relationships
                if 'subgraph' in rel.get('relationship_definition', {}).get('definition', {}).get('target', {}).get(
                    'model', {})
            ])
        }

        return stats


def create_directory_processor(metadata_collector: MetadataCollector,
                               domain_analyzer: DomainAnalyzer,
                               relationship_detector: RelationshipDetector,
                               relationship_mapper: RelationshipMapper,
                               relationship_generator: RelationshipGenerator,
                               document_enhancer: DocumentEnhancer) -> DirectoryProcessor:
    """
    Create a DirectoryProcessor instance with all required components.

    Args:
        metadata_collector: Schema metadata collector
        domain_analyzer: Domain analysis component
        relationship_detector: Relationship detection component
        relationship_mapper: Relationship mapping component
        relationship_generator: Relationship generation component
        document_enhancer: Document enhancement component

    Returns:
        Configured DirectoryProcessor instance
    """
    return DirectoryProcessor(
        metadata_collector, domain_analyzer, relationship_detector,
        relationship_mapper, relationship_generator, document_enhancer
    )
