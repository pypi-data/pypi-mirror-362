#!/usr/bin/env python3

"""
Enhanced configuration management for Metadata Bootstrap.
Supports YAML configuration files with waterfall precedence:
CLI args > Environment variables > config.yaml > defaults

Single config file location: ./config.yaml
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when there's a configuration error."""
    pass


class ConfigLoader:
    """Handles loading configuration from multiple sources with proper precedence."""

    def __init__(self):
        self.config_data = {}
        self.config_sources = {}  # Track where each config value came from

    def load_all(self, config_file: Optional[str] = None, cli_args: Optional[argparse.Namespace] = None) -> Dict[
        str, Any]:
        """
        Load configuration from all sources with proper precedence.

        Args:
            config_file: Optional path to YAML config file (defaults to ./config.yaml)
            cli_args: Optional parsed CLI arguments

        Returns:
            Merged configuration dictionary
        """
        # 1. Load defaults first
        self._load_defaults()

        # 2. Load YAML config file
        self._load_yaml_config(config_file)

        # 3. Load environment variables
        self._load_env_files()
        self._load_env_variables()

        # 4. Load CLI arguments (highest precedence)
        if cli_args:
            self._load_cli_args(cli_args)

        return self.config_data

    def _load_defaults(self):
        """Load default configuration values."""
        defaults = {
            # API Configuration
            'model': 'claude-3-haiku-20240307',
            'api_key': None,

            # AI Generation Configuration
            'system_prompt': 'Focus on business purpose and data relationships.',

            # Description length limits
            'line_length': 65,
            'field_desc_max_length': 120,
            'kind_desc_max_length': 250,

            # Token limits for AI generation
            'field_tokens': 250,
            'kind_tokens': 400,

            # Target lengths for concise descriptions
            'short_field_target': 100,
            'short_kind_target': 180,

            # Quality Assessment
            'enable_quality_assessment': True,
            'minimum_description_score': 70,
            'minimum_marginal_score': 50,
            'max_description_retry_attempts': 3,
            'enable_field_skipping': True,

            # Processing Limits
            'max_examples': 5,
            'max_domain_keywords': 10,
            'token_efficient': True,

            # File Processing
            'file_glob': "**/metadata/*.hml",

            # Kinds to exclude from processing
            'excluded_kinds': [
                "DataConnectorScalarRepresentation",
                "DataConnectorLink",
                "BooleanExpressionType",
                "ScalarType",
                "AggregateExpression",
                "Model"
            ],

            # Files to exclude (glob patterns)
            'excluded_files': [],

            # Fields that are considered generic/shared
            'generic_fields': [
                "_id", "_key", "level", "kind", "id", "name", "code",
                "category", "title", "record", "node", "label"
            ],

            # Domain-specific identifiers
            'domain_identifiers': [
                "iata", "icao", "isbn", "swift", "duns", "cusip", "sedol",
                "gtin", "upc", "ean", "faa", "ein", "ssn", "passport",
                "license", "registration"
            ],

            # Patterns for fields to skip entirely
            'skip_field_patterns': [
                r"^id$", r"^_id$", r"^uuid$", r"^key$", r"^created_at$",
                r"^createdAt$", r"^updated_at$", r"^updatedAt$",
                r"^timestamp$", r"^version$", r"^revision$", r"^metadata$",
                r"^_internal$", r"^debug_", r"^temp_", r"^test_"
            ],

            # Patterns for rejecting shared keys (converted from generic_fields_regex)
            'shared_key_rejection_patterns': [
                r"^flag$", r"^value$", r"^object$", r"^status$", r"^state$",
                r"id_\d+$", r"^location$", r"^info$", r"^internal$", r"^external$",
                r"^unknown$", r"^details$", r"^revision$", r"^metadata$",
                r"^description$", r"^created", r"^updated", r".*_name$",
                r"^active$", r"^version$", r"^summary$", r"^debug_.*",
                r"^test_.*", r"^temp_.*", r".*_count$", r".*_total$",
                r".*_flag$", r".*_status$", r".*_enabled$", r".*_type$",
                r".*_time$", r".*_date$"
            ],

            # Buzzwords to avoid in descriptions
            'buzzwords': [
                'contains', 'stores', 'holds', 'represents', 'captures', 'maintains',
                'enabling', 'facilitating', 'supporting', 'allowing', 'helping', 'serving',
                'ensuring', 'providing', 'establishing', 'maintaining', 'delivering', 'achieving',
                'governance', 'efficiency', 'oversight', 'compliance', 'operations',
                'manages', 'controls', 'strategic', 'optimize', 'enhance', 'streamline', 'leverage',
                'supports', 'enables', 'ensures', 'provides', 'facilitates',
                'system governance', 'operational efficiency', 'technology oversight',
                'secure and compliant', 'trusted access', 'industry regulations',
                'business operations', 'decision making', 'best practices',
                'competitive advantage', 'organizational goals', 'stakeholder needs'
            ],

            # Forbidden patterns in descriptions
            'forbidden_patterns': [
                # Explanatory format patterns
                r'^w+s*\(\w+\)\s*:',  # "Identifier (ID):"
                r'^\w+\s*\(\w+\)\s+is',  # "Identifier (ID) is"
                r'the\s+\w+\s+\(\w+\)',  # "The Identifier (ID)"
                r'in\s+a\s+business\s+context',
                r'this\s+field\s+represents',
                r'this\s+entity\s+represents',
                r'the\s+purpose\s+of',
                r'used\s+to\s+(track|manage|identify)',
                r'acronym.*stands\s+fo',
                r'business.*information',
                r'information.*business',
                r'efficient.*operations',
                r'decision.*making',
                r'data.*integrity',
                r'record.*keeping',
                r'information.*retrieval',
                r'cross.*referencing',
                r'various.*types',
                r'such\s+as',
                r'for\s+example',
                r'including\s+but',
                r'within\s+the'
            ],

            # Technical type patterns
            'technical_type_patterns': [
                r'unique\s+(code|number|identifier)',
                r'assigned\s+to',
                r'(string|alphanumeric|numeric|boolean)',
                r'consists?\s+of',
                r'serves?\s+as',
                r'acts?\s+as',
                r'functions?\s+as'
            ],

            # Primitive types in OpenDD
            'primitive_types': ["ID", "Int", "Float", "Boolean", "String"],

            # OpenDD kinds to process
            'opendd_kinds': [
                "Type", "Command", "Model", "Relationship", "ObjectType",
                "ScalarType", "EnumType", "InputObjectType",
                "BooleanExpressionType", "ObjectBooleanExpressionType",
                "DataConnectorLink", "Subgraph", "Supergraph", "Role",
                "AuthConfig", "CompatibilityConfig", "GraphqlConfig"
            ],

            # FK template patterns for relationship detection
            'fk_templates': "{gi}|{pt}_{gi},{gi}|{ps}_{pt}_{gi}",

            # Relationship processing flags
            'relationships_only': False,
            'enable_shared_relationships': True,
            'max_shared_relationships': 10000,
            'max_shared_per_entity': 10,
            'min_shared_confidence': 30,
            'rebuild_all_relationships': False,

            # Cryptic Field Handling
            'skip_cryptic_abbreviations': True,
            'skip_ultra_short_fields': True,
            'max_cryptic_field_length': 4,
            'detect_field_name_redundancy': True,

            # I/O Configuration
            'input_dir': None,
            'output_dir': None,
            'input_file': None,
            'output_file': None,

            # Acronym mappings - extensive defaults from config.yaml
            'acronym_mappings': {
                # Technology & Computing
                'api': 'Application Programming Interface',
                'url': 'Uniform Resource Locator',
                'ui': 'User Interface',
                'db': 'Database',
                'os': 'Operating System',
                'cpu': 'Central Processing Unit',
                'ram': 'Random Access Memory',
                'ssd': 'Solid State Drive',
                'sw': 'Software',
                'hw': 'Hardware',
                'sys': 'System',

                # Network & Protocols
                'ip': 'Internet Protocol',
                'ips': 'Internet Protocol Addresses',
                'dhcp': 'Dynamic Host Configuration Protocol',
                'cidr': 'Classless Inter-Domain Routing',
                'mac': 'Media Access Control Address',
                'vpn': 'Virtual Private Network',
                'lanid': 'Local Area Network Identifier',

                # HTTP/Web Standards
                'ssl': 'Secure Sockets Layer',
                'tls': 'Transport Layer Security',
                'etag': 'Entity Tag',
                'oauth': 'Open Authorization',
                'oauth2': 'Open Authorization 2.0',

                # Development & Operations
                'ci': 'Continuous Integration',
                'cd': 'Continuous Deployment',
                'cots': 'Commercial Off-The-Shelf',

                # Data & Identifiers
                'id': 'Identifier',
                'uid': 'Unique Identifier',
                'int': 'Integer',
                'nbr': 'Number',
                'ind': 'Indicator',
                'dsc': 'Description',
                'descr': 'Description',
                'orig': 'Original',
                'src': 'Source',
                'dest': 'Destination',
                'mkv': 'Multivalue',
                'x': 'Extension',

                # Security & Access Management
                'mfa': 'Multi-Factor Authentication',
                'sso': 'Single Sign-On',
                'iam': 'Identity and Access Management',
                'siem': 'Security Information and Event Management',
                'wss': 'Web Security Service',
                'esar': 'Enterprise Security Assessment and Review',
                'sep': 'Symantec Endpoint Protection',
                'kms': 'Key Management System',
                'oob': 'Out-of-Band',
                'rmc': 'Remote Management Controller',

                # Cloud Platforms & Services
                'aws': 'Amazon Web Services',
                'az': 'Azure',
                'gcp': 'Google Cloud Platform',
                'paa': 'Platform as a Service',
                'snow': 'ServiceNow',
                'epca': 'Enterprise Platform for Compliance and Administration',

                # Financial Services & Compliance
                'finra': 'Financial Industry Regulatory Authority',
                'cftc': 'Commodity Futures Trading Commission',
                'sox': 'Sarbanes-Oxley Act',
                'glba': 'Gramm-Leach-Bliley Act',
                'pci': 'Payment Card Industry',
                'coso': 'Committee of Sponsoring Organizations (of the Treadway Commission)',
                'hdpa': 'Health Data Privacy Act',
                'mnpi': 'Material Non-Public Information',
                'rc': 'Risk Category',
                'soc': 'Service Organizational Control',

                # Organizational & Business
                'hr': 'Human Resources',
                'emplid': 'Employee Identifier',
                'elid': 'Employee Identifier',
                'ps': 'PeopleSoft',
                'lob': 'Line of Business',
                'au': 'Administrative Unit',
                'cio': 'Chief Information Office',
                'exec': 'Executive',
                'org': 'Organization',
                'wf': 'Wells Fargo',
                'reg': 'Regular',
                'temp': 'Temporary',

                # Enterprise Architecture & Governance
                'edg': 'Enterprise Data Governance',
                'esa': 'Enterprise Service Architecture',
                'dmi': 'Data Management Initiative',
                'wam': 'Web Application Management',
                'itam': 'IT Asset Management',
                'bs': 'Business Service',
                'bsns': 'Business Service Namespace',
                'ns': 'Namespace',
                'be': 'building entity',
                'cpg': 'customer profile group',
                'sor': 'System of Record',
                'soo': 'System of Origin',
                'trims': 'Threat Response and Incident Management System',

                # Operational & Infrastructure
                'bcp': 'Business Continuity Plan',
                'trl': 'Technology Readiness Level',
                'rtc': 'Real-Time Code',
                'bits': 'Building Integrated Timing Supply',
            }
        }

        for key, value in defaults.items():
            self.config_data[key] = value
            self.config_sources[key] = 'defaults'

    def _load_yaml_config(self, config_file: Optional[str] = None):
        """Load configuration from YAML file."""
        if config_file:
            yaml_path = Path(config_file)
        else:
            yaml_path = Path.cwd() / 'config.yaml'

        if yaml_path.exists():
            try:
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    yaml_config = yaml.safe_load(f) or {}

                logger.info(f"✅ Loaded YAML configuration from: {yaml_path}")
                self._merge_yaml_config(yaml_config)

            except Exception as e:
                logger.error(f"❌ Failed to load YAML config from {yaml_path}: {e}")
                if config_file:  # If explicitly specified, raise error
                    raise ConfigurationError(f"Failed to load specified config file {config_file}: {e}")
        else:
            if config_file:
                raise ConfigurationError(f"Specified config file not found: {config_file}")
            else:
                logger.info("ℹ️  No config.yaml found, using environment variables and defaults")

    def _merge_yaml_config(self, yaml_config: Dict[str, Any]):
        """Merge YAML configuration into config_data."""

        def merge_recursive(target: Dict, source: Dict, path: str = ""):
            for key, value in source.items():
                current_path = f"{path}.{key}" if path else key

                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_recursive(target[key], value, current_path)
                else:
                    target[key] = value
                    self.config_sources[key] = f'yaml:{current_path}'

        merge_recursive(self.config_data, yaml_config)

    @staticmethod
    def _load_env_files():
        """Load environment variables from .env file."""
        env_path = Path.cwd() / '.env'

        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"✅ Loaded environment variables from: {env_path}")
        else:
            logger.info("ℹ️  No .env file found, using system environment variables only")

    def _load_env_variables(self):
        """Load configuration from environment variables."""
        env_mappings = {
            # API Configuration
            'METADATA_BOOTSTRAP_MODEL': 'model',
            'ANTHROPIC_API_KEY': 'api_key',

            # Processing Configuration
            'METADATA_BOOTSTRAP_LINE_LENGTH': ('line_length', int),
            'METADATA_BOOTSTRAP_FIELD_DESC_MAX_LENGTH': ('field_desc_max_length', int),
            'METADATA_BOOTSTRAP_KIND_DESC_MAX_LENGTH': ('kind_desc_max_length', int),
            'METADATA_BOOTSTRAP_FIELD_TOKENS': ('field_tokens', int),
            'METADATA_BOOTSTRAP_KIND_TOKENS': ('kind_tokens', int),
            'METADATA_BOOTSTRAP_SHORT_FIELD_TARGET': ('short_field_target', int),
            'METADATA_BOOTSTRAP_SHORT_KIND_TARGET': ('short_kind_target', int),

            # AI Configuration
            'METADATA_BOOTSTRAP_SYSTEM_PROMPT': 'system_prompt',

            # Processing Limits
            'METADATA_BOOTSTRAP_MAX_EXAMPLES': ('max_examples', int),
            'METADATA_BOOTSTRAP_MAX_DOMAIN_KEYWORDS': ('max_domain_keywords', int),
            'METADATA_BOOTSTRAP_TOKEN_EFFICIENT': ('token_efficient', bool),

            # File Configuration
            'FILE_GLOB': 'file_glob',

            # Quality Assessment
            'METADATA_BOOTSTRAP_ENABLE_QUALITY_ASSESSMENT': ('enable_quality_assessment', bool),
            'METADATA_BOOTSTRAP_MIN_DESCRIPTION_SCORE': ('minimum_description_score', int),
            'METADATA_BOOTSTRAP_MIN_MARGINAL_SCORE': ('minimum_marginal_score', int),
            'METADATA_BOOTSTRAP_MAX_RETRY_ATTEMPTS': ('max_description_retry_attempts', int),
            'METADATA_BOOTSTRAP_ENABLE_FIELD_SKIPPING': ('enable_field_skipping', bool),

            # Relationships
            'METADATA_BOOTSTRAP_RELATIONSHIPS_ONLY': ('relationships_only', bool),
            'METADATA_BOOTSTRAP_ENABLE_SHARED_RELATIONSHIPS': ('enable_shared_relationships', bool),
            'METADATA_BOOTSTRAP_MAX_SHARED_RELATIONSHIPS': ('max_shared_relationships', int),
            'METADATA_BOOTSTRAP_MAX_SHARED_PER_ENTITY': ('max_shared_per_entity', int),
            'METADATA_BOOTSTRAP_MIN_SHARED_CONFIDENCE': ('min_shared_confidence', int),
            'REBUILD_ALL_RELATIONSHIPS': ('rebuild_all_relationships', bool),

            # Cryptic Field Handling
            'METADATA_BOOTSTRAP_SKIP_CRYPTIC': ('skip_cryptic_abbreviations', bool),
            'METADATA_BOOTSTRAP_SKIP_ULTRA_SHORT': ('skip_ultra_short_fields', bool),
            'METADATA_BOOTSTRAP_MAX_CRYPTIC_LENGTH': ('max_cryptic_field_length', int),
            'METADATA_BOOTSTRAP_DETECT_REDUNDANCY': ('detect_field_name_redundancy', bool),

            # I/O Configuration
            'METADATA_BOOTSTRAP_INPUT_DIR': 'input_dir',
            'METADATA_BOOTSTRAP_OUTPUT_DIR': 'output_dir',
            'METADATA_BOOTSTRAP_INPUT_FILE': 'input_file',
            'METADATA_BOOTSTRAP_OUTPUT_FILE': 'output_file',

            # List-based configurations (simplified - most come from YAML)
            'METADATA_BOOTSTRAP_EXCLUDED_KINDS': ('excluded_kinds', 'list'),
            'METADATA_BOOTSTRAP_EXCLUDED_FILES': ('excluded_files', 'list'),
            'METADATA_BOOTSTRAP_GENERIC_FIELDS': ('generic_fields', 'list'),
            'METADATA_BOOTSTRAP_DOMAIN_IDENTIFIERS': ('domain_identifiers', 'list'),
            'METADATA_BOOTSTRAP_SKIP_FIELD_PATTERNS': ('skip_field_patterns', 'list'),
            'METADATA_BOOTSTRAP_PRIMITIVE_TYPES': ('primitive_types', 'list'),
            'METADATA_BOOTSTRAP_KINDS': ('opendd_kinds', 'list'),
            'METADATA_BOOTSTRAP_FK_TEMPLATES': 'fk_templates',
        }

        for env_key, config_mapping in env_mappings.items():
            env_value = os.environ.get(env_key)
            if env_value is not None:
                if isinstance(config_mapping, tuple):
                    config_key, converter = config_mapping
                    try:
                        if converter == int:
                            self.config_data[config_key] = int(env_value)
                        elif converter == bool:
                            self.config_data[config_key] = env_value.lower() in ('true', 'yes', '1')
                        elif converter == 'list':
                            self.config_data[config_key] = self._parse_list(env_value)
                        else:
                            self.config_data[config_key] = env_value
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Failed to convert env var {env_key}={env_value}: {e}")
                        continue
                else:
                    config_key = config_mapping
                    self.config_data[config_key] = env_value

                self.config_sources[config_key] = f'env:{env_key}'

    def _load_cli_args(self, cli_args: argparse.Namespace):
        """Load configuration from CLI arguments."""
        # Map CLI argument names to config keys
        cli_mappings = {
            'model': 'model',
            'api_key': 'api_key',
            'input_dir': 'input_dir',
            'output_dir': 'output_dir',
            'input_file': 'input_file',
            'output_file': 'output_file',
            'enable_quality_assessment': 'enable_quality_assessment',
            'disable_quality_assessment': ('enable_quality_assessment', False),
            'skip_cryptic': 'skip_cryptic_abbreviations',
            'relationships_only': 'relationships_only',
            'rebuild_relationships': 'rebuild_all_relationships',
        }

        for cli_arg, config_mapping in cli_mappings.items():
            if hasattr(cli_args, cli_arg):
                value = getattr(cli_args, cli_arg)
                if value is not None:
                    if isinstance(config_mapping, tuple):
                        config_key, override_value = config_mapping
                        if value:  # If flag is present
                            self.config_data[config_key] = override_value
                            self.config_sources[config_key] = f'cli:--{cli_arg}'
                    else:
                        config_key = config_mapping
                        self.config_data[config_key] = value
                        self.config_sources[config_key] = f'cli:--{cli_arg}'

    @staticmethod
    def _parse_list(value: str) -> List[str]:
        """Parse comma-separated string into list."""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]


