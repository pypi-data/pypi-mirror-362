#!/usr/bin/env python3

"""
YAML processing utilities for Metadata Bootstrap.
Contains functions for YAML loading, dumping, and document handling.
"""

import logging
import os
from typing import List, Any, Dict, Optional, Iterator

import yaml

logger = logging.getLogger(__name__)


def represent_multiline_str(dumper, data):
    """
    Custom YAML representer for multiline strings.

    Uses literal style (|) for strings containing newlines or carriage returns.
    This preserves the formatting of multiline descriptions.

    Args:
        dumper: YAML dumper instance
        data: String data to represent

    Returns:
        YAML scalar representation
    """
    if '\n' in data or '\r' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


# Register the custom representer
yaml.add_representer(str, represent_multiline_str)

_cache = {}


# Simplify: In rebuild mode, ALWAYS exclude relationships

def load_yaml_documents(file_path: str) -> List[Dict]:
    """Load YAML documents, filtering relationships in rebuild mode."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            documents = list(yaml.safe_load_all(file))
    except Exception as e:
        logger.error(f"Error loading YAML from {file_path}: {e}")
        return []

    # Filter relationships in rebuild mode
    from ..config import config
    if getattr(config, 'rebuild_all_relationships', False):
        filtered_docs = []
        relationships_filtered = 0

        for doc in documents:
            if isinstance(doc, dict) and doc.get('kind') == 'Relationship':
                relationships_filtered += 1
            else:
                filtered_docs.append(doc)

        if relationships_filtered > 0:
            logger.debug(f"🔄 REBUILD MODE: Filtered {relationships_filtered} relationships from {file_path}")

        return filtered_docs

    return documents


def save_yaml_documents(documents: List[Any], file_path: str,
                        create_dirs: bool = True) -> None:
    """
    Save YAML documents to a file.

    Args:
        documents: List of documents to save
        file_path: Output file path
        create_dirs: Whether to create parent directories if they don't exist

    Raises:
        OSError: If file operations fail
        yaml.YAMLError: If YAML serialization fails
    """
    try:
        # Create parent directories if needed
        if create_dirs:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump_all(documents, f, default_flow_style=False, sort_keys=False)

        logger.debug(f"Saved {len(documents)} documents to {file_path}")

    except OSError as e:
        logger.error(f"File operation error saving {file_path}: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML serialization error for {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving {file_path}: {e}")
        raise


def validate_yaml_document(document: Dict) -> tuple[bool, Optional[str]]:
    """
    Validate a YAML document structure.

    Args:
        document: YAML document to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(document, dict):
        return False, "Document must be a dictionary"

    # Check for required top-level structure
    if 'kind' not in document:
        return False, "Document missing 'kind' field"

    kind = document.get('kind')
    if not isinstance(kind, str):
        return False, "'kind' field must be a string"

    # Version field is often required
    if 'version' not in document:
        logger.warning(f"Document of kind '{kind}' missing 'version' field")

    return True, None


def filter_documents(documents: List[Dict],
                     include_kinds: Optional[List[str]] = None,
                     exclude_kinds: Optional[List[str]] = None,
                     include_names: Optional[List[str]] = None,
                     exclude_names: Optional[List[str]] = None) -> List[Dict]:
    """
    Filter YAML documents based on kind and name criteria.

    Args:
        documents: List of documents to filter
        include_kinds: Only include documents with these kinds
        exclude_kinds: Exclude documents with these kinds
        include_names: Only include documents with these names
        exclude_names: Exclude documents with these names

    Returns:
        Filtered list of documents
    """
    filtered = []

    for doc in documents:
        if not isinstance(doc, dict):
            continue

        kind = doc.get('kind')
        name = doc.get('definition', {}).get('name') if isinstance(doc.get('definition'), dict) else doc.get('name')

        # Apply kind filters
        if include_kinds and kind not in include_kinds:
            continue
        if exclude_kinds and kind in exclude_kinds:
            continue

        # Apply name filters
        if include_names and name not in include_names:
            continue
        if exclude_names and name in exclude_names:
            continue

        filtered.append(doc)

    logger.debug(f"Filtered {len(documents)} documents to {len(filtered)}")
    return filtered


def find_documents_by_kind(documents: List[Dict], kind: str) -> List[Dict]:
    """
    Find all documents of a specific kind.

    Args:
        documents: List of documents to search
        kind: Kind to search for

    Returns:
        List of documents matching the kind
    """
    return [doc for doc in documents
            if isinstance(doc, dict) and doc.get('kind') == kind]


def find_document_by_name(documents: List[Dict], name: str,
                          kind: Optional[str] = None) -> Optional[Dict]:
    """
    Find a document by name, optionally filtered by kind.

    Args:
        documents: List of documents to search
        name: Name to search for
        kind: Optional kind filter

    Returns:
        First matching document or None
    """
    for doc in documents:
        if not isinstance(doc, dict):
            continue

        doc_name = (doc.get('definition', {}).get('name')
                    if isinstance(doc.get('definition'), dict)
                    else doc.get('name'))

        if doc_name == name:
            if kind is None or doc.get('kind') == kind:
                return doc

    return None


