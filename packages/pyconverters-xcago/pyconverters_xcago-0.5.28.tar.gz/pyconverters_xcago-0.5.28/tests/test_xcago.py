from pathlib import Path
from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile

from pyconverters_xcago.xcago import (
    XCagoConverter,
    XCagoParameters,
)


def test_xcago_json():
    converter = XCagoConverter()
    parameters = XCagoParameters()
    testdir = Path(__file__).parent
    corpusdir = testdir / "data"
    for json_file in corpusdir.glob("*.json_"):
        with json_file.open("rb") as fin:
            docs: List[Document] = converter.convert(
                UploadFile(json_file.name, fin, "	application/json"), parameters
            )
            dl = DocumentList(__root__=docs)
            docfile = json_file.with_suffix(".json")
            with docfile.open("w") as fout:
                print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_xcago_corpus():
    converter = XCagoConverter()
    parameters = XCagoParameters()
    testdir = Path("/media/olivier/DATA/corpora/X-CAGO/PoC/corpus")
    for lang in ['DE']:
        corpusdir = testdir / f"Extra {lang}"
        convertdir = testdir / f"Extra Converted {lang}"
        for json_file in corpusdir.rglob("*.json"):
            with json_file.open("rb") as fin:
                docs: List[Document] = converter.convert(
                    UploadFile(json_file.name, fin, "	application/json"), parameters
                )
                dl = DocumentList(__root__=docs)
                docfile = convertdir / json_file.name
                with docfile.open("w") as fout:
                    print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
