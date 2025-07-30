#!/usr/bin/env python3

"""
Main MetadataBootstrapper class for orchestrating the metadata enhancement process.
This is a simplified version that delegates to specialized components.
"""

import logging
from typing import Dict, List, Set

from .ai.description_generator import DescriptionGenerator
from .config import config
from .processors.directory_processor import DirectoryProcessor
from .processors.document_enhancer import DocumentEnhancer
from .processors.file_processor import FileProcessor
from .relationships.detector import RelationshipDetector
from .relationships.generator import RelationshipGenerator
from .relationships.mapper import RelationshipMapper
from .schema.domain_analyzer import DomainAnalyzer
from .schema.metadata_collector import MetadataCollector

logger = logging.getLogger(__name__)


class MetadataBootstrapper:
    """
    Main class for bootstrapping metadata in YAML/HML schema files.

    Orchestrates the process of adding AI-generated descriptions and
    detecting/generating relationships between schema elements.
    """

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the MetadataBootstrapper.

        Args:
            api_key: Anthropic API key
            **kwargs: Additional configuration overrides
        """
        self.api_key = api_key
        self.model = kwargs.get('model') or config.model

        # Apply any configuration overrides
        self._apply_config_overrides(kwargs)

        # Initialize components
        self.description_generator = DescriptionGenerator(api_key, self.model)
        self.metadata_collector = MetadataCollector()
        self.domain_analyzer = DomainAnalyzer()
        self.relationship_detector = RelationshipDetector()
        self.relationship_generator = RelationshipGenerator()
        self.document_enhancer = DocumentEnhancer(self.description_generator)

        # Create relationship mapper with shared instances (fixes the double initialization)
        self.relationship_mapper = RelationshipMapper(
            relationship_detector=self.relationship_detector,
            relationship_generator=self.relationship_generator,
            metadata_collector=self.metadata_collector
        )

        # State tracking
        self.good_examples: Dict = {}
        self.detected_domains: Set[str] = set()
        self.generated_relationships_yaml: List = []
        self.existing_relationships_signatures: Set = set()

    @staticmethod
    def _apply_config_overrides(overrides: Dict):
        """Apply configuration overrides from constructor arguments."""
        override_mapping = {
            'field_tokens': 'field_tokens',
            'kind_tokens': 'kind_tokens',
            'field_max_length': 'field_desc_max_length',
            'kind_max_length': 'kind_desc_max_length',
            'excluded_files': 'excluded_files',
            'excluded_kinds': 'excluded_kinds',
            'generic_fields': 'generic_fields',
            'domain_identifiers': 'domain_identifiers',
            'fk_templates_str': 'fk_templates_string',
            'relationships_only': 'relationships_only',
            'input_dir': 'input_dir',
            'output_dir': 'output_dir',
            'system_prompt': 'system_prompt',
        }

        for arg_name, config_attr in override_mapping.items():
            if arg_name in overrides and overrides[arg_name] is not None:
                setattr(config, config_attr, overrides[arg_name])

    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """
        Process an entire directory of HML files.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
        """
        logger.info(f"Processing directory: {input_dir} -> {output_dir}")

        # Delegate to directory processor with shared instances
        directory_processor = DirectoryProcessor(
            self.metadata_collector,
            self.domain_analyzer,
            self.relationship_detector,
            self.relationship_mapper,  # Use the shared mapper instance
            self.relationship_generator,
            self.document_enhancer
        )

        directory_processor.process_directory(input_dir, output_dir)

        logger.info("Directory processing completed!")

    def process_file(self, input_file: str, output_file: str, input_dir: str) -> None:
        """
        Process a single HML file.

        Args:
            input_dir:
            input_file: Input file path
            output_file: Output file path
        """
        logger.info(f"Processing single file: {input_file} -> {output_file}")

        # Delegate to file processor with shared instances
        file_processor = FileProcessor(
            self.metadata_collector,
            self.domain_analyzer,
            self.relationship_detector,
            self.relationship_mapper,  # Use the shared mapper instance
            self.relationship_generator,
            self.document_enhancer
        )

        file_processor.process_file(input_file, output_file, input_dir)

        logger.info("File processing completed!")

    def extract_domain_terms(self, yaml_data: Dict) -> None:
        """
        Extract domain-specific terms from YAML data.

        Args:
            yaml_data: YAML data to analyze
        """
        self.domain_analyzer.extract_domain_terms(yaml_data)

    @staticmethod
    def should_generate_description(existing_description: str) -> bool:
        """
        Check if we should generate/regenerate a description.

        Args:
            existing_description: Current description content

        Returns:
            True if description should be generated
        """
        if not existing_description or not existing_description.strip():
            return True
        if existing_description.strip().startswith('!'):
            return True
        return False

    @staticmethod
    def clean_description_for_regeneration(existing_description: str) -> str:
        """
        Clean description for regeneration by removing '!' prefix if present.

        Args:
            existing_description: Description to clean

        Returns:
            Cleaned description
        """
        if not existing_description:
            return ""
        cleaned = existing_description.strip()
        if cleaned.startswith('!'):
            return cleaned[1:].strip()
        return cleaned

    def can_have_description(self, data: Dict, context: Dict = None) -> bool:
        """
        Check if a schema element can have a description.

        Args:
            data: Schema element data
            context: Element context information

        Returns:
            True if element can have a description
        """
        return self.document_enhancer.can_have_description(data, context)

    def generate_description(self, element_data: Dict, context: Dict) -> str:
        """
        Generate an appropriate description for a schema element.

        Args:
            element_data: Schema element data
            context: Element context information

        Returns:
            Generated description
        """
        element_kind = context.get('kind')

        # Determine if this is a field or a kind
        is_field_like = ('name' in element_data and
                         ('type' in element_data or 'outputType' in element_data) and
                         not element_kind)

        if is_field_like:
            return self.description_generator.generate_field_description(element_data, context)
        elif element_kind in config.opendd_kinds:
            return self.description_generator.generate_kind_description(element_data, context)
        else:
            return ""

    def get_statistics(self) -> Dict:
        """
        Get processing statistics.

        Returns:
            Dictionary containing processing statistics
        """
        return {
            'detected_domains': list(self.detected_domains),
            'relationships_generated': len(self.generated_relationships_yaml),
            'good_examples_collected': len(self.good_examples)
        }


# Convenience functions for backward compatibility
def create_bootstrapper(api_key: str, **kwargs) -> MetadataBootstrapper:
    """
    Create a MetadataBootstrapper instance with the given configuration.

    Args:
        api_key: Anthropic API key
        **kwargs: Additional configuration

    Returns:
        Configured MetadataBootstrapper instance
    """
    return MetadataBootstrapper(api_key, **kwargs)
