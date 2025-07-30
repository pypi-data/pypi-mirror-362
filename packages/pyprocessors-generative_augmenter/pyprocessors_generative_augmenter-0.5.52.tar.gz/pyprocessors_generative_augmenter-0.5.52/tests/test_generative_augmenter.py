import json
from pathlib import Path

import pytest
from dirty_equals import HasLen
from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_generative_augmenter.generative_augmenter import (
    GenerativeAugmenterProcessor,
    GenerativeAugmenterParameters,
)


def test_generative_augmenter_basic():
    model = GenerativeAugmenterProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == GenerativeAugmenterParameters


def test_0shot_ner():
    parameters = GenerativeAugmenterParameters(
        to_lowercase=False,
        variant_altText="NER"
    )
    processor = GenerativeAugmenterProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/afp_slug_gold_fr-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        docs = [Document(**jdoc)]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/afp_slug_gold_fr-document-ner.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.parametrize("variant", ['preserve_entities', 'substitute_entities'])
def test_augment_doc(variant):
    parameters = GenerativeAugmenterParameters(
        to_lowercase=False,
        variant_altText=variant,
        variant_separator_regex="^- "
    )
    processor = GenerativeAugmenterProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        f"data/jinjadocs_{variant}.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(6)
        sum_file = testdir / f"data/jinjadocs_{variant}_augmented.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501

# @pytest.mark.parametrize("variant", ['preserve_entities', 'substitute_entities'])
# def test_augment_semeval(variant):
#     parameters = GenerativeAugmenterParameters(
#         to_lowercase=True,
#         variant_altText=variant,
#         variant_separator_regex="^- "
#     )
#     processor = GenerativeAugmenterProcessor()
#     testdir = Path(__file__).parent / 'data'
#     datadir = Path("/home/olivier/dev/kairntech/pyprocessors_openai_completion/tests/data")
#     jsonfiles = datadir.glob(f"semeval_fa_da_{variant}_*.json")
#     for jsonfile in jsonfiles:
#         with jsonfile.open("r") as fin:
#             jdocs = json.load(fin)
#             docs = [Document(**jdoc) for jdoc in jdocs]
#             docs = processor.process(docs, parameters)
#             sum_file = testdir / jsonfile.name
#             dl = DocumentList(__root__=docs)
#             with sum_file.open("w") as fout:
#                 print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
