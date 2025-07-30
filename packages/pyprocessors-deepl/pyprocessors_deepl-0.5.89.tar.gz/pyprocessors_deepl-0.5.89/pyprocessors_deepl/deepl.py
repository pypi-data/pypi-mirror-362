import os
from enum import Enum
from functools import lru_cache
from typing import List, Type, cast

import deepl
from deepl import SplitSentences
from pydantic import Field, BaseModel
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, AltText

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")


class TargetLang(str, Enum):
    # BG - Bulgarian
    # CS - Czech
    # DA - Danish
    DE = "DE"
    # EL - Greek
    EN_GB = "EN-GB"
    EN_US = "EN-US"
    ES = "ES"
    # ET - Estonian
    # FI - Finnish
    FR = "FR"
    # HU - Hungarian
    # ID - Indonesian
    IT = "FR"
    # JA - Japanese
    # LT - Lithuanian
    # LV - Latvian
    NL = "NL"
    # PL - Polish
    PT_BR = "PT-BR"
    PT_PT = "PT-PT"
    # RO - Romanian
    RU = "RU"
    # SK - Slovak
    # SL - Slovenian
    # SV - Swedish
    # TR - Turkish
    # UK - Ukrainian
    ZH = "ZH"


class Formality(str, Enum):
    default = "default"
    more = "more"
    less = "less"
    prefer_more = "prefer_more"
    prefer_less = "prefer_less"


class DeepLParameters(ProcessorParameters):
    target_lang: TargetLang = Field(
        None,
        description="""The language into which the text should be translated. Options currently available:</br>
                        <li>`DE` - German
                        <li>`EN-GB` - English (British)
                        <li>`EN-US` - English (American)
                        <li>`ES` - Spanish
                        <li>`FR` - French
                        <li>`IT` - Italian
                        <li>`NL` - Dutch
                        <li>`PT-BR` - Portuguese (Brazilian)
                        <li>`PT-PT` - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)
                        <li>`RU` - Russian
                        <li>`ZH` - Chinese (simplified)""")
    formality: Formality = Field(
        Formality.default,
        description="""Sets whether the translated text should lean towards formal or informal language.
                        This feature currently only works for target languages
                        DE (German), FR (French), IT (Italian), ES (Spanish), NL (Dutch), PL (Polish),
                        PT-PT, PT-BR (Portuguese) and RU (Russian).
                        Setting this parameter with a target language that does not support formality will fail,
                        unless one of the prefer_... options are used. Possible options are:</br>
                        <li>`default` - default
                        <li>`more` - for a more formal language
                        <li>`less` - for a more informal language
                        <li>`prefer_more` - for a more formal language if available, otherwise fallback to default formality
                        <li>`prefer_less` - for a more informal language if available, otherwise fallback to default formality""")
    as_altText: str = Field(
        None,
        description="""If defined generate the translation as an alternative text of the input document,
    if not replace the text of the input document.""",
    )


SUPPORTED_LANGUAGES = (
    "bg,cs,da,de,el,en,es,et,fi,fr,hu,id,it,ja,lt,lv,nl,pl,pt,ro,ru,sk,sl,sv,tr,uk,zh"
)


class DeepLProcessor(ProcessorBase):
    __doc__ = """Translate using DeepL
    #languages:""" + SUPPORTED_LANGUAGES

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        supported_languages = comma_separated_to_list(SUPPORTED_LANGUAGES)

        params: DeepLParameters = cast(DeepLParameters, parameters)
        try:
            translator = get_translator(DEEPL_API_KEY)
            for document in documents:
                lang = document_language(document, None)
                if lang is None or lang not in supported_languages:
                    raise AttributeError(
                        f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}"
                    )
                trans_title = None
                if document.title:
                    trans_title = translator.translate_text(document.title, source_lang=lang.upper(),
                                                            target_lang=params.target_lang.value,
                                                            split_sentences=SplitSentences.OFF,
                                                            formality=params.formality.value).text
                if document.sentences:
                    stexts = [
                        document.text[s.start:s.end] for s in document.sentences
                    ]
                    results = translator.translate_text(stexts, source_lang=lang.upper(),
                                                        target_lang=params.target_lang.value,
                                                        split_sentences=SplitSentences.OFF,
                                                        formality=params.formality.value)
                    trans_texts = [r.text for r in results]
                    trans_text = "\n".join(trans_texts)
                else:
                    trans_text = translator.translate_text(document.text, source_lang=lang.upper(),
                                                           target_lang=params.target_lang.value,
                                                           split_sentences=SplitSentences.ALL,
                                                           formality=params.formality.value).text
                if params.as_altText is not None and len(params.as_altText):
                    document.altTexts = document.altTexts or []
                    altTexts = [
                        alt
                        for alt in document.altTexts
                        if alt.name != params.as_altText
                    ]
                    atext = trans_text if trans_title is None else trans_title + "\n" + trans_text
                    altTexts.append(AltText(name=params.as_altText, text=atext))
                    document.altTexts = altTexts
                else:
                    if trans_title is not None:
                        document.title = trans_title
                    document.text = trans_text
                    document.metadata["language"] = params.target_lang.value[:2].lower()
                    document.sentences = []
                    document.annotations = None
                    document.categories = None

        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepLParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and "language" in doc.metadata:
        return doc.metadata["language"]
    return default


@lru_cache(maxsize=None)
def get_translator(auth_key):
    translator = deepl.Translator(auth_key)
    return translator
