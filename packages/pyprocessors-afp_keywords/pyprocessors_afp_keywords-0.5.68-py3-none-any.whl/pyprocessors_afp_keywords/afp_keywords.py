import os
from typing import List
from typing import Type, cast

from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorBase, ProcessorParameters
from pymultirole_plugins.v1.schema import Document, AltText

_home = os.path.expanduser("~")

class AFPKeywordsParameters(ProcessorParameters):
    threshold: float = Field(0.0, description="""Score threshold to keep the keyword.""")
    as_altText: str = Field(
        "slug",
        description="If defined, generate the slug as an alternative text of the input document.",
    )


class AFPKeywordsProcessor(ProcessorBase):
    """AFP keywords extractor."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: AFPKeywordsParameters = cast(AFPKeywordsParameters, parameters)
        for document in documents:
            labels = []
            if document.categories:
                for cat in document.categories:
                    if cat.score > params.threshold:
                        labels.append(cat.label or cat.labelName)
            slug = "-".join(labels)
            if params.as_altText is not None and len(params.as_altText):
                document.altTexts = document.altTexts or []
                altTexts = [
                    alt for alt in document.altTexts if alt.name != params.as_altText
                ]
                altTexts.append(AltText(name=params.as_altText, text=slug))
                document.altTexts = altTexts
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPKeywordsParameters

