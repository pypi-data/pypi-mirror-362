#!/usr/bin/env python3

"""
Main entry point for Metadata Bootstrap CLI application.
Handles argument parsing, configuration, and application orchestration.
"""

import argparse
import logging
import os
import traceback
from argparse import Namespace
from typing import Optional

# Handle both direct execution and module execution
try:
    from .config import config
    from .bootstrapper import MetadataBootstrapper
except ImportError:
    # Handle direct execution (python main.py)
    import sys
    from pathlib import Path

    # Add the parent directory to Python path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))

    from .config import config
    from .bootstrapper import MetadataBootstrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Bootstrap metadata for HML/YAML schema files with AI-generated descriptions and relationships',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process entire directory
  python -m metadata_bootstrap --input-dir ./input --output-dir ./output --api-key YOUR_KEY

  # Process single file
  python -m metadata_bootstrap --input-file schema.hml --output-file enhanced.hml --api-key YOUR_KEY

  # Use environment variables for configuration
  export ANTHROPIC_API_KEY=your_key
  export METADATA_BOOTSTRAP_INPUT_DIR=./input
  export METADATA_BOOTSTRAP_OUTPUT_DIR=./output
  python -m metadata_bootstrap
        """
    )

    # Input/Output options
    io_group = parser.add_argument_group('Input/Output')
    io_group.add_argument('--input-dir', help='Input directory containing HML files')
    io_group.add_argument('--output-dir', help='Output directory for enhanced files')
    io_group.add_argument('--input-file', help='Single input HML file')
    io_group.add_argument('--output-file', help='Single output HML file')

    # API Configuration
    api_group = parser.add_argument_group('API Configuration')
    api_group.add_argument('--api-key', help='Anthropic API key')
    api_group.add_argument('--model', help='Anthropic model to use')
    api_group.add_argument('--use-case', help='General use case description for better context')
    api_group.add_argument('--system-prompt', help='System prompt for AI description generation')

    # Generation Configuration
    gen_group = parser.add_argument_group('Generation Configuration')
    gen_group.add_argument('--field-tokens', type=int, help='Max tokens for field descriptions')
    gen_group.add_argument('--kind-tokens', type=int, help='Max tokens for kind descriptions')
    gen_group.add_argument('--field-max-length', type=int, help='Max character length for field descriptions')
    gen_group.add_argument('--kind-max-length', type=int, help='Max character length for kind descriptions')
    gen_group.add_argument('--token-efficient', choices=['true', 'false'],
                           help='Enable token efficiency optimizations')
    gen_group.add_argument('--relationships-only', action='store_true', default=None,
                           help='Only generate relationships, skip description generation')

    # Filtering Configuration
    filter_group = parser.add_argument_group('Filtering Configuration')
    filter_group.add_argument('--excluded-files', help='Comma-separated list of files to exclude')
    filter_group.add_argument('--excluded-kinds', help='Comma-separated list of kinds to exclude')
    filter_group.add_argument('--generic-fields', help='Comma-separated list of generic field names')
    filter_group.add_argument('--domain-identifiers', help='Comma-separated list of domain identifiers')

    # Relationship Configuration
    rel_group = parser.add_argument_group('Relationship Configuration')
    rel_group.add_argument('--fk-templates',
                           help='Foreign key templates (format: PK_TEMPLATE|FK_TEMPLATE,...)')
    rel_group.add_argument('--domain-mappings',
                           help='Domain mappings (format: domain:term1,term2|domain2:term3,term4)')

    # Utility options
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--dry-run', action='store_true', help='Validate configuration without processing')
    parser.add_argument('--version', action='version', version='metadata-bootstrap 1.0.0')

    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> Optional[str]:
    """
    Validate command line arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        Error message if validation fails, None if valid
    """
    # Check for required input and output combinations
    has_dir_mode = bool(args.input_dir or args.output_dir)
    has_file_mode = bool(args.input_file or args.output_file)

    if not has_dir_mode and not has_file_mode:
        # Check environment variables
        io_config = config.get_io_config()
        has_env_dir = bool(io_config['input_dir'] and io_config['output_dir'])
        has_env_file = bool(io_config['input_file'] and io_config['output_file'])

        if not has_env_dir and not has_env_file:
            # Provide helpful error message with environment variable names
            return (
                "Either input/output directory or input/output file must be specified.\n"
                "Options:\n"
                "1. Use command line: --input-dir ./input --output-dir ./output\n"
                "2. Set environment variables:\n"
                "   METADATA_BOOTSTRAP_INPUT_DIR=./input\n"
                "   METADATA_BOOTSTRAP_OUTPUT_DIR=./output\n"
                "3. Or create a .env file with these variables\n"
                f"Currently found: input_dir={io_config['input_dir']}, output_dir={io_config['output_dir']}"
            )

    if has_dir_mode and has_file_mode:
        return "Cannot specify both directory and file modes simultaneously"

    # Validate directory mode
    if has_dir_mode:
        input_dir = args.input_dir or config.get_io_config()['input_dir']
        output_dir = args.output_dir or config.get_io_config()['output_dir']

        if not input_dir:
            return "Input directory is required for directory mode"
        if not output_dir:
            return "Output directory is required for directory mode"
        if not os.path.exists(input_dir):
            return f"Input directory does not exist: {input_dir}"

    # Validate file mode
    if has_file_mode:
        input_file = args.input_file or config.get_io_config()['input_file']
        output_file = args.output_file or config.get_io_config()['output_file']

        if not input_file:
            return "Input file is required for file mode"
        if not output_file:
            return "Output file is required for file mode"
        if not os.path.exists(input_file):
            return f"Input file does not exist: {input_file}"

    # Validate API key
    api_key = args.api_key or config.api_key
    if not api_key:
        return "Anthropic API key is required (use --api-key or ANTHROPIC_API_KEY environment variable)"

    return None


def setup_logging(verbose: bool):
    """Configure logging based on verbosity level."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")


