import json
import logging
from functools import lru_cache
from typing import Type, List, cast, Dict

import spacy
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.util import filter_spans
from wasabi import msg

logger = logging.getLogger(__name__)

PATTERNS_EXAMPLE = [
    [
        {"POS": {"IN": ["ADJ", "NOUN", "PROPN"]}},
        {"POS": {"IN": ["ADJ", "NOUN", "PROPN", "DET", "ADP"]}, "OP": "*"},
        {"POS": {"IN": ["ADJ", "NOUN", "PROPN"]}},
    ]
]
PATTERNS_EXAMPLE_STR = json.dumps(PATTERNS_EXAMPLE, indent=2)


class SpacyMatcherParameters(AnnotatorParameters):
    mapping: Dict[str, str] = Field(
        None,
        description="""List of [spacy rule-based token patterns](https://demos.explosion.ai/matcher)<br/>
                            For example you can define a pattern to recognize (loosely)  noun-phrases like this:<br/>
    ```"""
        + PATTERNS_EXAMPLE_STR
        + "```",
        extra="key:label,val:json",
    )
    left_longest_match: bool = Field(
        True,
        description="""When spans overlap, the (first) longest span is preferred over shorter spans""",
        extra="advanced",
    )


SUPPORTED_LANGUAGES = "en,fr,de,nl,es,pt,it,zh,ar,ru"


class SpacyMatcherAnnotator(AnnotatorBase):
    __doc__ = """SpacyMatcher annotator using the [spacy rule-matching engine](https://spacy.io/usage/rule-based-matching#matcher).
    #need-segments
    #languages:""" + SUPPORTED_LANGUAGES

    def annotate(
        self, documents: List[Document], parameters: AnnotatorParameters
    ) -> List[Document]:
        params: SpacyMatcherParameters = cast(SpacyMatcherParameters, parameters)
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        mapping = frozenset(params.mapping.items())

        for document in documents:
            # Retrieve nlp pipe
            lang = document_language(document, None)
            if lang is None or lang not in supported_languages:
                raise AttributeError(
                    f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}"
                )
            get_matcher(lang, mapping)
            nlp, matcher = get_matcher(lang, mapping)

            document.annotations = []
            if not document.sentences:
                document.sentences = [Span(start=0, end=len(document.text))]

            sents_stexts = [
                (s, document.text[s.start : s.end])
                for s in document.sentences
                if s.end > s.start
            ]
            sents, stexts = list(map(list, zip(*sents_stexts)))
            docs = nlp.pipe(stexts)
            for s, doc in zip(sents, docs):
                if s.end > s.start:
                    spans = matcher(doc, as_spans=True)
                    if params.left_longest_match:
                        spans = filter_spans(spans)
                    for span in spans:
                        start = span.start_char + s.start
                        end = span.end_char + s.start
                        document.annotations.append(
                            Annotation(
                                start=start,
                                end=end,
                                text=document.text[start:end],
                                labelName=span.label_,
                            )
                        )

            return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SpacyMatcherParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


# Deprecated model shortcuts, only used in errors and warnings
MODEL_SHORTCUTS = {
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
    "es": "es_core_news_sm",
    "pt": "pt_core_news_sm",
    "fr": "fr_core_news_sm",
    "it": "it_core_news_sm",
    "nl": "nl_core_news_sm",
    "el": "el_core_news_sm",
    "nb": "nb_core_news_sm",
    "lt": "lt_core_news_sm",
    "xx": "xx_ent_wiki_sm",
    "zh": "zh_core_web_sm",
    "ru": "ru_core_news_sm",
}


@lru_cache(maxsize=None)
def get_nlp(lang):
    model = MODEL_SHORTCUTS.get(lang, lang)
    try:
        nlp: Language = spacy.load(model)
    except BaseException:
        nlp = load_spacy_model(model)
    return nlp


@lru_cache(maxsize=None)
def get_matcher(lang, mapping):
    nlp = get_nlp(lang)
    matcher = Matcher(nlp.vocab)
    for label, str_patterns in mapping:
        patterns = json.loads(str_patterns)
        matcher.add(label, patterns)
    return nlp, matcher


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
