from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document

from assertions import assert_result
from pyannotators_patterns.patterns import PatternsAnnotator, PatternsParameters, PATTERNS_EXAMPLE_STR


@pytest.fixture(scope="module")
def annotator():
    return PatternsAnnotator()


@pytest.fixture(scope="module")
def parameters():
    return PatternsParameters(mapping={
        "cc": PATTERNS_EXAMPLE_STR
    })


@pytest.mark.parametrize(
    "text, expected_len, expected_res",
    [
        # fmt: off
        (
            "4012888888881881 4012-8888-8888-1881 4012 8888 8888 1881",
            3, ((0, 16), (17, 36), (37, 56),),
        ),
        ("122000000000003", 1, ((0, 15),),),
        ("my credit card: 122000000000003", 1, ((16, 31),),),
        ("371449635398431", 1, ((0, 15),),),
        ("5555555555554444", 1, ((0, 16),),),
        ("5019717010103742", 1, ((0, 16),),),
        ("30569309025904", 1, ((0, 14),),),
        ("6011000400000000", 1, ((0, 16),),),
        ("3528000700000000", 1, ((0, 16),),),
        ("6759649826438453", 1, ((0, 16),),),
        ("5555555555554444", 1, ((0, 16),),),
        ("4111111111111111", 1, ((0, 16),),),
        ("4917300800000000", 1, ((0, 16),),),
        ("4484070000000000", 1, ((0, 16),),),
        # fmt: on
    ],
)
def test_when_all_credit_cards_then_succeed(
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
