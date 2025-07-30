import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_segment_renseignor.segment_renseignor import (
    SegmentRenseignorProcessor,
    SegmentRenseignorParameters,
)


def test_model():
    model = SegmentRenseignorProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == SegmentRenseignorParameters


def test_segment_renseignor():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/renseignor-document-test2.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        original_docs = [Document(**jdoc)]
    processor = SegmentRenseignorProcessor()
    parameters = SegmentRenseignorParameters()

    docs = processor.process(original_docs, parameters)
    assert len(docs) > len(original_docs)
    result = Path(testdir, "data/renseignor-document-segmented2.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_segment_renseignors():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/renseignor-export-search.json")
    with source.open("r") as fin:
        jdocs = json.load(fin)
        original_docs = [Document(**jdoc) for jdoc in jdocs]
    processor = SegmentRenseignorProcessor()
    parameters = SegmentRenseignorParameters()

    docs = processor.process(original_docs, parameters)
    assert len(docs) > len(original_docs)
    result = Path(testdir, "data/renseignor-export-segmented.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
