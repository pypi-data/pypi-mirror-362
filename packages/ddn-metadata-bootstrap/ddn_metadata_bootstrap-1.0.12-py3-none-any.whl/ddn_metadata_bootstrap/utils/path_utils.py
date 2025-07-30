#!/usr/bin/env python3

"""
Path and file system utilities for Metadata Bootstrap.
Contains functions for path manipulation, file discovery, and directory operations.
"""

import glob
import logging
import os
import shutil
from pathlib import Path
from typing import List, Optional, Iterator, Set, Dict

logger = logging.getLogger(__name__)


def extract_subgraph_from_path(file_path: str) -> Optional[str]:
    """
    Extract subgraph name from file path.

    Looks for 'metadata' directory and returns the parent directory name,
    which typically represents the subgraph name in Hasura DDN structure.

    Args:
        file_path: Path to analyze

    Returns:
        Subgraph name or None if not found

    Example:
        'project/users/metadata/Users.hml' -> 'users'
        'app/inventory/metadata/Products.hml' -> 'inventory'
    """
    parts = Path(file_path).parts

    try:
        metadata_index = parts.index("metadata")
        if metadata_index > 0:
            return parts[metadata_index - 1]
    except ValueError:
        # 'metadata' not found in path
        pass

    return None


def find_hml_files(directory: str, pattern: str = "**/metadata/*.hml") -> List[str]:
    """
    Find all HML files in a directory using a glob pattern.

    Args:
        directory: Root directory to search
        pattern: Glob pattern for file matching

    Returns:
        List of absolute file paths
    """
    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern, recursive=True)

    # Convert to absolute paths and sort for consistent ordering
    absolute_files = [os.path.abspath(f) for f in files]
    absolute_files.sort()

    logger.debug(f"Found {len(absolute_files)} HML files in {directory}")
    return absolute_files


def find_files_by_extension(directory: str, extensions: List[str],
                            recursive: bool = True) -> List[str]:
    """
    Find files by extension(s) in a directory.

    Args:
        directory: Directory to search
        extensions: List of file extensions (with or without dots)
        recursive: Whether to search subdirectories

    Returns:
        List of matching file paths
    """
    files = []

    # Normalize extensions
    normalized_exts = []
    for ext in extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        normalized_exts.append(ext.lower())

    if recursive:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in normalized_exts):
                    files.append(os.path.join(root, filename))
    else:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if any(item.lower().endswith(ext) for ext in normalized_exts):
                    files.append(item_path)

    files.sort()
    logger.debug(f"Found {len(files)} files with extensions {extensions} in {directory}")
    return files


