# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-23

### Added
- Initial release of DDN Metadata Bootstrap
- AI-powered description generation using Anthropic Claude
- Automatic relationship detection and generation
- Support for Hasura DDN schema files (HML/YAML)
- Domain analysis and terminology extraction
- Batch processing of directory structures
- Comprehensive CLI interface
- Environment variable configuration
- Cross-subgraph relationship support
- Field-level and entity-level description generation
- Foreign key pattern detection
- Shared field relationship identification
- Token-efficient description optimization
- Configurable AI model selection
- Extensive logging and error handling

### Features
- **AI Integration**: Seamless integration with Anthropic's Claude API
- **Schema Analysis**: Intelligent parsing of DDN schema structures
- **Relationship Detection**: Multiple algorithms for relationship identification
- **Batch Processing**: Efficient processing of large schema repositories
- **Configuration**: Flexible configuration via environment variables or CLI
- **Extensibility**: Modular architecture for easy extension

### Supported Formats
- Hasura DDN HML files
- Standard YAML schema files
- OpenDD kind definitions (ObjectType, Model, Relationship, etc.)

### Requirements
- Python >= 3.8
- Anthropic API key
- DDN schema files in supported format
