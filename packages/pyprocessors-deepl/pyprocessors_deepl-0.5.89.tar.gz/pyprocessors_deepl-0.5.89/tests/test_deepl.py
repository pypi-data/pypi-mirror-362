import json
from pathlib import Path
import pytest
from dirty_equals import IsPartialDict, HasLen, HasAttributes, IsList
from pymultirole_plugins.v1.schema import Document, DocumentList
from pyprocessors_deepl.deepl import DeepLProcessor, DeepLParameters, TargetLang


def test_deepl_basic():
    model = DeepLProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepLParameters


@pytest.mark.skip(reason="Not a test")
def test_deepl():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/from.json",
    )

    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]

        parameters = DeepLParameters(target_lang=TargetLang.EN_US)
        processor = DeepLProcessor()
        docs = processor.process(docs, parameters)
        assert docs == HasLen(11)
        for doc in docs:
            assert doc.metadata == IsPartialDict(language="en")

        target = Path(
            testdir,
            "data/to.json",
        )
        with target.open("w") as fout:
            dl = DocumentList(__root__=docs)
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

        parameters.as_altText = "translation"
        parameters.target_lang = TargetLang.FR
        docs = processor.process(docs, parameters)
        assert docs == HasLen(11)
        for doc in docs:
            assert doc.altTexts == IsList(HasAttributes(name=parameters.as_altText))

        target = Path(
            testdir,
            "data/toalts.json",
        )
        with target.open("w") as fout:
            dl = DocumentList(__root__=docs)
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_deepl_zh():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/chinese.json",
    )

    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]

        parameters = DeepLParameters(target_lang=TargetLang.FR)
        processor = DeepLProcessor()
        docs = processor.process(docs, parameters)
        target = Path(
            testdir,
            "data/chinese_fr.json",
        )
        with target.open("w") as fout:
            dl = DocumentList(__root__=docs)
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
