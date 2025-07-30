import time
from abc import ABC
from functools import lru_cache
from typing import Type, List, cast

import spacy
from pydantic import BaseModel
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.schema import Document, Sentence
from pymultirole_plugins.v1.segmenter import SegmenterParameters, SegmenterBase
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.language import Language
from wasabi import msg

from pysegmenters_pysdb.pysbd_sentencizer import PySBDSentencizer


class PySDBSegmenterParameters(SegmenterParameters, ABC):
    pass


SUPPORTED_LANGUAGES = "en,fr,de,nl,es,pt,it,zh,ar,hi,ur,fa,ru"


class PySDBSegmenter(SegmenterBase, ABC):
    __doc__ = """Rule-based segmenter relying on [PySBD](https://github.com/nipunsadvilkar/pySBD).
    #need-language
    #languages:""" + SUPPORTED_LANGUAGES

    def segment(self, documents: List[Document], parameters: SegmenterParameters) \
            -> List[Document]:
        params: PySDBSegmenterParameters = \
            cast(PySDBSegmenterParameters, parameters)
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        for document in documents:
            # Retrieve nlp pipe
            lang = document_language(document, None)
            if lang is None or lang not in supported_languages:
                raise AttributeError(f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}")
            nlp, enable_pipes = get_sentencizer_from_params(lang)
            with nlp.select_pipes(enable=enable_pipes):
                document.sentences = []
                doc = nlp(document.text)
                if doc.has_annotation("SENT_START"):
                    for sent in doc.sents:
                        end_token = doc[sent.end - 2] if doc[sent.end - 1].is_space and len(sent) >= 2 else doc[
                            sent.end - 1]
                        document.sentences.append(Sentence(start=sent.start_char, end=end_token.idx + len(end_token)))
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PySDBSegmenterParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and 'language' in doc.metadata:
        return doc.metadata['language']
    return default


def get_sentencizer_from_params(lang):
    return get_pysbd_sentencizer(lang, ttl_hash=get_ttl_hash())


# Deprecated model shortcuts, only used in errors and warnings
MODEL_SHORTCUTS = {
    "en": "en_core_web_sm", "de": "de_core_news_sm", "es": "es_core_news_sm",
    "pt": "pt_core_news_sm", "fr": "fr_core_news_sm", "it": "it_core_news_sm",
    "nl": "nl_core_news_sm", "el": "el_core_news_sm", "nb": "nb_core_news_sm",
    "lt": "lt_core_news_sm", "xx": "xx_ent_wiki_sm", "zh": "zh_core_web_sm",
    "ru": "ru_core_news_sm", "ja": "ja_core_news_sm"
}


@lru_cache(maxsize=None)
def get_nlp(lang: str, exclude=tuple(), ttl_hash=None):
    del ttl_hash
    model = MODEL_SHORTCUTS.get(lang, lang)
    # model = lang
    try:
        nlp: Language = spacy.load(model, exclude=exclude)
    except BaseException:
        nlp = load_spacy_model(model, exclude=exclude)
    return nlp


@lru_cache(maxsize=None)
def get_pysbd_sentencizer(lang: str, ttl_hash=None):
    nlp = get_nlp(lang, exclude=("parser", "tagger", "ner", "lemmatizer"), ttl_hash=ttl_hash)
    unique_name = "sentencizer_pysbd"
    sentencizer: PySBDSentencizer = nlp.add_pipe("pysbd_sentencizer", name=unique_name)
    enable_pipes = [p for p in nlp.pipe_names if not p.startswith("sentencizer_") or p == sentencizer.name]
    return nlp, enable_pipes


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


def load_spacy_model(model, exclude, *pip_args):
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
    if model_name not in compatibility:
        msg.warn(
            f"No compatible package found for '{model}' (spaCy v{spacy.about.__version__}), fallback to blank model")
        return spacy.blank(model_name)
    else:
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
        return spacy.load(model_name, exclude=exclude)


def require_package(name):
    try:
        import pkg_resources

        pkg_resources.working_set.require(name)
        return True
    except:  # noqa: E722
        return False