class BootstrapperConfig:
    """Configuration class with YAML support and waterfall precedence."""

    def _optimize_config_for_hash_lookups(self):
        """
        Optimize configuration data structures for O(1) hash lookups.
        This should be called during config initialization.
        """

        # Ensure acronym mappings are dictionaries for O(1) lookup
        if hasattr(self, 'acronym_mappings') and not isinstance(self.acronym_mappings, dict):
            # Convert list of tuples or other format to dict if needed
            if isinstance(self.acronym_mappings, (list, tuple)):
                self.acronym_mappings = dict(self.acronym_mappings)
            else:
                self.acronym_mappings = {}

        # Handle acronym_meanings if it exists (from YAML config)
        if hasattr(self, 'acronym_meanings') and not isinstance(self.acronym_meanings, dict):
            if isinstance(self.acronym_meanings, (list, tuple)):
                self.acronym_meanings = dict(self.acronym_meanings)
            else:
                self.acronym_meanings = {}

        # Handle domain_abbreviations if it exists (from YAML config)
        if hasattr(self, 'domain_abbreviations') and not isinstance(self.domain_abbreviations, dict):
            if isinstance(self.domain_abbreviations, (list, tuple)):
                self.domain_abbreviations = dict(self.domain_abbreviations)
            else:
                self.domain_abbreviations = {}

        # Create optimized lookup sets for frequently checked lists
        if hasattr(self, 'generic_fields'):
            self._generic_fields_set = {gf.lower() for gf in self.generic_fields}

        if hasattr(self, 'opendd_kinds'):
            self._opendd_kinds_set = set(self.opendd_kinds)

        if hasattr(self, 'excluded_kinds'):
            self._excluded_kinds_set = set(self.excluded_kinds)

        if hasattr(self, 'buzzwords'):
            self._buzzwords_set = set(self.buzzwords)

        if hasattr(self, 'excluded_files'):
            self._excluded_files_set = set(self.excluded_files)

    def get_optimized_acronym_lookup(self) -> Dict[str, str]:
        """
        Get combined acronym lookup dictionary for optimal performance.
        Merges all acronym sources into a single hash table.
        """
        combined_acronyms = {}

        # Merge all acronym sources
        if hasattr(self, 'acronym_mappings') and isinstance(self.acronym_mappings, dict):
            combined_acronyms.update(self.acronym_mappings)

        if hasattr(self, 'acronym_meanings') and isinstance(self.acronym_meanings, dict):
            combined_acronyms.update(self.acronym_meanings)

        if hasattr(self, 'domain_abbreviations') and isinstance(self.domain_abbreviations, dict):
            # Extract default domain abbreviations
            default_terms = self.domain_abbreviations.get('default', {})
            if isinstance(default_terms, dict):
                combined_acronyms.update(default_terms)
            elif isinstance(default_terms, (set, list)):
                # Convert set/list to dict with empty values if needed
                for term in default_terms:
                    if term not in combined_acronyms:
                        combined_acronyms[term] = term.upper()

        return combined_acronyms

    def is_opendd_kind_optimized(self, kind: str) -> bool:
        """Optimized OpenDD kind checking using hash lookup."""
        if not hasattr(self, '_opendd_kinds_set'):
            self._opendd_kinds_set = set(getattr(self, 'opendd_kinds', []))

        return kind in self._opendd_kinds_set

    def is_excluded_kind_optimized(self, kind: str) -> bool:
        """Optimized excluded kind checking using hash lookup."""
        if not hasattr(self, '_excluded_kinds_set'):
            self._excluded_kinds_set = set(getattr(self, 'excluded_kinds', []))

        return kind in self._excluded_kinds_set

    def is_buzzword_optimized(self, word: str) -> bool:
        """Optimized buzzword checking using hash lookup."""
        if not hasattr(self, '_buzzwords_set'):
            self._buzzwords_set = set(getattr(self, 'buzzwords', []))

        return word.lower() in self._buzzwords_set

    def is_excluded_file_optimized(self, filename: str) -> bool:
        """Optimized excluded file checking using hash lookup."""
        if not hasattr(self, '_excluded_files_set'):
            self._excluded_files_set = set(getattr(self, 'excluded_files', []))

        return filename in self._excluded_files_set

    def _setup_attributes(self):
        """Set up all configuration attributes from loaded data."""
        # API Configuration
        self.model = self.config_data['model']
        self.api_key = self.config_data['api_key']

        # AI Generation Configuration
        self.system_prompt = self.config_data['system_prompt']

        # Description length limits
        self.line_length = self.config_data['line_length']
        self.field_desc_max_length = self.config_data['field_desc_max_length']
        self.kind_desc_max_length = self.config_data['kind_desc_max_length']

        # Token limits for AI generation
        self.field_tokens = self.config_data['field_tokens']
        self.kind_tokens = self.config_data['kind_tokens']

        # Target lengths for concise descriptions
        self.short_field_target = self.config_data['short_field_target']
        self.short_kind_target = self.config_data['short_kind_target']

        # Quality Assessment
        self.enable_quality_assessment = self.config_data['enable_quality_assessment']
        self.minimum_description_score = self.config_data['minimum_description_score']
        self.minimum_marginal_score = self.config_data['minimum_marginal_score']
        self.max_description_retry_attempts = self.config_data['max_description_retry_attempts']
        self.enable_field_skipping = self.config_data['enable_field_skipping']

        # Processing Limits
        self.max_examples = self.config_data['max_examples']
        self.max_domain_keywords = self.config_data['max_domain_keywords']
        self.token_efficient = self.config_data['token_efficient']

        # File Processing
        self.file_glob = self.config_data['file_glob']

        # Exclusions
        self.excluded_kinds = self.config_data['excluded_kinds']
        self.excluded_files = self.config_data['excluded_files']

        # Field Analysis
        self.generic_fields = self.config_data['generic_fields']
        self.domain_identifiers = self.config_data['domain_identifiers']
        self.skip_field_patterns = self.config_data['skip_field_patterns']
        self.shared_key_rejection_patterns = self.config_data['shared_key_rejection_patterns']

        # Content Quality Control
        self.buzzwords = self.config_data['buzzwords']
        self.forbidden_patterns = self.config_data['forbidden_patterns']
        self.technical_type_patterns = self.config_data['technical_type_patterns']

        # OpenDD Schema Configuration
        self.primitive_types = self.config_data['primitive_types']
        self.opendd_kinds = self.config_data['opendd_kinds']

        # FK Templates (handle both array and comma-delimited string formats)
        self.fk_templates_raw = self.config_data.get('fk_templates', [])

        # Convert comma-delimited string to array if needed (for env vars/CLI)
        if isinstance(self.fk_templates_raw, str):
            self.fk_templates = [template.strip() for template in self.fk_templates_raw.split(',') if template.strip()]
        elif isinstance(self.fk_templates_raw, list):
            self.fk_templates = self.fk_templates_raw
        else:
            logger.warning(f"Invalid fk_templates format: {type(self.fk_templates_raw)}. Using empty list.")
            self.fk_templates = []

        # Relationships
        self.relationships_only = self.config_data.get('relationships_only', None)
        self.enable_shared_relationships = self.config_data['enable_shared_relationships']
        self.max_shared_relationships = self.config_data['max_shared_relationships']
        self.max_shared_per_entity = self.config_data['max_shared_per_entity']
        self.min_shared_confidence = self.config_data['min_shared_confidence']
        self.rebuild_all_relationships = self.config_data['rebuild_all_relationships']

        # FK key blacklist (RENAMED from cross_source_fk_blacklist)
        self.fk_key_blacklist = self.config_data.get('fk_key_blacklist', [])

        # Cryptic Field Handling
        self.skip_cryptic_abbreviations = self.config_data['skip_cryptic_abbreviations']
        self.skip_ultra_short_fields = self.config_data['skip_ultra_short_fields']
        self.max_cryptic_field_length = self.config_data['max_cryptic_field_length']
        self.detect_field_name_redundancy = self.config_data['detect_field_name_redundancy']

        # I/O Configuration
        self.input_dir = self.config_data['input_dir'] or ''
        self.output_dir = self.config_data['output_dir'] or ''
        self.input_file = self.config_data['input_file']
        self.output_file = self.config_data['output_file']

        # Acronym mappings
        self.acronym_mappings = self.config_data['acronym_mappings']

        # Handle missing attributes that may be in YAML config
        self.acronym_meanings = self.config_data.get('acronym_meanings', {})
        self.domain_abbreviations = self.config_data.get('domain_abbreviations', {})
        self.self_explanatory_patterns = self.config_data.get('self_explanatory_patterns', [])

    def __init__(self, config_file: Optional[str] = None, cli_args: Optional[argparse.Namespace] = None):
        """
        Initialize configuration with waterfall precedence.

        Args:
            config_file: Optional path to YAML config file (defaults to ./config.yaml)
            cli_args: Optional parsed CLI arguments
        """
        self._excluded_files_set = None
        self._buzzwords_set = None
        self._excluded_kinds_set = None
        self._opendd_kinds_set = None
        self.loader = ConfigLoader()
        self.config_data = self.loader.load_all(config_file, cli_args)

        # Set up all configuration attributes
        self._setup_attributes()

        # Set up derived configurations
        self._setup_derived_configs()

        # Compile regex patterns from YAML and set up compiled defaults
        self._compile_regex_patterns()

        # OPTIMIZATION: Apply hash-based lookup optimizations
        self._optimize_config_for_hash_lookups()

    def _compile_regex_patterns(self):
        """Compile regex patterns loaded from YAML configuration."""
        try:
            # Compile forbidden patterns
            self.compiled_forbidden_patterns = []
            for pattern in self.forbidden_patterns:
                try:
                    self.compiled_forbidden_patterns.append(re.compile(pattern, re.IGNORECASE))
                except re.error as e:
                    logger.warning(f"Failed to compile forbidden pattern '{pattern}': {e}")

            # Compile technical type patterns
            self.compiled_technical_patterns = []
            for pattern in self.technical_type_patterns:
                try:
                    self.compiled_technical_patterns.append(re.compile(pattern, re.IGNORECASE))
                except re.error as e:
                    logger.warning(f"Failed to compile technical pattern '{pattern}': {e}")

            # Compile skip field patterns
            self.compiled_skip_patterns = []
            for pattern in self.skip_field_patterns:
                try:
                    self.compiled_skip_patterns.append(re.compile(pattern))
                except re.error as e:
                    logger.warning(f"Failed to compile skip field pattern '{pattern}': {e}")

            # Compile shared key rejection patterns
            self.compiled_shared_key_rejection_patterns = []
            for pattern in self.shared_key_rejection_patterns:
                try:
                    self.compiled_shared_key_rejection_patterns.append(re.compile(pattern))
                except re.error as e:
                    logger.warning(f"Failed to compile shared key rejection pattern '{pattern}': {e}")

            self.compiled_self_explanatory_patterns = []
            for pattern in self.self_explanatory_patterns:
                try:
                    self.compiled_self_explanatory_patterns.append(re.compile(pattern))
                except re.error as e:
                    logger.warning(f"Failed to compile self-explanatory pattern '{pattern}': {e}")

            # UPDATED: Compile FK key blacklist patterns
            self.compiled_fk_blacklist = []
            for rule in self.fk_key_blacklist:
                try:
                    sources = rule.get('sources', [])
                    field_pattern = rule.get('field_pattern', '*')
                    entity_pattern = rule.get('entity_pattern', '*')
                    logic = rule.get('logic', 'and').lower()
                    reason = rule.get('reason', 'No reason specified')

                    # Validate sources is a list
                    if not isinstance(sources, list) or not sources:
                        logger.warning(f"Invalid sources in FK key blacklist rule: {rule}")
                        continue

                    # Validate logic parameter
                    if logic not in ['and', 'or']:
                        logger.warning(
                            f"Invalid logic '{logic}' in FK key blacklist rule: {rule}. Using 'and' as default.")
                        logic = 'and'

                    # Convert sources to lowercase for case-insensitive matching
                    normalized_sources = [source.lower() for source in sources]

                    # Convert glob patterns to regex if needed
                    if field_pattern == '*':
                        compiled_field_pattern = re.compile('.*')
                    else:
                        # Treat as regex pattern directly
                        compiled_field_pattern = re.compile(field_pattern)

                    if entity_pattern == '*':
                        compiled_entity_pattern = re.compile('.*')
                    else:
                        # Treat as regex pattern directly
                        compiled_entity_pattern = re.compile(entity_pattern)

                    compiled_rule = {
                        'sources': normalized_sources,
                        'field_pattern': compiled_field_pattern,
                        'entity_pattern': compiled_entity_pattern,
                        'logic': logic,
                        'original_field_pattern': field_pattern,
                        'original_entity_pattern': entity_pattern,
                        'reason': reason
                    }

                    self.compiled_fk_blacklist.append(compiled_rule)
                    logger.info(
                        f"Compiled FK key blacklist rule: sources={sources}, field: {field_pattern}, entity: {entity_pattern}, logic: {logic}")

                except re.error as e:
                    logger.warning(f"Failed to compile FK key blacklist pattern '{rule}': {e}")
                except Exception as e:
                    logger.warning(f"Error processing FK key blacklist rule '{rule}': {e}")

        except Exception as e:
            logger.warning(f"Failed to compile regex patterns: {e}")
            self.compiled_forbidden_patterns = []
            self.compiled_technical_patterns = []
            self.compiled_skip_patterns = []
            self.compiled_shared_key_rejection_patterns = []
            self.compiled_fk_blacklist = []

    def parse_fk_templates(self) -> List[Dict]:
        """Parse FK templates from configuration array or comma-delimited string."""
        parsed_templates = []

        if not self.fk_templates:
            logger.warning("No FK templates provided.")
            return parsed_templates

        # Build regex patterns - each element should be a single alphanumeric string
        pt_re = r"(?P<primary_table>[a-zA-Z0-9]+)"  # Single alphanumeric string (no underscores)
        ps_re = r"(?P<primary_subgraph>[a-zA-Z0-9]+)"  # Single alphanumeric string (no underscores)
        fs_re = r"(?P<foreign_subgraph>[a-zA-Z0-9]+)"  # Single alphanumeric string (no underscores)
        pm_re = r"(?P<prefix_modifier>\w+)"  # Can be anything including underscores

        sorted_generic_fields = sorted(self.generic_fields, key=len, reverse=True)
        gi_re_options = "|".join(re.escape(gf) for gf in sorted_generic_fields)
        gi_re = f"(?P<generic_id>(?:{gi_re_options}))"

        for tpl_pair_str in self.fk_templates:
            tpl_pair_str = tpl_pair_str.strip()
            if not tpl_pair_str or '|' not in tpl_pair_str:
                continue

            pk_tpl_str, fk_tpl_str_orig = [part.strip() for part in tpl_pair_str.split('|', 1)]

            fk_regex_str = fk_tpl_str_orig
            fk_regex_str = fk_regex_str.replace("{fs}", fs_re)
            fk_regex_str = fk_regex_str.replace("{ps}", ps_re)
            fk_regex_str = fk_regex_str.replace("{pt}", pt_re)
            fk_regex_str = fk_regex_str.replace("{pm}", pm_re)
            fk_regex_str = fk_regex_str.replace("{gi}", gi_re)
            fk_regex_str = f"^{fk_regex_str}$"

            try:
                compiled_regex = re.compile(fk_regex_str)
                parsed_templates.append({
                    'pk_template_str': pk_tpl_str,
                    'fk_template_str_orig': fk_tpl_str_orig,
                    'fk_regex': compiled_regex
                })
                logger.debug(f"Compiled FK template: '{fk_tpl_str_orig}' -> regex: '{fk_regex_str}'")
            except re.error as e:
                logger.error(f"Failed to compile regex for FK template '{fk_tpl_str_orig}': {e}")

        logger.info(f"Successfully parsed {len(parsed_templates)} FK templates")
        return parsed_templates

    def _setup_derived_configs(self):
        """Set up derived/computed configuration values."""
        # Parse FK templates (now from array format)
        self.fk_templates_parsed = self.parse_fk_templates()

        # Special markers
        self.relationship_marker = "***ADD_RELATIONSHIPS***"

        # Set up quality assessment patterns
        self._setup_quality_patterns()

    def is_fk_blocked(self, source_entity_name: str, target_entity_name: str,
                      source_data_source: str, target_data_source: str,
                      field_name: str) -> tuple[bool, str]:
        """
        Check if a foreign key relationship should be blocked.

        UPDATED: Now supports both cross-source and intra-source blocking for FK relationships.
        Uses multi-source rules with entity pattern matching and configurable logic.
        Blocks FK relationships between any sources in the same blacklist rule
        based on entity patterns and/or field patterns depending on the logic setting.

        Args:
            source_entity_name: Name of the source entity
            target_entity_name: Name of the target entity
            source_data_source: Data source of the source entity
            target_data_source: Data source of the target entity
            field_name: Name of the field creating the relationship

        Returns:
            Tuple of (is_blocked, reason)
        """
        if not hasattr(self, 'compiled_fk_blacklist'):
            return False, "No FK blacklist compiled"

        # Normalize input data sources for comparison
        source_normalized = source_data_source.lower()
        target_normalized = target_data_source.lower()

        for rule in self.compiled_fk_blacklist:
            sources_list = rule['sources']
            field_regex = rule['field_pattern']
            entity_regex = rule['entity_pattern']
            logic = rule['logic']
            reason = rule['reason']

            # Check if BOTH source and target are in the sources list
            source_in_list = source_normalized in sources_list
            target_in_list = target_normalized in sources_list

            # Skip if both sources aren't in the list
            if not (source_in_list and target_in_list):
                continue

            # Check pattern matches
            field_matches = field_regex.match(field_name)
            source_entity_matches = entity_regex.match(source_entity_name)
            target_entity_matches = entity_regex.match(target_entity_name)
            entity_matches = source_entity_matches or target_entity_matches

            # Apply logic operator
            pattern_match = False
            if logic == 'and':
                pattern_match = field_matches and entity_matches
            elif logic == 'or':
                pattern_match = field_matches or entity_matches

            # Block if pattern conditions are met
            if pattern_match:
                # Build detailed match information
                match_details = []
                if field_matches:
                    match_details.append(f"field '{field_name}' matches pattern '{rule['original_field_pattern']}'")
                if entity_matches:
                    entity_match_info = []
                    if source_entity_matches:
                        entity_match_info.append(f"source entity '{source_entity_name}'")
                    if target_entity_matches:
                        entity_match_info.append(f"target entity '{target_entity_name}'")
                    match_details.append(
                        f"entity pattern '{rule['original_entity_pattern']}' matches {' and '.join(entity_match_info)}")

                # Determine if this is cross-source or intra-source
                relationship_type = "cross-source" if source_normalized != target_normalized else "intra-source"

                detailed_reason = (f"Blocked by {relationship_type} FK rule: sources={rule['sources']}, "
                                   f"logic='{logic}', {' and '.join(match_details) if logic == 'and' else ' or '.join(match_details)}. "
                                   f"Reason: {reason}")
                return True, detailed_reason

        return False, "Not blocked"

    def _setup_quality_patterns(self):
        """Set up quality assessment patterns."""
        self.circular_description_patterns = [
            "business information about",
            "information about this",
            "describes the",
            "represents the",
            "stores information about",
            "contains.*data",
            "holds.*information",
            "data about this",
            "stores business information",
            "business data about"
        ]

        self.generic_rejection_patterns = [
            "business information$",
            "data storage$",
            "information storage$",
            "stores data$",
            "contains information$",
            "holds data$",
            "general information$",
            "basic data$"
        ]

    def get_acronym_meaning(self, acronym: str, _context_text: str = "") -> str:
        """Get the appropriate meaning for an acronym based on context."""
        acronym_lower = acronym.lower()

        if acronym_lower in self.acronym_mappings:
            return self.acronym_mappings[acronym_lower]

        return acronym.upper()

    def enhance_field_description_with_acronyms(self, field_name: str, description: str, context: str = "") -> str:
        """
        Enhance a field description by expanding acronyms found in the field name.

        Args:
            field_name: The name of the field
            description: The generated description
            context: Combined context from entity and field information

        Returns:
            Enhanced description with acronym meanings
        """
        if not description:
            return description

        # Extract potential acronyms from field name
        field_parts = field_name.lower().split('_')
        acronyms_found = []

        for part in field_parts:
            if len(part) <= 5 and part.isalpha() and part in self.acronym_mappings:
                meaning = self.get_acronym_meaning(part, context)
                if meaning != part.upper():
                    acronyms_found.append((part.upper(), meaning))

        # If we found acronyms, enhance the description
        if acronyms_found:
            enhanced_description = description

            # Replace acronym mentions in description with full meaning
            for acronym, meaning in acronyms_found:
                # Be careful not to replace partial matches
                pattern = r'\b' + re.escape(acronym) + r'\b'
                enhanced_description = re.sub(pattern, meaning, enhanced_description, flags=re.IGNORECASE)

            return enhanced_description

        return description

    def validate(self) -> bool:
        """Validate configuration and return True if valid."""
        errors = []

        if not self.api_key:
            errors.append("API key is required (set ANTHROPIC_API_KEY or specify in config)")

        if self.line_length < 20:
            errors.append("Line length must be at least 20 characters")

        if self.field_desc_max_length < 50:
            errors.append("Field description max length must be at least 50 characters")

        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            return False

        return True

    def is_shared_key(self, field_name: str) -> bool:
        """Determine if a field is a valid, shared key."""
        if field_name in self.generic_fields:
            return False

        for pattern in self.compiled_shared_key_rejection_patterns:
            if pattern.match(field_name):
                return False

        return True

    @staticmethod
    def get_io_config() -> Dict[str, str]:
        """Get input/output configuration from environment."""
        return {
            'input_dir': os.environ.get('METADATA_BOOTSTRAP_INPUT_DIR'),
            'output_dir': os.environ.get('METADATA_BOOTSTRAP_OUTPUT_DIR'),
            'input_file': os.environ.get('METADATA_BOOTSTRAP_INPUT_FILE'),
            'output_file': os.environ.get('METADATA_BOOTSTRAP_OUTPUT_FILE'),
        }

    def print_config_sources(self):
        """Print where each configuration value came from."""
        print("\n📋 Configuration Sources:")
        print("=" * 50)

        for key, source in sorted(self.loader.config_sources.items()):
            value = self.config_data.get(key, 'N/A')
            # Mask sensitive values
            if 'key' in key.lower() or 'token' in key.lower():
                display_value = '***masked***' if value else 'None'
            elif isinstance(value, list) and len(value) > 3:
                display_value = f"[{len(value)} items]"
            elif isinstance(value, dict) and len(value) > 3:
                display_value = f"{{_{len(value)} mappings}}"
            else:
                display_value = str(value)[:50] + ('...' if len(str(value)) > 50 else '')

            print(f"{key:30} = {display_value:30} [{source}]")
        print()


