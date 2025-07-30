import json
from pathlib import Path
from typing import List

from dirty_equals import IsPartialDict
from pymultirole_plugins.v1.schema import Document
from pytest_check import check

from pyannotators_patterns.patterns import PatternsAnnotator, PatternsParameters


def test_coords(
):
    testdir = Path(__file__).parent
    source = Path(testdir, "data/coords.json")
    with source.open("r") as fin:
        pat = json.load(fin)
        parameters = PatternsParameters(mapping={
            "coords": json.dumps(pat, indent=2)
        })
    source = Path(testdir, "data/coords-document.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
    annotator = PatternsAnnotator()
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    lat0 = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                a.text == 'N85,8598654')
    with check:
        assert lat0 == IsPartialDict(labelName='coords', text='N85,8598654',
                                     properties=IsPartialDict(ref_lat='N', val_lat='85,8598654',
                                                              pattern_name='ref_lat'))

    lat1 = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                a.text == '85,8598654N')
    with check:
        assert lat1 == IsPartialDict(labelName='coords', text='85,8598654N',
                                     properties=IsPartialDict(ref_lat='N', val_lat='85,8598654',
                                                              pattern_name='ref_lat_DEVANT'))
