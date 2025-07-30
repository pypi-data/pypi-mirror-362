from pathlib import Path
from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

from pyconverters_whisperx.whisperx import (
    WhisperXConverter,
    WhisperXParameters,
)


def test_whisperx():
    model = WhisperXConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == WhisperXParameters


@pytest.mark.skip(reason="Not a test")
def test_whisperx_yaml():
    model = WhisperXConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == WhisperXParameters
    converter = WhisperXConverter()
    parameters = WhisperXParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, "data/test.yaml")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin), parameters
        )
        assert len(docs) == 1
        doc0 = docs[0]
        assert "rapporteur" in doc0.text
