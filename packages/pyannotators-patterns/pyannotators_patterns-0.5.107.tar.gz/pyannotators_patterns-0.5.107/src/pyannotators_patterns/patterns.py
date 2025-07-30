import json
import logging
from functools import lru_cache
from typing import Type, List, cast, Dict

import spacy
from log_with_context import add_logging_context
from presidio_analyzer import Pattern, RecognizerRegistry, AnalyzerEngine, LemmaContextAwareEnhancer, RecognizerResult
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NerModelConfiguration
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.language import Language
from wasabi import msg

from .named_pattern_recognizer import NamedPatternRecognizer

logger = logging.getLogger(__name__)

PATTERNS_EXAMPLE = {
    "patterns": [
        {
            "name": "All Credit Cards (weak)",
            "regex": r"\b((4\d{3})|(5[0-5]\d{2})|(6\d{3})|(1\d{3})|(3\d{3}))[- ]?(\d{3,4})[- ]?(\d{3,4})[- ]?(\d{3,5})\b",
            "score": 0.3
        }
    ],
    "context": [
        "credit",
        "card",
        "visa",
        "mastercard",
        "cc ",
        "amex",
        "discover",
        "jcb",
        "diners",
        "maestro",
        "instapayment",
    ]
}
PATTERNS_EXAMPLE_STR = json.dumps(PATTERNS_EXAMPLE, indent=2)


class PatternsParameters(AnnotatorParameters):
    mapping: Dict[str, str] = Field(None,
                                    description="""List of regex patterns to be used by the annotator and optionnal list of context words to increase confidence in detection.<br/>
                            Each pattern is composed of a name, a list of python regular expressions and a score indicating the pattern's strength (values varies from 0 to 1).<br/>
                            For example you can define a regex pattern to recognize credit card numbers addresses along with some [context words](https://microsoft.github.io/presidio/tutorial/06_context/) like this:<br/>
    ```""" + PATTERNS_EXAMPLE_STR + "```", extra="key:label,val:json")

    score_threshold: float = Field(0.0, description="Minimum confidence value for detected entities to be returned")
    context_similarity_factor: float = Field(0.35,
                                             description="How much to enhance confidence of match entity, as explained [here](https://microsoft.github.io/presidio/tutorial/06_context/)",
                                             extra="advanced")
    min_score_with_context_similarity: float = Field(0.4,
                                                     description="Minimum confidence score, as explained [here](https://microsoft.github.io/presidio/tutorial/06_context/)",
                                                     extra="advanced")
    context_prefix_count: int = Field(5,
                                      description="How many words before the entity to match context, as explained [here](https://microsoft.github.io/presidio/tutorial/06_context/)",
                                      extra="advanced")
    context_suffix_count: int = Field(0,
                                      description="How many words after the entity to match context, as explained [here](https://microsoft.github.io/presidio/tutorial/06_context/)",
                                      extra="advanced")


SUPPORTED_LANGUAGES = "en,fr,de,nl,es,pt,it,zh,ar,ru"


class PatternsAnnotator(AnnotatorBase):
    __doc__ = """Patterns annotator using the Presidio [regex pattern recognizer](https://microsoft.github.io/presidio/tutorial/02_regex/).
    Regular expressions can be tested [here](https://regex101.com/).
    #need-segments
    #languages:""" + SUPPORTED_LANGUAGES

    def annotate(
            self, documents: List[Document], parameters: AnnotatorParameters
    ) -> List[Document]:
        params: PatternsParameters = cast(PatternsParameters, parameters)
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        mapping = frozenset(params.mapping.items())
        labels = list(params.mapping.keys())
        for document in documents:
            with add_logging_context(docid=document.identifier):
                # Retrieve nlp pipe
                lang = document_language(document, None)
                if lang is None or lang not in supported_languages:
                    raise AttributeError(f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}")
                nlp = get_nlp(lang)
                registry = get_registry(mapping, lang)
                analyzer = AnalyzerEngine(registry=registry,
                                          nlp_engine=LoadedSpacyNlpEngine(lang, nlp),
                                          default_score_threshold=0,
                                          supported_languages=supported_languages,
                                          context_aware_enhancer=LemmaContextAwareEnhancer(params.context_similarity_factor,
                                                                                           params.min_score_with_context_similarity,
                                                                                           params.context_prefix_count,
                                                                                           params.context_suffix_count))

                document.annotations = []
                if not document.sentences:
                    document.sentences = [Span(start=0, end=len(document.text))]

                for s in document.sentences:
                    if s.end > s.start:
                        stext = document.text[s.start: s.end]
                        results = analyzer.analyze(text=stext, entities=labels,
                                                   language=lang, return_decision_process=True,
                                                   score_threshold=params.score_threshold)  # noqa D501
                        for result in results:
                            start = s.start + result.start
                            end = s.start + + result.end
                            props = {k: v for k, v in result.recognition_metadata.items() if
                                     k not in [RecognizerResult.RECOGNIZER_NAME_KEY,
                                               RecognizerResult.RECOGNIZER_IDENTIFIER_KEY]}
                            document.annotations.append(
                                Annotation(
                                    start=start,
                                    end=end,
                                    text=document.text[start: end],
                                    labelName=result.entity_type,
                                    score=result.score,
                                    properties=props
                                )
                            )

            return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PatternsParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and 'language' in doc.metadata:
        return doc.metadata['language']
    return default


