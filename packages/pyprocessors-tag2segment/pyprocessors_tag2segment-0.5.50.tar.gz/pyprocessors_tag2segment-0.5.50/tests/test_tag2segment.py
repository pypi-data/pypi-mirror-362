import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document, DocumentList
from pyprocessors_tag2segment.tag2segment import (
    Tag2SegmentProcessor,
    Tag2SegmentParameters,
)


def test_model():
    model = Tag2SegmentProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == Tag2SegmentParameters


def test_tag2segment():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/news_fr.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    segmentation_annots = [a for a in original_doc.annotations if a.labelName == "bos"]
    processor = Tag2SegmentProcessor()
    parameters = Tag2SegmentParameters(
        segmentation_labels=["bos"], remove_segmentation_annotations=False
    )
    docs = processor.process([Document(**doc)], parameters)
    tag2segmented: Document = docs[0]
    assert len(tag2segmented.sentences) == len(segmentation_annots)
    for i, a in enumerate(segmentation_annots):
        assert a.start == tag2segmented.sentences[i].start

    parameters = Tag2SegmentParameters(
        segmentation_labels=["bos"], remove_segmentation_annotations=True
    )
    docs = processor.process([Document(**doc)], parameters)
    tag2segmented: Document = docs[0]
    assert len(tag2segmented.sentences) == len(segmentation_annots)
    assert len(original_doc.annotations) > len(tag2segmented.annotations)


@pytest.mark.skip(reason="Not a test")
def test_tag2segment2():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/wescreen_2-documents.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        original_docs = [Document(**doc) for doc in docs]
    original_segs = [len(doc.sentences) for doc in original_docs]
    processor = Tag2SegmentProcessor()
    parameters = Tag2SegmentParameters(segmentation_labels=[
        "objet",
        "lancement_exclusion",
        "lancement_garantie",
        "toutefois",
        "franchise",
        "article",
        "qui_est_assure",
        "sont_garantis",
        "modalites_d_indemnisation"])

    docs = processor.process(original_docs, parameters)
    tag2segmented: Document = docs[0]
    assert len(tag2segmented.sentences) < original_segs[0]
    result = Path(testdir, "data/wescreen_2-documents-segmented.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
