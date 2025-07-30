#!/usr/bin/env python3

"""
Text processing utilities for Metadata Bootstrap.
Contains functions for text formatting, refinement, and manipulation.
"""

from typing import Optional


def refine_ai_description(desc: str) -> str:
    """
    Refine AI-generated descriptions by cleaning up common issues.

    Args:
        desc: The description to refine

    Returns:
        Cleaned and refined description
    """
    if not desc:
        return ""

    desc = desc.strip()

    # Remove trailing ellipsis
    if desc.endswith("..."):
        desc = desc[:-3].strip()

    # Remove trailing conjunctions
    common_conjunctions = ["and", "or", "but", "so", "yet", "for"]
    for conj in common_conjunctions:
        if desc.endswith(f" {conj}."):
            desc = desc[:-(len(conj) + 2)].strip()
        elif desc.endswith(f" {conj}"):
            desc = desc[:-(len(conj) + 1)].strip()

    # Remove trailing punctuation that shouldn't end a sentence
    if desc.endswith((",", "-", ";")):
        desc = desc[:-1].strip()

    # Ensure proper sentence ending
    if desc and not desc.endswith(('.', '!', '?')):
        desc += '.'

    return desc.strip()


def clean_description_response(text: str) -> str:
    """
    Clean AI response text by removing prefatory phrases and improving efficiency.

    Args:
        text: Raw AI response text

    Returns:
        Cleaned text with prefatory phrases removed
    """
    if not text:
        return text

    # Remove common prefatory patterns
    prefatory_patterns = [
        "Here's a more concise description", "Here's a description", "Here is a description",
        "A description for", "A concise description", "The description for", "Description:"
    ]

    for pattern in prefatory_patterns:
        if text.startswith(pattern):
            colon_pos = text.find(':')
            if colon_pos > 0:
                return text[colon_pos + 1:].lstrip()

            # Look for sentence break after pattern
            for i, char in enumerate(text):
                if i > len(pattern) and char in ['.', '!', '?'] and i + 1 < len(text) and text[i + 1] == ' ':
                    return text[i + 2:].lstrip()

    # Remove token-inefficient phrases
    token_inefficient_phrases = [
        "This element is responsible for ", "This element is used to ", "This element enables ",
        "This object is used to ", "This object is responsible for ", "This is used to ",
        "This is responsible for ", "specifically ", "essentially ", " in order to ",
        "This type is used for ", "This component ", "This module "
    ]

    for phrase in token_inefficient_phrases:
        if text.startswith(phrase):
            if len(text) > len(phrase):
                text = text[0].upper() + text[1:len(phrase)] + text[len(phrase):]
        text = text.replace(phrase, " ")

    # Additional replacements for efficiency
    text = text.replace(" in order to ", " to ").replace(" for the purpose of ", " for ")
    text = text.replace(" is utilized to ", " ").replace(" is designed to ", " ")

    # Clean up multiple spaces
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def normalize_description(description: str, line_length: Optional[int] = None,
                          make_token_efficient: Optional[bool] = None) -> str:
    """
    Normalize description formatting with line wrapping and token efficiency.

    Args:
        description: The description to normalize
        line_length: Maximum line length (default: 65)
        make_token_efficient: Whether to apply token efficiency improvements (default: True)

    Returns:
        Normalized description with proper formatting
    """
    if not description:
        return description

    if line_length is None:
        line_length = 65
    if make_token_efficient is None:
        make_token_efficient = True

    # Apply token efficiency improvements
    if make_token_efficient:
        token_inefficient_pairs = [
            (" in order to ", " to "), (" for the purpose of ", " for "),
            (" is utilized to ", " "), (" is designed to ", " "),
            (" specifically ", " "), (" essentially ", " "),
            (" in particular", ""), (", specifically,", ","),
            (", essentially,", ","), (", in particular,", ","),
            (" that is used to ", " that "), (" which is used to ", " which "),
            (" that are used to ", " that "), (" which are used to ", " which "),
            ("This element provides ", "Provides "), ("This element enables ", "Enables "),
            ("This element allows ", "Allows "), ("This component ", ""),
            ("This object ", ""), ("This model ", ""), ("This type ", ""),
        ]

        for old, new in token_inefficient_pairs:
            description = description.replace(old, new)

        # Clean up multiple spaces
        while "  " in description:
            description = description.replace("  ", " ")

    lines = description.splitlines()
    has_paragraphs = len(lines) > 2 and any(not line.strip() for line in lines)

    if has_paragraphs:
        result = []
        current_paragraph = []

        for line in lines:
            if not line.strip():
                if current_paragraph:
                    result.append(wrap_text(' '.join(current_paragraph), line_length))
                current_paragraph = []
                result.append('')
            else:
                current_paragraph.append(line.strip())

        if current_paragraph:
            result.append(wrap_text(' '.join(current_paragraph), line_length))

        return '\n'.join(result)
    else:
        text = ' '.join(line.strip() for line in lines)
        return wrap_text(text, line_length)


