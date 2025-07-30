from pathlib import Path
from typing import List
from pyconverters_pyword.pyword import PyWordConverter, PyWordParameters
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile


def test_pyword():
    converter = PyWordConverter()
    parameters = PyWordParameters(segment=True)
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/PC_Kairntech_LLM_v1.docx')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'application/octet-streamn'), parameters)
        assert len(docs) == 1
        assert docs[0].identifier
        assert docs[0].text
    json_file = source.with_suffix(".md.json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