def create_directory_structure(file_path: str) -> None:
    """
    Create directory structure for a file path if it doesn't exist.

    Args:
        file_path: File path for which to create parent directories
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def copy_file_with_structure(source: str, destination: str) -> None:
    """
    Copy a file to destination, creating directory structure if needed.

    Args:
        source: Source file path
        destination: Destination file path
    """
    create_directory_structure(destination)
    shutil.copy2(source, destination)
    logger.debug(f"Copied {source} -> {destination}")


def get_relative_path(file_path: str, base_dir: str) -> str:
    """
    Get relative path from base directory.

    Args:
        file_path: Absolute or relative file path
        base_dir: Base directory

    Returns:
        Relative path from base directory
    """
    return os.path.relpath(file_path, base_dir)


def normalize_path(path: str) -> str:
    """
    Normalize a path by resolving relative components and symbolic links.

    Args:
        path: Path to normalize

    Returns:
        Normalized absolute path
    """
    return os.path.abspath(os.path.normpath(path))


def is_same_file(path1: str, path2: str) -> bool:
    """
    Check if two paths refer to the same file.

    Args:
        path1: First file path
        path2: Second file path

    Returns:
        True if paths refer to the same file
    """
    try:
        return os.path.samefile(path1, path2)
    except (OSError, FileNotFoundError):
        # Fall back to comparing normalized paths
        return normalize_path(path1) == normalize_path(path2)


def filter_existing_files(file_paths: List[str]) -> List[str]:
    """
    Filter a list of file paths to only include existing files.

    Args:
        file_paths: List of file paths to check

    Returns:
        List of existing file paths
    """
    existing = [path for path in file_paths if os.path.isfile(path)]

    missing_count = len(file_paths) - len(existing)
    if missing_count > 0:
        logger.warning(f"Filtered out {missing_count} non-existent files")

    return existing


def group_files_by_directory(file_paths: List[str]) -> Dict[str, List[str]]:
    """
    Group file paths by their parent directory.

    Args:
        file_paths: List of file paths

    Returns:
        Dictionary mapping directory paths to lists of files
    """
    groups = {}

    for file_path in file_paths:
        directory = os.path.dirname(file_path)
        if directory not in groups:
            groups[directory] = []
        groups[directory].append(file_path)

    return groups


def group_files_by_subgraph(file_paths: List[str]) -> Dict[Optional[str], List[str]]:
    """
    Group file paths by their inferred subgraph.

    Args:
        file_paths: List of file paths

    Returns:
        Dictionary mapping subgraph names to lists of files
    """
    groups = {}

    for file_path in file_paths:
        subgraph = extract_subgraph_from_path(file_path)
        if subgraph not in groups:
            groups[subgraph] = []
        groups[subgraph].append(file_path)

    return groups


def ensure_output_directory(input_path: str, output_dir: str,
                            input_base_dir: str) -> str:
    """
    Ensure output directory structure matches input structure.

    Args:
        input_path: Input file path
        output_dir: Output base directory
        input_base_dir: Input base directory

    Returns:
        Output file path with proper directory structure
    """
    relative_path = get_relative_path(input_path, input_base_dir)
    output_path = os.path.join(output_dir, relative_path)
    create_directory_structure(output_path)
    return output_path


def walk_directories(root_dir: str, exclude_patterns: Optional[List[str]] = None) -> Iterator[
    tuple[str, List[str], List[str]]]:
    """
    Walk directory tree with optional exclusion patterns.

    Args:
        root_dir: Root directory to walk
        exclude_patterns: List of patterns to exclude (supports glob-style wildcards)

    Yields:
        Tuples of (dirpath, dirnames, filenames) like os.walk()
    """
    import fnmatch  # Add this import

    exclude_patterns = exclude_patterns or []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames
                       if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]

        # Filter out excluded files
        filtered_files = [f for f in filenames
                          if not any(fnmatch.fnmatch(f, pattern) for pattern in exclude_patterns)]

        yield dirpath, dirnames, filtered_files

def get_file_stats(file_paths: List[str]) -> Dict[str, int]:
    """
    Get statistics about a collection of files.

    Args:
        file_paths: List of file paths

    Returns:
        Dictionary with file statistics
    """
    stats = {
        'total_files': len(file_paths),
        'existing_files': 0,
        'total_size_bytes': 0,
        'by_extension': {},
        'by_directory': {},
        'by_subgraph': {}
    }

    for file_path in file_paths:
        if os.path.isfile(file_path):
            stats['existing_files'] += 1

            # File size
            try:
                stats['total_size_bytes'] += os.path.getsize(file_path)
            except OSError:
                pass

            # Extension
            ext = os.path.splitext(file_path)[1].lower()
            stats['by_extension'][ext] = stats['by_extension'].get(ext, 0) + 1

            # Directory
            directory = os.path.dirname(file_path)
            stats['by_directory'][directory] = stats['by_directory'].get(directory, 0) + 1

            # Subgraph
            subgraph = extract_subgraph_from_path(file_path)
            subgraph_key = subgraph or '<no_subgraph>'
            stats['by_subgraph'][subgraph_key] = stats['by_subgraph'].get(subgraph_key, 0) + 1

    return stats


class FileCollector:
    """
    Helper class for collecting and organizing files for processing.
    """

    def __init__(self, base_directory: str, file_pattern: str = "**/metadata/*.hml"):
        """
        Initialize file collector.

        Args:
            base_directory: Base directory to search
            file_pattern: Glob pattern for file matching
        """
        self.base_directory = normalize_path(base_directory)
        self.file_pattern = file_pattern
        self.excluded_files: Set[str] = set()
        self.included_files: Set[str] = set()

    def add_exclusion(self, filename: str) -> None:
        """Add a filename to the exclusion list."""
        self.excluded_files.add(filename)

    def add_inclusion(self, filename: str) -> None:
        """Add a filename to the inclusion list (overrides exclusions)."""
        self.included_files.add(filename)

    def collect_files(self) -> List[str]:
        """
        Collect files according to configured patterns and filters.

        Returns:
            List of file paths to process
        """
        all_files = find_hml_files(self.base_directory, self.file_pattern)
        filtered_files = []
        excluded_count = 0

        for file_path in all_files:
            filename = os.path.basename(file_path)

            # Check inclusion list first (overrides exclusions)
            if filename in self.included_files:
                filtered_files.append(file_path)
                continue

            # Check exclusion list
            if filename in self.excluded_files:
                excluded_count += 1
                continue

            filtered_files.append(file_path)

        logger.info(f"Collected {len(filtered_files)} files for processing "
                    f"({excluded_count} excluded)")

        return filtered_files

    def get_subgraph_summary(self, file_paths: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Get summary of files by subgraph.

        Args:
            file_paths: Optional list of file paths (defaults to collected files)

        Returns:
            Dictionary mapping subgraph names to file counts
        """
        if file_paths is None:
            file_paths = self.collect_files()

        subgraph_groups = group_files_by_subgraph(file_paths)
        return {k or '<no_subgraph>': len(v) for k, v in subgraph_groups.items()}


def safe_remove_file(file_path: str) -> bool:
    """
    Safely remove a file, logging any errors.

    Args:
        file_path: Path to file to remove

    Returns:
        True if file was removed successfully, False otherwise
    """
    try:
        os.remove(file_path)
        logger.debug(f"Removed file: {file_path}")
        return True
    except OSError as e:
        logger.warning(f"Could not remove file {file_path}: {e}")
        return False


def safe_move_file(source: str, destination: str) -> bool:
    """
    Safely move a file, creating destination directories as needed.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        True if file was moved successfully, False otherwise
    """
    try:
        create_directory_structure(destination)
        shutil.move(source, destination)
        logger.debug(f"Moved file: {source} -> {destination}")
        return True
    except (OSError, shutil.Error) as e:
        logger.warning(f"Could not move file {source} to {destination}: {e}")
        return False
