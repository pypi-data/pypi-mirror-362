import json
from pathlib import Path
from typing import List

from pymultirole_plugins.v1.schema import Document
from pyprocessors_afp_keywords.afp_keywords import (
    AFPKeywordsParameters,
    AFPKeywordsProcessor,
)


def test_afp_keywords_fr():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_doc_fr.json")
    parameters = AFPKeywordsParameters()
    annotator = AFPKeywordsProcessor()
    with source.open("r") as fin:
        jdoc = json.load(fin)
        jdocs = [Document(**jdoc)]

    docs: List[Document] = annotator.process(
        jdocs, parameters
    )
    doc = docs[0]
    alt0 = doc.altTexts[0]
    assert alt0.name == "slug"
    assert alt0.text == 'USA-cinéma-célébrités-récompense-GB-médias-Allemagne-France'

    parameters.threshold = 0.01
    docs: List[Document] = annotator.process(
        jdocs, parameters
    )
    doc = docs[0]
    alt0 = doc.altTexts[0]
    assert alt0.name == "slug"
    assert alt0.text == 'USA-cinéma-célébrités-récompense-GB-médias'
