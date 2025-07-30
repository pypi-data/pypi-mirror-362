import json
from pathlib import Path
from typing import List

from dirty_equals import IsPartialDict
from pymultirole_plugins.v1.schema import Document
from pytest_check import check

from pyannotators_patterns.patterns import PatternsAnnotator, PatternsParameters


def test_tel(
):
    testdir = Path(__file__).parent
    source = Path(testdir, "data/tel.json")
    with source.open("r") as fin:
        pat = json.load(fin)
        parameters = PatternsParameters(mapping={
            "telephone": json.dumps(pat, indent=2)
        })
    source = Path(testdir, "data/tel-document.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
    annotator = PatternsAnnotator()
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    tel = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
               a.text == '+33.089-658-6494')
    with check:
        assert tel == IsPartialDict(labelName='telephone', text='+33.089-658-6494', score=0.85,
                                    properties=IsPartialDict(prefix='33', number='089-658-6494'))