def create_bootstrapper_from_args(args: argparse.Namespace) -> MetadataBootstrapper:
    """
    Create a MetadataBootstrapper instance from command line arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        Configured MetadataBootstrapper instance
    """
    # Prepare constructor arguments
    api_key = args.api_key or config.api_key
    kwargs = {
        'model': args.model,
        'field_tokens': args.field_tokens,
        'kind_tokens': args.kind_tokens,
        'field_max_length': args.field_max_length,
        'kind_max_length': args.kind_max_length,
        'excluded_files': args.excluded_files.split(',') if args.excluded_files else None,
        'excluded_kinds': args.excluded_kinds.split(',') if args.excluded_kinds else None,
        'generic_fields': args.generic_fields.split(',') if args.generic_fields else None,
        'domain_identifiers': args.domain_identifiers.split(',') if args.domain_identifiers else None,
        'fk_templates_str': args.fk_templates,
        'relationships_only': args.relationships_only,
        'input_dir': args.input_dir,
        'output_dir': args.output_dir,
        'system_prompt': args.system_prompt,
    }

    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    return MetadataBootstrapper(api_key, **kwargs)


def determine_processing_mode(args: argparse.Namespace) -> tuple[str, dict]:
    """
    Determine processing mode and parameters.

    Args:
        args: Parsed command line arguments

    Returns:
        Tuple of (mode, parameters) where mode is 'directory' or 'file'
    """
    io_config = config.get_io_config()

    # Check for directory mode
    input_dir = args.input_dir or io_config['input_dir']
    output_dir = args.output_dir or io_config['output_dir']

    if input_dir and output_dir:
        return 'directory', {'input_dir': input_dir, 'output_dir': output_dir}

    # Check for file mode
    input_file = args.input_file or io_config['input_file']
    output_file = args.output_file or io_config['output_file']

    if input_file and output_file:
        return 'file', {'input_file': input_file, 'output_file': output_file}

    raise ValueError("Unable to determine processing mode")


def main():
    """Main application entry point."""
    args: Optional[Namespace] = None
    try:
        # Parse arguments
        args: Namespace = parse_arguments()

        # Setup logging
        setup_logging(args.verbose)

        # Validate arguments
        error_msg = validate_arguments(args)
        if error_msg:
            logger.error(f"Configuration error: {error_msg}")
            sys.exit(1)

        # Validate configuration
        if not config.validate():
            logger.error("Configuration validation failed")
            sys.exit(1)

        # Handle dry run
        if args.dry_run:
            logger.info("Dry run mode - configuration is valid")
            mode, params = determine_processing_mode(args)
            logger.info(f"Would process in {mode} mode with parameters: {params}")
            return

        # Create bootstrapper
        bootstrapper = create_bootstrapper_from_args(args)

        # Determine processing mode and run
        mode, params = determine_processing_mode(args)

        logger.info(f"Starting metadata bootstrap in {mode} mode")

        if mode == 'directory':
            bootstrapper.process_directory(params['input_dir'], params['output_dir'])
        elif mode == 'file':
            bootstrapper.process_file(params['input_file'], params['output_file'], params.get('input_dir'))

        # Print statistics
        stats = bootstrapper.get_statistics()
        logger.info("Processing completed successfully!")
        logger.info(f"Statistics: {stats}")

    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        if args.verbose:
            logger.exception("Full traceback:")
        exit(1)


if __name__ == "__main__":
    main()
