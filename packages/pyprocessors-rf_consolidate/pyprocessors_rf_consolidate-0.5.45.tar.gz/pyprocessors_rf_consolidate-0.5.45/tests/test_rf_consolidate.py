import copy
import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document

from pyprocessors_rf_consolidate.rf_consolidate import (
    RFConsolidateProcessor,
    RFConsolidateParameters,
)


def test_model():
    model = RFConsolidateProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == RFConsolidateParameters


# Arrange
@pytest.fixture
def original_docs():
    testdir = Path(__file__).parent
    datadir = testdir / "data"
    original_docs = []
    for jfile in datadir.glob("*.json"):
        with jfile.open("r") as fin:
            doc = json.load(fin)
            original_docs.append(Document(**doc))
    return original_docs


def test_rf_consolidate_acro(original_docs):
    docs = copy.deepcopy(original_docs)
    processor = RFConsolidateProcessor()
    parameters = RFConsolidateParameters()
    docs = processor.process(docs, parameters)
    for i, conso in enumerate(docs):
        original_doc = original_docs[i]
        assert len(conso.annotations) < len(original_doc.annotations)
