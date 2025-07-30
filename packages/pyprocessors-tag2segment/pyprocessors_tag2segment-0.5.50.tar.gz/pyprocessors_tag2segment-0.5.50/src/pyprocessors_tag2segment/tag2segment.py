from typing import Type, List, cast

from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Sentence


class Tag2SegmentParameters(ProcessorParameters):
    segmentation_labels: List[str] = Field(
        None,
        description="""The list of possible label names to use as beginning of segment tags, all if empty. For example `\"bos\"`""",
        extra="label",
    )
    remove_segmentation_annotations: bool = Field(
        False, description="If True, remove the annotations used for segmentation"
    )


class Tag2SegmentProcessor(ProcessorBase):
    """Create segments from annotations ."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: Tag2SegmentParameters = cast(Tag2SegmentParameters, parameters)
        segmentation_labels = params.segmentation_labels or []
        for document in documents:
            sentences = []
            if document.annotations:
                if len(segmentation_labels) == 0:
                    segmentation_annots = [a for a in document.annotations if a.status != "KO"]
                    kept_annots = (
                        []
                        if params.remove_segmentation_annotations
                        else document.annotations
                    )
                else:
                    segmentation_annots = [
                        a
                        for a in document.annotations
                        if a.labelName in segmentation_labels and a.status != "KO"
                    ]
                    kept_annots = (
                        [
                            a
                            for a in document.annotations
                            if a.labelName not in segmentation_labels
                        ]
                        if params.remove_segmentation_annotations
                        else document.annotations
                    )
                indexes = sorted([a.start for a in segmentation_annots])
                if indexes:
                    start = 0
                    sentences = []
                    for i in indexes:
                        if i > start:
                            sentences.append(Sentence(start=start, end=i - 1))
                            start = i
                    if i < len(document.text):
                        sentences.append(Sentence(start=i, end=len(document.text)))
                    document.annotations = kept_annots
            if len(sentences) == 0:
                sentences.append(Sentence(start=0, end=len(document.text)))
            document.sentences = sentences
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return Tag2SegmentParameters
