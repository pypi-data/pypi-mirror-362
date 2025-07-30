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
        "zip": json.dumps({
            "patterns" : [
                {
                    "name": "zip code (weak)",
                    "regex": "(\\b\\d{5}(?:\\-\\d{4})?\\b)",
                    "score": 0.01,
                }
            ],
            "context": ["zip", "code"]
        })
    })


@pytest.mark.parametrize(
    "text, expected_len, expected_res",
    [
        # fmt: off
        # valid email addresses
        ("My zip code is 90210", 1, ((15, 20),),),
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
