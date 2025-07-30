import re
from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer, RecognizerResult, EntityRecognizer
from presidio_analyzer.nlp_engine import NlpArtifacts


class NamedPatternRecognizer(PatternRecognizer):
    def __init__(
            self,
            supported_entity: str,
            name: str = None,
            supported_language: str = "en",
            patterns: List[Pattern] = None,
            deny_list: List[str] = None,
            context: List[str] = None,
            deny_list_score: float = 1.0,
            global_regex_flags: Optional[int] = re.DOTALL | re.MULTILINE,
            version: str = "0.0.1",
    ):
        super().__init__(supported_entity, name, supported_language, patterns, deny_list, context, deny_list_score,
                         global_regex_flags, version)

    def analyze(
            self,
            text: str,
            entities: List[str],
            nlp_artifacts: Optional[NlpArtifacts] = None,
            regex_flags: Optional[int] = None,
    ) -> List[RecognizerResult]:
        """
        Analyzes text to detect PII using regular expressions or deny-lists.

        :param text: Text to be analyzed
        :param entities: Entities this recognizer can detect
        :param nlp_artifacts: Output values from the NLP engine
        :param regex_flags: regex flags to be used in regex matching
        :return:
        """
        results = []

        if self.patterns:
            pattern_result = self.__analyze_patterns(text, regex_flags)
            results.extend(pattern_result)

        return results

    def __analyze_patterns(
            self, text: str, flags: int = None
    ) -> List[RecognizerResult]:
        """
        Evaluate all patterns in the provided text.

        Including words in the provided deny-list

        :param text: text to analyze
        :param flags: regex flags
        :return: A list of RecognizerResult
        """
        flags = flags if flags else self.global_regex_flags
        results = []
        for pattern in self.patterns:
            # Compile regex if flags differ from flags the regex was compiled with
            if not pattern.compiled_regex or pattern.compiled_with_flags != flags:
                pattern.compiled_with_flags = flags
                pattern.compiled_regex = re.compile(pattern.regex, flags=flags)

            matches = pattern.compiled_regex.finditer(text)
            for match in matches:
                start, end = match.span()
                current_match = text[start:end]

                # Skip empty results
                if current_match == "":
                    continue

                score = pattern.score

                validation_result = self.validate_result(current_match)
                description = self.build_regex_explanation(
                    self.name,
                    pattern.name,
                    pattern.regex,
                    score,
                    validation_result,
                    flags,
                )
                recognition_metadata = {"pattern_name": pattern.name}
                recognition_metadata.update(match.groupdict())
                pattern_result = RecognizerResult(
                    entity_type=self.supported_entities[0],
                    start=start,
                    end=end,
                    score=score,
                    analysis_explanation=description,
                    recognition_metadata=recognition_metadata
                )

                if validation_result is not None:
                    if validation_result:
                        pattern_result.score = EntityRecognizer.MAX_SCORE
                    else:
                        pattern_result.score = EntityRecognizer.MIN_SCORE

                invalidation_result = self.invalidate_result(current_match)
                if invalidation_result is not None and invalidation_result:
                    pattern_result.score = EntityRecognizer.MIN_SCORE

                if pattern_result.score > EntityRecognizer.MIN_SCORE:
                    results.append(pattern_result)

                # Update analysis explanation score following validation or invalidation
                description.score = pattern_result.score

        results = EntityRecognizer.remove_duplicates(results)
        return results