def wrap_text(text: str, line_length: int) -> str:
    """
    Wrap text to specified line length, breaking at word boundaries.

    Args:
        text: Text to wrap
        line_length: Maximum line length

    Returns:
        Text wrapped to specified length
    """
    if len(text) <= line_length:
        return text

    result = []
    remaining = text

    while remaining:
        if len(remaining) <= line_length:
            result.append(remaining)
            break

        # Find last space within line length
        cut_point = remaining[:line_length].rfind(' ')
        if cut_point == -1:  # No space found, cut at line length
            cut_point = line_length

        result.append(remaining[:cut_point])
        remaining = remaining[cut_point:].strip()

    return '\n'.join(result)


def to_camel_case(snake_str: str, first_char_lowercase: bool = True) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: String in snake_case format
        first_char_lowercase: Whether first character should be lowercase

    Returns:
        String in camelCase format
    """
    if not snake_str:
        return snake_str

    parts = snake_str.split('_')
    if not parts:
        return snake_str

    if len(parts) == 1:
        if first_char_lowercase:
            return parts[0][0].lower() + parts[0][1:] if parts[0] else ""
        else:
            return parts[0].capitalize() if parts[0] else ""

    if first_char_lowercase:
        return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
    else:
        return "".join(p.capitalize() for p in parts)


def smart_pluralize(word: str) -> str:
    """
    Intelligently pluralize a word, avoiding double pluralization.

    Args:
        word: The word to pluralize

    Returns:
        The pluralized form of the word
    """
    if not word:
        return word

    word_lower = word.lower()

    # Common plural endings - if word already ends with these, don't add 's'
    plural_endings = [
        'ies', 'es', 'ves', 'ren', 'feet', 'geese', 'mice', 'teeth',
        'data', 'criteria', 'phenomena', 'alumni'
    ]

    # Check if already plural
    if any(word_lower.endswith(ending) for ending in plural_endings):
        return word

    # If already ends with 's', likely already plural
    if word_lower.endswith('s'):
        # But check for exceptions that do take 's' even when ending in 's'
        exceptions = ['focus', 'bus', 'gas', 'class', 'pass', 'mass', 'grass', 'glass']
        if not any(word_lower.endswith(exc) for exc in exceptions):
            return word

    # Standard pluralization rules
    if word_lower.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        # city -> cities
        return word[:-1] + 'ies'
    elif word_lower.endswith(('s', 'sh', 'ch', 'x', 'z')):
        # bus -> buses, dish -> dishes, church -> churches
        return word + 'es'
    elif word_lower.endswith('f'):
        # leaf -> leaves
        return word[:-1] + 'ves'
    elif word_lower.endswith('fe'):
        # life -> lives
        return word[:-2] + 'ves'
    elif word_lower.endswith('o') and len(word) > 1 and word[-2] not in 'aeiou':
        # hero -> heroes (but photo -> photos)
        return word + 'es'
    else:
        # Default: just add 's'
        return word + 's'
