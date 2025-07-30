import json
import logging
import time
from abc import ABC
from functools import lru_cache
from typing import Type, List, cast, Dict, Any, Optional

import spacy
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.schema import Document, Sentence
from pymultirole_plugins.v1.segmenter import SegmenterParameters, SegmenterBase
from spacy.cli.download import download_model, get_compatibility, get_version
from spacy.language import Language
from wasabi import msg

from pysegmenters_rules_segmenter.rules_sentencizer import RuleSentencizer

logger = logging.getLogger("pymultirole")

SPLIT_DEFAULT = [
    [
        {
            "__comment": "Split on double line breaks...",
            "TEXT": {
                "NOT_IN": [
                    ":", ",", "，", "："
                ]
            }
        },
        {
            "__comment": "...except if previous lines ends with : or ,",
            "IS_SPACE": True,
            "TEXT": {
                "REGEX": "(.?\n){2,}"
            }
        },
        {
            "__comment": "Sentence start at this token"
        }
    ],
    [
        {
            "__comment": "Split on hard punctuation",
            "IS_PUNCT": True,
            "TEXT": {
                "IN": [
                    "!", "?", "¿", "؟", "¡", "。", "？", "！", "·", "…", "……"
                ]
            }
        },
        {
            "__comment": "Sentence start at this token"
        }
    ],
    [
        {
            "__comment": "Split on full stop...n",
            "IS_PUNCT": True,
            "TEXT": "."
        },
        {
            "__comment": "...if not followed by lower case letter or digit",
            "SHAPE": {
                "REGEX": "^[^xd]"
            }
        }
    ]
]
SPLIT_DEFAULT_STR = json.dumps(SPLIT_DEFAULT, indent=2)

SPLIT_EXAMPLE = [
    [
        {
            "__comment": "Split on line break...",
            "IS_SPACE": True,
            "TEXT": {
                "REGEX": "(.?\\n){1,}"
            }
        },
        {
            "__comment1": "... only if followed by paragraph trigger word",
            "LOWER": {
                "IN": [
                    "chapter", "title"
                ]
            },
            "__comment2": "... starting by an uppercase letter",
            "SHAPE": {
                "REGEX": "^X"
            }
        }
    ]
]
SPLIT_EXAMPLE_STR = json.dumps(SPLIT_EXAMPLE, indent=2)

JOIN_EXAMPLE = [
    [
        {
            "__comment": "Some abbreviations not natively covered by Spacy...",
            "TEXT": {
                "IN": [
                    "Doc.",
                    "Pres"
                ]
            }
        },
        {
            "__comment": "... followed by full stop",
            "IS_PUNCT": True,
            "TEXT": "."
        },
        {
            "IS_SENT_START": True
        }
    ]
]
JOIN_EXAMPLE_STR = json.dumps(JOIN_EXAMPLE, indent=2)


class RulesSegmenterParameters(SegmenterParameters, ABC):
    split_rule: str = Field(SPLIT_DEFAULT_STR,
                            description="""List of split rules that operates over tokens based on the [Spacy Rule-based matcher](https://spacy.io/usage/rule-based-matching) syntax<br/>
    The rules_segmenter can refer to token annotations (e.g. the token text and flags (e.g. IS_PUNCT), the sentence start always at the last token a of sequence.<br/>
    Let's suppose you want to force sentence to start on word triggers like Title/Chapter, then you need to define a single rule composed of 2 tokens:<ol>
    <li>A token whose `IS_SPACE` flag is set to true and that contains at least one line break `\\n`
    <li>A token whose `TEXT` is in a list of predefined paragraph triggers `["Chapter", "Title"]`
    </ol>
    Keys starting with `__comment` are considered as comments.<br/>
    Then you need to define a rule like:<br/>
```""" + SPLIT_EXAMPLE_STR + "```", extra="json")
    join_rule: Optional[str] = Field(None,
                                     description="""List of join rules that operates over tokens based on the [Spacy Rule-based matcher](https://spacy.io/usage/rule-based-matching) syntax<br/>
    The rules_segmenter join rules can be seen as exceptions that apply after the split rules.<br/>
    Let's suppose you don't want to segment after some abbreviations like `Pres.` or `Doc.`<br/>
    Then you need to define a rule like:<br/>
```""" + JOIN_EXAMPLE_STR + "```", extra="json")


SUPPORTED_LANGUAGES = "en,fr,de,nl,es,pt,it,zh,ar,hi,ur,fa,ru"


class RulesSegmenter(SegmenterBase, ABC):
    __doc__ = """Rule-based segmenter relying on custom [Spacy Rules](https://spacy.io/usage/rule-based-matching).
    #languages:""" + SUPPORTED_LANGUAGES

    def segment(self, documents: List[Document], parameters: SegmenterParameters) \
            -> List[Document]:
        params: RulesSegmenterParameters = \
            cast(RulesSegmenterParameters, parameters)
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)
        split_rules = json.loads(params.split_rule) if params.split_rule else []
        join_rules = json.loads(params.join_rule) if params.join_rule else []
        if len(split_rules) == 0:
            logger.warning(
                f"No splitting rules defined: ignoring",
                exc_info=True,
            )
            return documents
        for document in documents:
            # Retrieve nlp pipe
            lang = document_language(document, None)
            if lang is None or lang not in supported_languages:
                raise AttributeError(f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}")
            json_split = json_rules_to_string(split_rules)
            json_join = json_rules_to_string(join_rules)
            nlp, enable_pipes = get_custom_sentencizer(lang, json_split, json_join)
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
        return RulesSegmenterParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and 'language' in doc.metadata:
        return doc.metadata['language']
    return default


def json_rules_to_string(json_rules: List[List[Dict[str, Any]]]):
    str_rules = None
    if json_rules:
        for json_rule in json_rules:
            for token_rule in json_rule:
                # Remove comments if any
                for key in [k for k in token_rule if k.startswith('__comment')]:
                    del token_rule[key]
        str_rules = json.dumps(json_rules)
    return str_rules


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
def get_custom_sentencizer(lang: str, json_split: str, json_join: str, ttl_hash=None):
    nlp = get_nlp(lang, exclude=("parser", "tagger", "ner", "lemmatizer"), ttl_hash=ttl_hash)
    split_rules = json.loads(json_split) if json_split else None
    join_rules = json.loads(json_join) if json_join else None
    unique_name = f"sentencizer_{json_split if json_split else ''}_{json_join if json_join else ''}"
    sentencizer: RuleSentencizer = nlp.add_pipe("rules_sentencizer", name=unique_name,
                                                config={"split_patterns": split_rules, "join_patterns": join_rules})
    enable_pipes = [p for p in nlp.pipe_names if not p.startswith("sentencizer_") or p == sentencizer.name]
    return nlp, enable_pipes


@lru_cache(maxsize=None)
def get_spacy_sentencizer(lang: str, ttl_hash=None):
    nlp = get_nlp(lang, exclude=tuple(), ttl_hash=ttl_hash)
    enable_pipes = [p for p in nlp.pipe_names]
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
        msg.fail(
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
