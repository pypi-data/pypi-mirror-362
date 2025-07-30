from pathlib import Path
from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile

from pyconverters_isako.isako import IsakoConverter, IsakoParameters, OutputFormat


@pytest.mark.skip(reason="Not a test")
def test_isako_pdf():
    converter = IsakoConverter()
    parameters = IsakoParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Sodexo_URD_2023_FR - 4p.pdf")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "application/pdf"), parameters
        )
    assert len(docs) == 1
    assert docs[0].identifier
    assert docs[0].text
    json_file = source.with_suffix(".text.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

    parameters.output_format = OutputFormat.Html
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "application/pdf"), parameters
        )
    assert len(docs) == 1
    assert docs[0].identifier
    assert docs[0].text
    json_file = source.with_suffix(".html.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

    parameters.output_format = OutputFormat.Markdown
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "application/pdf"), parameters
        )
    assert len(docs) == 1
    assert docs[0].identifier
    assert docs[0].text
    json_file = source.with_suffix(".md.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
