import json
from typing import List
import pytest
from pymultirole_plugins.v1.schema import Document

from assertions import assert_result
from pyannotators_patterns.patterns import PatternsAnnotator, PatternsParameters


@pytest.fixture(scope="module")
def annotator():
    return PatternsAnnotator()


@pytest.fixture(scope="module")
def parameters():
    return PatternsParameters(mapping={
        "email": json.dumps({
            "patterns" : [
                {
                    "name": "Email (Medium)",
                    "regex": r"\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b",
                    "score": 0.5,
                }
            ],
            "context": ["email"]
        })
    })


@pytest.mark.parametrize(
    "text, expected_len, expected_res",
    [
        # fmt: off
        # valid email addresses
        ("info@presidio.site", 1, ((0, 18),),),
        ("my email address is info@presidio.site", 1, ((20, 38),),),
        ("try one of these emails: info@presidio.site or anotherinfo@presidio.site",
            2,
         ((25, 43), (47, 72),),),
        # invalid email address
        ("my email is info@presidio.", 0, ()),
        # fmt: on
    ],
)
def test_when_all_email_addresses_then_succeed(
        text,
        expected_len,
        expected_res,
        annotator,
        parameters,
):
    entity_type = list(parameters.mapping.keys())[0]
    docs: List[Document] = annotator.annotate([Document(text=text, metadata={'language': 'en'})], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == expected_len
    for res, (start, end) in zip(doc0.annotations, expected_res):
        assert_result(res, entity_type, start, end, None)
