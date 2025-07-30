#!/usr/bin/env python3

"""
WordNet-based generic term detection with minimal hardcoding.
Uses linguistic analysis to determine term specificity and context disambiguation.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

# Optional import - gracefully handle if not available
try:
    import ssl

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    import nltk
    from nltk.corpus import wordnet as wn

    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available - falling back to basic heuristics")


@dataclass
class TermAnalysis:
    """Analysis result for a single term."""
    word: str
    is_generic: bool
    specificity_score: float  # 0.0 = very generic, 1.0 = very specific
    abstraction_level: int  # Higher = more abstract
    definition_quality: str  # 'specific', 'generic', 'abstract'
    reasoning: str


class WordNetGenericDetector:
    """WordNet-based generic term detection with linguistic analysis."""

    def __init__(self):
        self._ensure_wordnet()

        # Minimal hardcoded exceptions (truly unavoidable cases)
        self._always_generic = {'thing', 'stuff', 'data', 'info', 'item'}  # Reduced to bare minimum
        self._never_generic = {'user', 'name', 'email', 'phone', 'date'}  # Common specific terms

    @staticmethod
    def _ensure_wordnet():
        """Ensure WordNet data is available."""
        if not NLTK_AVAILABLE:
            return

        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            print("Downloading WordNet...")
            nltk.download('wordnet', quiet=True)

    def assess_field_name_clarity(self, field_name: str) -> Dict[str, Any]:
        """Enhanced field name clarity assessment using WordNet."""
        components = self._split_field_name(field_name)
        issues = []

        # Basic structural checks
        if len(field_name) <= 3:
            vowel_count = sum(1 for c in field_name.lower() if c in 'aeiou')
            if vowel_count == 0:
                issues.append("Very short with no vowels - likely cryptic")

        # Analyze each component for genericity
        term_analyses = [self.analyze_term(comp) for comp in components]
        generic_analysis = self._analyze_component_interactions(term_analyses)

        if generic_analysis['has_unresolved_generic']:
            issues.extend(generic_analysis['issues'])

        return {
            'is_clear': len(issues) == 0,
            'issues': issues,
            'generic_analysis': generic_analysis,
            'term_analyses': [vars(ta) for ta in term_analyses]  # For debugging
        }

    def analyze_term(self, word: str) -> TermAnalysis:
        """Analyze a single term for genericity using WordNet."""
        word_lower = word.lower()

        # Check hardcoded exceptions first (minimal set)
        if word_lower in self._always_generic:
            return TermAnalysis(
                word=word,
                is_generic=True,
                specificity_score=0.0,
                abstraction_level=10,
                definition_quality='generic',
                reasoning='Known generic term'
            )

        if word_lower in self._never_generic:
            return TermAnalysis(
                word=word,
                is_generic=False,
                specificity_score=1.0,
                abstraction_level=1,
                definition_quality='specific',
                reasoning='Known specific term'
            )

        # Use WordNet analysis
        if NLTK_AVAILABLE:
            return self._analyze_with_wordnet(word_lower)
        else:
            return self._analyze_with_heuristics(word_lower)

    def _analyze_with_wordnet(self, word: str) -> TermAnalysis:
        """Comprehensive WordNet-based analysis."""
        try:
            synsets = wn.synsets(word)
            if not synsets:
                return self._create_unknown_analysis(word)

            # Analyze multiple dimensions
            specificity_scores = []
            abstraction_levels = []
            definition_qualities = []

            for synset in synsets[:3]:  # Top 3 most common meanings
                spec_score, abs_level, def_quality = self._analyze_synset(synset)
                specificity_scores.append(spec_score)
                abstraction_levels.append(abs_level)
                definition_qualities.append(def_quality)

            # Use the most specific interpretation (benefit of doubt)
            max_specificity = max(specificity_scores)
            min_abstraction = min(abstraction_levels)
            best_quality = self._select_best_quality(definition_qualities)

            is_generic = max_specificity < 0.4  # Threshold for genericity

            reasoning = self._build_reasoning(synsets[:3], specificity_scores, abstraction_levels)

            return TermAnalysis(
                word=word,
                is_generic=is_generic,
                specificity_score=max_specificity,
                abstraction_level=min_abstraction,
                definition_quality=best_quality,
                reasoning=reasoning
            )

        except Exception as e:
            return TermAnalysis(
                word=word,
                is_generic=False,  # Conservative: assume specific if unsure
                specificity_score=0.5,
                abstraction_level=5,
                definition_quality='unknown',
                reasoning=f'WordNet error: {str(e)}'
            )

    def _analyze_synset(self, synset) -> Tuple[float, int, str]:
        """Analyze a single synset for specificity."""
        definition = synset.definition().lower()

        # 1. Definition analysis
        specificity_from_def = self._analyze_definition_specificity(definition)

        # 2. Taxonomic position analysis
        abstraction_level = self._calculate_abstraction_level(synset)

        # 3. Hyponym analysis (how many specific things fall under this concept)
        hyponym_count = len(list(synset.closure(lambda s: s.hyponyms())))
        specificity_from_hyponyms = min(1.0, hyponym_count / 100.0)  # Normalize

        # 4. Lexical relations analysis
        relation_specificity = self._analyze_lexical_relations(synset)

        # Combine scores
        overall_specificity = (
                specificity_from_def * 0.4 +
                (1.0 - min(abstraction_level / 10.0, 1.0)) * 0.3 +
                specificity_from_hyponyms * 0.2 +
                relation_specificity * 0.1
        )

        # Determine quality category
        if overall_specificity > 0.7:
            quality = 'specific'
        elif overall_specificity > 0.3:
            quality = 'moderate'
        else:
            quality = 'generic'

        return overall_specificity, abstraction_level, quality

    def _analyze_definition_specificity(self, definition: str) -> float:
        """Analyze definition specificity using linguistic patterns and WordNet."""
        words = definition.split()

        # 1. Analyze grammatical structure
        structure_score = self._analyze_grammatical_structure(words)

        # 2. Analyze semantic density using WordNet
        semantic_score = self._analyze_semantic_density(words)

        # 3. Analyze definitional patterns
        pattern_score = self._analyze_definitional_patterns(definition)

        # 4. Analyze concept concreteness
        concreteness_score = self._analyze_concreteness(words)

        # Combine scores with weights
        overall_score = (
                structure_score * 0.25 +
                semantic_score * 0.35 +
                pattern_score * 0.25 +
                concreteness_score * 0.15
        )

        return max(0.0, min(1.0, overall_score))

    @staticmethod
    def _analyze_grammatical_structure(words: List[str]) -> float:
        """Analyze grammatical complexity as indicator of specificity."""
        if not words:
            return 0.0

        # Longer definitions with more detail tend to be more specific
        length_factor = min(len(words) / 15.0, 1.0)

        # Count content words vs function words
        function_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                          'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                          'should', 'may', 'might', 'can', 'must', 'shall', 'to', 'of', 'in',
                          'on', 'at', 'by', 'for', 'with', 'from', 'up', 'about', 'into',
                          'through', 'during', 'before', 'after', 'above', 'below', 'between'}

        content_words = [w for w in words if w.lower() not in function_words]
        content_ratio = len(content_words) / len(words) if words else 0

        # Combine factors
        return length_factor * 0.6 + content_ratio * 0.4

    @staticmethod
    def _analyze_semantic_density(words: List[str]) -> float:
        """Analyze semantic richness using WordNet relationships."""
        if not NLTK_AVAILABLE or not words:
            return 0.5

        try:
            # Get synsets for definition words
            word_synsets = []
            for word in words:
                if len(word) > 3:  # Skip very short words
                    synsets = wn.synsets(word.lower())
                    if synsets:
                        word_synsets.append((word, synsets[0]))  # Use primary meaning

            if not word_synsets:
                return 0.3

            # Calculate semantic relationships between words in definition
            relationship_count = 0
            total_pairs = 0

            for i, (word1, synset1) in enumerate(word_synsets):
                for word2, synset2 in word_synsets[i + 1:]:
                    total_pairs += 1

                    # Check for semantic relationships
                    similarity = synset1.path_similarity(synset2)
                    if similarity and similarity > 0.1:  # Some relationship exists
                        relationship_count += similarity

            if total_pairs == 0:
                return 0.3

            # High interconnectedness suggests rich, specific meaning
            density = relationship_count / total_pairs
            return min(1.0, density * 2.0)  # Scale up since similarities are often low

        except Exception:
            return 0.5

    def _analyze_definitional_patterns(self, definition: str) -> float:
        """Analyze definitional patterns without hardcoded word lists."""
        # Circular definitions (defining with same root) are often generic
        # E.g., "data is information" or "information is data"
        words = definition.lower().split()

        # Check for circular patterns
        root_repetition = self._check_root_repetition(words)

        # Check for vague quantifiers (detected by POS patterns)
        vague_quantification = self._check_vague_quantification(definition)

        # Check for categorical vs functional definitions
        categorical_strength = self._check_categorical_definition(definition)

        # Combine pattern analysis
        specificity = 1.0
        specificity -= root_repetition * 0.4
        specificity -= vague_quantification * 0.3
        specificity += categorical_strength * 0.2

        return max(0.0, min(1.0, specificity))

    @staticmethod
    def _check_root_repetition(words: List[str]) -> float:
        """Check for root word repetition in definition."""

        # Simple stemming: remove common suffixes
        def simple_stem(word):
            suffixes = ['ing', 'ed', 'er', 'est', 'ly', 'tion', 'sion', 'ness', 'ment']
            for suffix in suffixes:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    return word[:-len(suffix)]
            return word

        stems = [simple_stem(word) for word in words if len(word) > 3]
        if not stems:
            return 0.0

        # Count repeated stems
        from collections import Counter
        stem_counts = Counter(stems)
        repeated = sum(1 for count in stem_counts.values() if count > 1)

        return min(1.0, repeated / len(set(stems)))

    @staticmethod
    def _check_vague_quantification(definition: str) -> float:
        """Check for vague quantification patterns."""
        # Pattern-based detection of indefinite language
        patterns = [
            r'\bsome\b.*\bof\b',  # "some of"
            r'\bmany\b.*\btypes?\b',  # "many types"
            r'\bvarious\b.*\bforms?\b',  # "various forms"
            r'\ba\s+(?:type|kind|form|sort)\s+of\b',  # "a type of"
            r'\bany\b.*\bthat\b',  # "any ... that"
        ]

        vague_count = sum(1 for pattern in patterns if re.search(pattern, definition, re.IGNORECASE))
        return min(1.0, vague_count / 3.0)  # Normalize

    @staticmethod
    def _check_categorical_definition(definition: str) -> float:
        """Check for strong categorical (specific) definition patterns."""
        # Strong categorical patterns suggest specificity
        strong_patterns = [
            r'\bis\s+(?:a|an)\s+[a-z]+\s+(?:that|which|used)',  # "is an X that/which/used"
            r'\brefers\s+to\s+(?:a|an|the)\s+specific',         # "refers to a specific"
            r'\bdenotes\s+(?:a|an|the)',                        # "denotes a/an/the"
            r'\bmeans\s+(?:a|an|the)\s+[a-z]+',                 # "means an X"
        ]

        strong_count = sum(1 for pattern in strong_patterns if re.search(pattern, definition, re.IGNORECASE))
        return min(1.0, strong_count / 2.0)

    @staticmethod
    def _analyze_concreteness(words: List[str]) -> float:
        """Analyze concreteness vs abstractness of definition words."""
        if not NLTK_AVAILABLE or not words:
            return 0.5

        try:
            concrete_score = 0.0
            analyzed_words = 0

            for word in words:
                if len(word) > 3:  # Skip short function words
                    synsets = wn.synsets(word.lower())
                    if synsets:
                        # Check if word has physical/concrete meanings
                        for synset in synsets[:2]:  # Check top 2 meanings
                            # Physical objects tend to have part meronyms
                            meronyms = list(synset.part_meronyms())
                            if meronyms:
                                concrete_score += 0.8
                                break

                            # Check lexical domain for concrete categories
                            lexname = synset.lexname()
                            if any(domain in lexname for domain in
                                   ['noun.artifact', 'noun.object', 'noun.substance',
                                    'noun.body', 'noun.food', 'noun.animal', 'noun.plant']):
                                concrete_score += 0.6
                                break
                        analyzed_words += 1

            if analyzed_words == 0:
                return 0.5

            return concrete_score / analyzed_words

        except Exception:
            return 0.5

    @staticmethod
    def _calculate_abstraction_level(synset) -> int:
        """Calculate how abstract a concept is based on taxonomic position."""
        try:
            # Count steps to root
            paths_to_root = synset.hypernym_paths()
            if not paths_to_root:
                return 5  # Middle level if no hypernyms

            # Use the shortest path (most direct route to root)
            min_depth = min(len(path) for path in paths_to_root)

            # Convert to abstraction level (fewer steps = more abstract)
            return max(1, 12 - min_depth)  # Invert: closer to root = higher abstraction

        except Exception:
            return 5  # Default middle level

    @staticmethod
    def _analyze_lexical_relations(synset) -> float:
        """Analyze lexical relations to determine specificity."""
        try:
            # More meronyms (parts) suggests concrete concepts
            meronyms = len(list(synset.part_meronyms()))

            # More similar_tos suggests rich semantic network
            similar_tos = len(list(synset.similar_tos()))

            # Combine relation counts
            relation_score = min(1.0, (meronyms + similar_tos) / 10.0)

            return relation_score

        except Exception:
            return 0.5

    @staticmethod
    def _analyze_with_heuristics(word: str) -> TermAnalysis:
        """Fallback heuristic analysis when WordNet unavailable."""
        # Basic heuristics for common patterns
        if len(word) <= 2:
            return TermAnalysis(word, True, 0.2, 8, 'generic', 'Very short word')

        # Common patterns that indicate specificity
        specific_patterns = [
            r'.*[a-z]+er$',    # agent nouns (user, server, etc.)
            r'.*[a-z]+ed$',    # past participles (created, updated)
            r'.*[a-z]+ing$',   # present participles (pending, running)
            r'.*[a-z]+tion$',  # abstract nouns but often specific (creation, deletion)
        ]

        for pattern in specific_patterns:
            if re.match(pattern, word):
                return TermAnalysis(word, False, 0.7, 3, 'specific', f'Matches pattern {pattern}')

        # Default to moderately specific
        return TermAnalysis(word, False, 0.6, 4, 'moderate', 'Heuristic analysis')

    def _analyze_component_interactions(self, term_analyses: List[TermAnalysis]) -> Dict[str, Any]:
        """Analyze how components interact to create meaning."""
        generic_terms = [ta for ta in term_analyses if ta.is_generic]
        specific_terms = [ta for ta in term_analyses if not ta.is_generic]

        if not generic_terms:
            return {
                'has_generic': False,
                'has_unresolved_generic': False,
                'issues': []
            }

        # Check if generic terms are disambiguated by specific terms
        disambiguated = []
        unresolved = []

        for generic_term in generic_terms:
            if self._is_disambiguated_by_context(generic_term, specific_terms):
                disambiguated.append(generic_term.word)
            else:
                unresolved.append(generic_term.word)

        issues = []
        if unresolved:
            issues.append(f"Contains unresolved generic terms: {', '.join(unresolved)}")

        return {
            'has_generic': True,
            'has_unresolved_generic': len(unresolved) > 0,
            'generic_terms': [ta.word for ta in generic_terms],
            'disambiguated_terms': disambiguated,
            'unresolved_terms': unresolved,
            'issues': issues
        }

    @staticmethod
    def _is_disambiguated_by_context(generic_term: TermAnalysis, specific_terms: List[TermAnalysis]) -> bool:
        """Check if a generic term is disambiguated by other specific terms."""
        if not specific_terms:
            return False

        # If there's at least one highly specific term, it likely disambiguates
        has_highly_specific = any(ta.specificity_score > 0.7 for ta in specific_terms)

        # If the generic term isn't extremely generic, context might help
        moderately_generic = generic_term.specificity_score > 0.2

        return has_highly_specific and moderately_generic

    @staticmethod
    def _split_field_name(field_name: str) -> List[str]:
        """Split field name into components."""
        if '_' in field_name:
            parts = field_name.split('_')
            processed_parts = []
            for part in parts:
                if part and any(c.isupper() for c in part[1:]):
                    processed_parts.extend(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|$)', part))
                else:
                    processed_parts.append(part)
            return [part.lower() for part in processed_parts if part]
        else:
            parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|$)', field_name)
            return [part.lower() for part in parts if part]

    @staticmethod
    def _create_unknown_analysis(word: str) -> TermAnalysis:
        """Create analysis for unknown words."""
        return TermAnalysis(
            word=word,
            is_generic=False,  # Conservative: assume specific
            specificity_score=0.5,
            abstraction_level=5,
            definition_quality='unknown',
            reasoning='Word not found in WordNet'
        )

    @staticmethod
    def _select_best_quality(qualities: List[str]) -> str:
        """Select the best definition quality from a list."""
        if 'specific' in qualities:
            return 'specific'
        elif 'moderate' in qualities:
            return 'moderate'
        elif 'generic' in qualities:
            return 'generic'
        else:
            return 'unknown'

    @staticmethod
    def _build_reasoning(synsets, specificity_scores, abstraction_levels) -> str:
        """Build human-readable reasoning for the analysis."""
        if not synsets:
            return "No definitions found"

        best_synset = synsets[0]
        best_score = max(specificity_scores)
        avg_abstraction = sum(abstraction_levels) / len(abstraction_levels)

        parts = [f"Primary meaning: '{best_synset.definition()}'"]

        if best_score > 0.7:
            parts.append("High specificity from definition analysis")
        elif best_score < 0.3:
            parts.append("Low specificity - generic language in definition")

        if avg_abstraction > 7:
            parts.append("High abstraction level in taxonomy")
        elif avg_abstraction < 3:
            parts.append("Concrete concept in taxonomy")

        return "; ".join(parts)


# Simple test
def test_wordnet_detector():
    """Test the WordNet-based detector."""
    detector = WordNetGenericDetector()

    test_cases = [
        "user_data", "customer_info", "data_value", "server_config",
        "item_thing", "user_name", "payment_amount", "account_type"
    ]

    print("WordNet-Based Generic Detection:")
    print("=" * 40)

    for field_name in test_cases:
        analysis = detector.assess_field_name_clarity(field_name)
        print(f"\n{field_name}: {'CLEAR' if analysis['is_clear'] else 'UNCLEAR'}")

        if 'generic_analysis' in analysis:
            ga = analysis['generic_analysis']
            if ga['has_generic']:
                print(f"  Generic: {ga['generic_terms']}")
                if ga['disambiguated_terms']:
                    print(f"  Disambiguated: {ga['disambiguated_terms']}")
                if ga['unresolved_terms']:
                    print(f"  Unresolved: {ga['unresolved_terms']}")


if __name__ == "__main__":
    test_wordnet_detector()