# Deprecated model shortcuts, only used in errors and warnings
MODEL_SHORTCUTS = {
    "en": "en_core_web_sm", "de": "de_core_news_sm", "es": "es_core_news_sm",
    "pt": "pt_core_news_sm", "fr": "fr_core_news_sm", "it": "it_core_news_sm",
    "nl": "nl_core_news_sm", "el": "el_core_news_sm", "nb": "nb_core_news_sm",
    "lt": "lt_core_news_sm", "xx": "xx_ent_wiki_sm", "zh": "zh_core_web_sm",
    "ru": "ru_core_news_sm"
}


@lru_cache(maxsize=None)
def get_nlp(lang):
    model = MODEL_SHORTCUTS.get(lang, lang)
    try:
        nlp: Language = spacy.load(model)
    except BaseException:
        nlp = load_spacy_model(model)
    return nlp


# Create a class inheriting from SpacyNlpEngine
class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, lang, loaded_spacy_model, ner_model_configuration=None):
        self.nlp = {lang: loaded_spacy_model}
        self.ner_model_configuration = ner_model_configuration or NerModelConfiguration()


@lru_cache(maxsize=None)
def get_registry(mapping_items, lang):
    recognizers = []
    for pname, pvalue in mapping_items:
        try:
            pattern_definition = json.loads(pvalue)
        except BaseException:
            logger.warning(f"Invalid json: {pvalue}", exc_info=True)
        patterns = [Pattern.from_dict(pat) for pat in pattern_definition['patterns']]
        recognizer = NamedPatternRecognizer(
            supported_entity=pname, supported_language=lang, patterns=patterns, context=pattern_definition.get('context', None)
        )
        recognizers.append(recognizer)
    registry = RecognizerRegistry(recognizers)
    return registry


def load_spacy_model(model, *pip_args):
    suffix = "-py3-none-any.whl"
    dl_tpl = "{m}-{v}/{m}-{v}{s}#egg={m}=={v}"
    model_name = model
    if model in MODEL_SHORTCUTS:
        msg.warn(
            f"As of spaCy v3.0, shortcuts like '{model}' are deprecated. Please "
            f"use the full pipeline package name '{MODEL_SHORTCUTS[model]}' instead."
        )
        model_name = MODEL_SHORTCUTS[model]
    compatibility = get_compatibility()
    version = get_version(model_name, compatibility)
    download_model(dl_tpl.format(m=model_name, v=version, s=suffix), pip_args)
    msg.good(
        "Download and installation successful",
        f"You can now load the package via spacy.load('{model_name}')",
    )
    # If a model is downloaded and then loaded within the same process, our
    # is_package check currently fails, because pkg_resources.working_set
    # is not refreshed automatically (see #3923). We're trying to work
    # around this here be requiring the package explicitly.
    require_package(model_name)
    return spacy.load(model_name, exclude=["parser"])


def require_package(name):
    try:
        import pkg_resources

        pkg_resources.working_set.require(name)
        return True
    except:  # noqa: E722
        return False
