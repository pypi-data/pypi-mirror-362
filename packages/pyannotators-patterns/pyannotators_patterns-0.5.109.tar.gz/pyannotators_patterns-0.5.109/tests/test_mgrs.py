import json
from pathlib import Path
from typing import List

from pymultirole_plugins.v1.schema import Document

from pyannotators_patterns.patterns import PatternsAnnotator, PatternsParameters


def test_coords(
):
    testdir = Path(__file__).parent
    source = Path(testdir, "data/mgrs.json")
    with source.open("r") as fin:
        pat = json.load(fin)
        parameters = PatternsParameters(mapping={
            "mgrs": json.dumps(pat, indent=2)
        })
    source = Path(testdir, "data/mgrs-document.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
    annotator = PatternsAnnotator()
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    mgrs0 = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                 a.text == '30TYN1276297163')
    assert mgrs0['properties']['pattern_name'] == 'RE_MGRS_COORDINATES'
