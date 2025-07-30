import json
import re
from pathlib import Path

import pytest
from dirty_equals import HasLen, IsPartialDict, IsStr
from pymultirole_plugins.v1.schema import Document
from pyprocessors_document_fingerprint.document_fingerprint import (
    DocumentFingerprintProcessor,
    DocumentFingerprintParameters,
)


def test_model():
    model = DocumentFingerprintProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DocumentFingerprintParameters


# Arrange
@pytest.fixture
def original_doc():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


# Arrange
@pytest.fixture
def original_doc_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        return original_doc


def test_document_fingerprint_linker(original_doc):
    # linker
    doc = original_doc.copy(deep=True)
    processor = DocumentFingerprintProcessor()
    parameters = DocumentFingerprintParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )


def test_document_fingerprint_linker_en(original_doc_en):
    # linker
    doc = original_doc_en.copy(deep=True)
    processor = DocumentFingerprintProcessor()
    parameters = DocumentFingerprintParameters()
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert conso.altTexts == HasLen(1)
    altText = conso.altTexts[0]
    FINGERPRINT = re.compile(r"([QE]\d+[ ]?)+")
    assert altText.dict() == IsPartialDict(
        name="fingerprint", text=IsStr(regex=FINGERPRINT)
    )