def extract_document_names(documents: List[Dict]) -> List[str]:
    """
    Extract all document names from a list of documents.

    Args:
        documents: List of documents

    Returns:
        List of document names (excluding None values)
    """
    names = []
    for doc in documents:
        if not isinstance(doc, dict):
            continue

        name = (doc.get('definition', {}).get('name')
                if isinstance(doc.get('definition'), dict)
                else doc.get('name'))

        if name:
            names.append(name)

    return names


def merge_documents(base_documents: List[Dict],
                    additional_documents: List[Dict],
                    conflict_strategy: str = 'append') -> List[Dict]:
    """
    Merge two lists of YAML documents.

    Args:
        base_documents: Base list of documents
        additional_documents: Documents to merge in
        conflict_strategy: How to handle conflicts ('append', 'replace', 'skip')

    Returns:
        Merged list of documents
    """
    if conflict_strategy == 'append':
        return base_documents + additional_documents

    # For replace and skip strategies, we need to track by (kind, name)
    merged = []
    seen_signatures = set()

    # Process base documents first
    for doc in base_documents:
        if not isinstance(doc, dict):
            merged.append(doc)
            continue

        kind = doc.get('kind')
        name = (doc.get('definition', {}).get('name')
                if isinstance(doc.get('definition'), dict)
                else doc.get('name'))

        signature = (kind, name)
        seen_signatures.add(signature)
        merged.append(doc)

    # Process additional documents
    for doc in additional_documents:
        if not isinstance(doc, dict):
            merged.append(doc)
            continue

        kind = doc.get('kind')
        name = (doc.get('definition', {}).get('name')
                if isinstance(doc.get('definition'), dict)
                else doc.get('name'))

        signature = (kind, name)

        if signature in seen_signatures:
            if conflict_strategy == 'replace':
                # Find and replace the existing document
                for i, existing_doc in enumerate(merged):
                    if isinstance(existing_doc, dict):
                        existing_kind = existing_doc.get('kind')
                        existing_name = (existing_doc.get('definition', {}).get('name')
                                         if isinstance(existing_doc.get('definition'), dict)
                                         else existing_doc.get('name'))
                        if (existing_kind, existing_name) == signature:
                            merged[i] = doc
                            break
            # For 'skip' strategy, do nothing
        else:
            seen_signatures.add(signature)
            merged.append(doc)

    logger.debug(f"Merged {len(base_documents)} + {len(additional_documents)} = {len(merged)} documents")
    return merged


def get_document_summary(documents: List[Dict]) -> Dict[str, int]:
    """
    Get a summary of document types and counts.

    Args:
        documents: List of documents to summarize

    Returns:
        Dictionary mapping kinds to counts
    """
    summary = {}

    for doc in documents:
        if isinstance(doc, dict) and 'kind' in doc:
            kind = doc['kind']
            summary[kind] = summary.get(kind, 0) + 1

    return summary


def stream_yaml_documents(file_path: str) -> Iterator[Dict]:
    """
    Stream YAML documents from a file one at a time.

    Useful for processing large files without loading everything into memory.

    Args:
        file_path: Path to the YAML file

    Yields:
        Individual YAML documents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for doc in yaml.safe_load_all(f):
                if doc is not None:
                    yield doc
    except Exception as e:
        logger.error(f"Error streaming documents from {file_path}: {e}")
        raise


class YamlProcessor:
    """
    High-level YAML processing class with common operations.
    """

    def __init__(self, validate_on_load: bool = True):
        """
        Initialize YAML processor.

        Args:
            validate_on_load: Whether to validate documents when loading
        """
        self.validate_on_load = validate_on_load
        self.validation_errors = []

    def load_and_validate(self, file_path: str) -> List[Dict]:
        """
        Load YAML documents and optionally validate them.

        Args:
            file_path: Path to YAML file

        Returns:
            List of loaded (and validated) documents
        """
        documents = load_yaml_documents(file_path)

        if self.validate_on_load:
            validated_docs = []
            self.validation_errors = []

            for i, doc in enumerate(documents):
                if doc is None:
                    continue

                is_valid, error = validate_yaml_document(doc)
                if is_valid:
                    validated_docs.append(doc)
                else:
                    self.validation_errors.append(f"Document {i}: {error}")
                    logger.warning(f"Validation error in {file_path}, document {i}: {error}")

            return validated_docs

        return [doc for doc in documents if doc is not None]

    @staticmethod
    def save_with_backup(documents: List[Dict], file_path: str) -> None:
        """
        Save documents with backup of existing file.

        Args:
            documents: Documents to save
            file_path: Output file path
        """
        # Create backup if file exists
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup"
            try:
                os.rename(file_path, backup_path)
                logger.info(f"Created backup: {backup_path}")
            except OSError as e:
                logger.warning(f"Could not create backup of {file_path}: {e}")

        # Save new content
        save_yaml_documents(documents, file_path)

    def get_validation_errors(self) -> List[str]:
        """Get validation errors from last load operation."""
        return self.validation_errors.copy()