def create_cli_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser for configuration."""
    parser = argparse.ArgumentParser(
        description='Metadata Bootstrap Configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Configuration precedence (highest to lowest):
  1. Command line arguments
  2. Environment variables  
  3. config.yaml (in current directory)
  4. Default values

Example usage:
  python script.py                              # Use ./config.yaml if exists
  python script.py --config custom.yaml        # Use specific config file
        """
    )

    # Configuration file
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to YAML configuration file (default: ./config.yaml)'
    )

    # API Configuration
    parser.add_argument(
        '--model',
        type=str,
        help='AI model to use'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key'
    )

    # I/O Configuration
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Input directory path'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory path'
    )

    parser.add_argument(
        '--input-file',
        type=str,
        help='Input file path'
    )

    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file path'
    )

    # Feature Flags
    parser.add_argument(
        '--enable-quality-assessment',
        action='store_true',
        help='Enable AI quality assessment'
    )

    parser.add_argument(
        '--disable-quality-assessment',
        action='store_true',
        help='Disable AI quality assessment'
    )

    parser.add_argument(
        '--skip-cryptic',
        action='store_true',
        help='Skip cryptic field names'
    )

    parser.add_argument(
        '--relationships-only',
        action='store_true',
        help='Only process relationships, skip description generation'
    )

    parser.add_argument(
        '--rebuild-relationships',
        action='store_true',
        help='Rebuild all relationships from scratch'
    )

    # Utility
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Show configuration sources and exit'
    )

    parser.add_argument(
        '--validate-config',
        action='store_true',
        help='Validate configuration and exit'
    )

    return parser


def load_config(config_file: Optional[str] = None, cli_args: Optional[argparse.Namespace] = None) -> BootstrapperConfig:
    """
    Load configuration with proper precedence handling.

    Args:
        config_file: Optional path to YAML config file (defaults to ./config.yaml)
        cli_args: Optional parsed CLI arguments

    Returns:
        Configured BootstrapperConfig instance
    """
    try:
        config = BootstrapperConfig(config_file, cli_args)

        if not config.validate():
            raise ConfigurationError("Configuration validation failed")

        return config

    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise


# Global configuration instance for backward compatibility
# This will be initialized with defaults and environment variables
config = BootstrapperConfig()

if __name__ == "__main__":
    # CLI interface for configuration testing
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        config = load_config(args.config, args)

        if args.show_config:
            config.print_config_sources()
            sys.exit(0)

        if args.validate_config:
            if config.validate():
                print("✅ Configuration is valid")
                sys.exit(0)
            else:
                print("❌ Configuration validation failed")
                sys.exit(1)

        print("✅ Configuration loaded successfully")
        config.print_config_sources()

    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
