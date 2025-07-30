#!/usr/bin/env python3

"""
Single file processing for metadata bootstrap operations.
Handles the complete processing workflow for individual HML/YAML files.
"""

import logging
import os
import shutil
from typing import Dict, List, Any, Optional, Tuple, Set

from .document_enhancer import DocumentEnhancer
from ..config import config
from ..relationships.detector import RelationshipDetector
from ..relationships.generator import RelationshipGenerator
from ..relationships.mapper import RelationshipMapper
from ..schema.domain_analyzer import DomainAnalyzer
from ..schema.metadata_collector import MetadataCollector
from ..utils.path_utils import extract_subgraph_from_path, create_directory_structure
from ..utils.yaml_utils import load_yaml_documents, save_yaml_documents

logger = logging.getLogger(__name__)


class FileProcessor:
    """
    Processes individual HML/YAML files through the complete enhancement workflow.

    This class orchestrates the full processing pipeline for a single file:
    - Loading and parsing YAML documents
    - Collecting schema metadata
    - Detecting relationships
    - Enhancing documents with descriptions
    - Adding relationship information
    - Saving enhanced documents
    """

    def __init__(self, metadata_collector: MetadataCollector,
                 domain_analyzer: DomainAnalyzer,
                 relationship_detector: RelationshipDetector,
                 relationship_mapper: RelationshipMapper,
                 relationship_generator: RelationshipGenerator,
                 document_enhancer: DocumentEnhancer):
        """
        Initialize the file processor with required components.

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

        # Processing state
        self.existing_relationships_signatures: Set[Tuple] = set()
        self.generated_relationships: List[Dict[str, Any]] = []

    def process_file(self, input_file: str, output_file: str, input_dir: str) -> Dict[str, Any]:
        """
        Process a single file through the complete enhancement workflow.

        Args:
            input_dir:
            input_file: Path to input HML/YAML file
            output_file: Path to output enhanced file

        Returns:
            Dictionary with processing results and statistics
        """
        logger.info(f"Processing file: {input_file} -> {output_file}")

        try:
            # Determine base directory for relationship scanning
            base_dir = os.path.dirname(input_file) if os.path.isabs(input_file) else "."
            if not base_dir:
                base_dir = "."

            # Initialize processing state
            self.generated_relationships = []

            # Load and validate documents
            documents = self._load_and_validate_documents(input_file)
            if not documents:
                return self._handle_empty_file(input_file, output_file)

            # Scan for existing relationships
            self._scan_for_existing_relationships([input_file])

            # Extract basic file information
            subgraph = extract_subgraph_from_path(input_file)
            relative_path = os.path.relpath(input_file, base_dir)

            # Perform first pass: collect metadata and enhance structure
            enhanced_documents, metadata = self._perform_first_pass(
                documents, relative_path, subgraph
            )

            # Build relationship map if we have entities
            relationship_map = None
            if metadata.get('entities'):
                relationship_map = self._build_single_file_relationship_map(metadata, relative_path, input_dir)

            # Perform second pass: add relationship information
            final_documents = self._perform_second_pass(
                enhanced_documents, relationship_map, subgraph
            )

            # Generate and append new relationships
            final_documents = self._append_generated_relationships(
                final_documents, relative_path
            )

            # Save enhanced documents
            self._save_enhanced_documents(final_documents, output_file)

            # Calculate and return statistics
            return self._calculate_processing_statistics(documents, final_documents, metadata)

        except Exception as e:
            logger.error(f"Error processing file {input_file}: {e}")
            logger.debug(f"Full traceback:", exc_info=True)

            # Attempt to copy original file on error
            self._copy_original_on_error(input_file, output_file)

            return {
                'success': False,
                'error': str(e),
                'input_file': input_file,
                'output_file': output_file
            }

    @staticmethod
    def _load_and_validate_documents(input_file: str) -> List[Dict]:
        """Load and validate YAML documents from input file."""
        try:
            documents = load_yaml_documents(input_file)

            # Filter out None documents
            valid_documents = [doc for doc in documents if doc is not None]

            if not valid_documents:
                logger.warning(f"No valid documents found in {input_file}")
                return []

            logger.debug(f"Loaded {len(valid_documents)} valid documents from {input_file}")
            return valid_documents

        except Exception as e:
            logger.error(f"Failed to load documents from {input_file}: {e}")
            raise

    @staticmethod
    def _handle_empty_file(input_file: str, output_file: str) -> Dict[str, Any]:
        """Handle the case where input file is empty or invalid."""
        logger.warning(f"Empty or invalid YAML file: {input_file}")

        # Copy original file if different from output
        if os.path.abspath(input_file) != os.path.abspath(output_file):
            create_directory_structure(output_file)
            shutil.copy2(input_file, output_file)
            logger.info(f"Copied empty file: {output_file}")

        return {
            'success': True,
            'input_file': input_file,
            'output_file': output_file,
            'documents_processed': 0,
            'descriptions_added': 0,
            'relationships_generated': 0,
            'warning': 'File was empty or invalid'
        }

    def _scan_for_existing_relationships(self, file_paths: List[str]) -> None:
        """Scan files for existing relationship definitions."""
        self.existing_relationships_signatures = self.relationship_detector.scan_for_existing_relationships(file_paths)
        logger.debug(f"Found {len(self.existing_relationships_signatures)} existing relationship signatures")

    def _perform_first_pass(self, documents: List[Dict], file_path: str,
                            subgraph: Optional[str]) -> Tuple[List[Dict], Dict]:
        """Perform first pass: metadata collection and structure enhancement."""
        # Initialize metadata
        metadata = {
            'entities': [],
            'file_path': file_path,
            'subgraph': subgraph
        }

        enhanced_documents = []

        for doc_index, doc in enumerate(documents):
            # Log first document info
            if doc_index == 0 and isinstance(doc, dict) and 'kind' in doc:
                doc_name = doc.get('definition', {}).get('name', doc.get('name', 'unnamed'))
                logger.debug(f"Processing document {doc_index}: kind={doc.get('kind')}, name={doc_name}")

            # Extract domain terms
            self.domain_analyzer.extract_domain_terms(doc)

            # Collect schema metadata
            entity_count_before = len(metadata['entities'])
            self.metadata_collector.collect_schema_metadata(doc, metadata, subgraph)

            if len(metadata['entities']) > entity_count_before:
                entities_added = len(metadata['entities']) - entity_count_before
                logger.debug(f"Document {doc_index}: Added {entities_added} entities")

            # Enhance document structure
            enhanced_doc = self.document_enhancer.enhance_yaml_structure(doc)
            enhanced_documents.append(enhanced_doc)

            # Update metadata with generated descriptions
            self.metadata_collector.update_metadata_with_descriptions(enhanced_doc, metadata)

        if metadata['entities']:
            logger.info(f"First pass complete: {len(metadata['entities'])} entities collected")

        return enhanced_documents, metadata

    def _build_single_file_relationship_map(self, metadata: Dict, file_path: str, input_dir: str) -> Dict[str, Any]:
        """Build relationship map for single file processing."""
        # Create schema metadata in the expected format
        schema_metadata = {file_path: metadata}

        # Build comprehensive relationship map
        relationship_map = self.relationship_mapper.build_relationship_map(schema_metadata, input_dir)

        # Store generated relationships for later appending
        self.generated_relationships = relationship_map.get('generated_yaml', [])

        logger.debug(f"Built relationship map with {len(relationship_map.get('relationships', []))} relationships")
        return relationship_map

    def _perform_second_pass(self, enhanced_documents: List[Dict],
                             relationship_map: Optional[Dict[str, Any]],
                             subgraph: Optional[str]) -> List[Dict]:
        """Perform second pass: add relationship information to descriptions."""
        if not relationship_map:
            # No relationships to add, just clean up markers
            return self._clean_relationship_markers(enhanced_documents)

        final_documents = self.document_enhancer.enhance_with_relationships(
            enhanced_documents, relationship_map, subgraph
        )

        logger.debug("Second pass complete: relationship information added")
        return final_documents

    @staticmethod
    def _clean_relationship_markers(documents: List[Dict]) -> List[Dict]:
        """Clean relationship markers from documents when no relationships are found."""

        def clean_markers(data):
            if isinstance(data, dict):
                # Clean description markers
                if 'description' in data:
                    desc = data['description']
                    # FIX: Add type check
                    if isinstance(desc, str) and config.relationship_marker in desc:
                        data['description'] = desc.replace(f"\n{config.relationship_marker}", "").replace(
                            config.relationship_marker, "")

                if isinstance(data.get('definition'), dict) and 'description' in data['definition']:
                    desc = data['definition']['description']
                    # FIX: Add type check
                    if isinstance(desc, str) and config.relationship_marker in desc:
                        data['definition']['description'] = desc.replace(f"\n{config.relationship_marker}", "").replace(
                            config.relationship_marker, "")

                # Recurse into nested structures
                for value in data.values():
                    clean_markers(value)
            elif isinstance(data, list):
                for item in data:
                    clean_markers(item)

            return data

        return [clean_markers(doc) for doc in documents]

    def _append_generated_relationships(self, documents: List[Dict],
                                        file_path: str) -> List[Dict]:
        """Append generated relationship definitions to documents."""
        if not self.generated_relationships:
            return documents

        # Filter relationships that belong to this file
        relationships_for_file = [
            rel['relationship_definition']
            for rel in self.generated_relationships
            if rel.get('target_file_path') == file_path
        ]

        if not relationships_for_file:
            return documents

        # Deduplicate against existing relationships
        unique_relationships = self._deduplicate_new_relationships(relationships_for_file)

        if unique_relationships:
            documents.extend(unique_relationships)
            logger.info(f"Appended {len(unique_relationships)} relationship definitions")

        return documents

    def _deduplicate_new_relationships(self, new_relationships: List[Dict]) -> List[Dict]:
        """Remove duplicate relationships from new relationships list."""
        unique_relationships = []
        seen_signatures = self.existing_relationships_signatures.copy()

        for rel_def in new_relationships:
            # Extract signature
            signature = RelationshipGenerator.extract_relationship_signature(rel_def)

            if signature and signature not in seen_signatures:
                unique_relationships.append(rel_def)
                seen_signatures.add(signature)
            elif not signature:
                # If we can't create a signature, include with warning
                logger.warning(f"Could not create signature for relationship, including anyway")
                unique_relationships.append(rel_def)

        logger.debug(f"Deduplicated {len(new_relationships)} to {len(unique_relationships)} relationships")
        return unique_relationships

    @staticmethod
    def _save_enhanced_documents(documents: List[Dict], output_file: str) -> None:
        """Save enhanced documents to output file."""
        try:
            save_yaml_documents(documents, output_file, create_dirs=True)
            logger.debug(f"Saved {len(documents)} enhanced documents to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save enhanced documents to {output_file}: {e}")
            raise

    @staticmethod
    def _copy_original_on_error(input_file: str, output_file: str) -> None:
        """Copy original file to output location on processing error."""
        if os.path.abspath(input_file) != os.path.abspath(output_file):
            try:
                create_directory_structure(output_file)
                shutil.copy2(input_file, output_file)
                logger.info(f"Copied original file due to processing error: {output_file}")
            except Exception as copy_error:
                logger.error(f"Could not copy original file {input_file}: {copy_error}")

    def _calculate_processing_statistics(self, original_documents: List[Dict],
                                         final_documents: List[Dict],
                                         metadata: Dict) -> Dict[str, Any]:
        """Calculate comprehensive processing statistics."""
        stats = {
            'success': True,
            'input_file': metadata.get('file_path', ''),
            'output_file': '',  # Will be set by caller
            'documents_processed': len(original_documents),
            'final_document_count': len(final_documents),
            'entities_found': len(metadata.get('entities', [])),
            'relationships_generated': len(self.generated_relationships),
            'subgraph': metadata.get('subgraph'),
            'entity_summary': {},
            'enhancement_stats': {}
        }

        # Entity summary by kind
        entities = metadata.get('entities', [])
        for entity in entities:
            kind = entity.get('kind', 'Unknown')
            stats['entity_summary'][kind] = stats['entity_summary'].get(kind, 0) + 1

        # Enhancement statistics
        if original_documents and final_documents:
            stats['enhancement_stats'] = self.document_enhancer.get_enhancement_statistics(
                original_documents[0] if original_documents else {},
                final_documents[0] if final_documents else {}
            )

        # Relationship statistics
        if hasattr(self.relationship_mapper, 'get_generation_statistics'):
            stats['relationship_stats'] = self.relationship_mapper.get_generation_statistics()

        return stats

    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current processing state.

        Returns:
            Dictionary with processing summary information
        """
        return {
            'existing_relationships_found': len(self.existing_relationships_signatures),
            'relationships_generated': len(self.generated_relationships),
            'domain_analyzer_state': self.domain_analyzer.get_domain_summary() if hasattr(self.domain_analyzer,
                                                                                          'get_domain_summary') else {},
            'metadata_collector_state': 'ready'
        }


def create_file_processor(metadata_collector: MetadataCollector,
                          domain_analyzer: DomainAnalyzer,
                          relationship_detector: RelationshipDetector,
                          relationship_mapper: RelationshipMapper,
                          relationship_generator: RelationshipGenerator,
                          document_enhancer: DocumentEnhancer) -> FileProcessor:
    """
    Create a FileProcessor instance with all required components.

    Args:
        metadata_collector: Schema metadata collector
        domain_analyzer: Domain analysis component
        relationship_detector: Relationship detection component
        relationship_mapper: Relationship mapping component
        relationship_generator: Relationship generation component
        document_enhancer: Document enhancement component

    Returns:
        Configured FileProcessor instance
    """
    return FileProcessor(
        metadata_collector, domain_analyzer, relationship_detector,
        relationship_mapper, relationship_generator, document_enhancer
    )
