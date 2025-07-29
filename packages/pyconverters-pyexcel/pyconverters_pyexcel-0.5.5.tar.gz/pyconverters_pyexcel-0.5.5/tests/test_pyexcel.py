from pathlib import Path
from typing import List
from pyconverters_pyexcel.pyexcel import PyExcelConverter, PyExcelParameters
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile


def test_pyexcel():
    converter = PyExcelConverter()
    parameters = PyExcelParameters(text_cols="Verbatim")
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/Echantion_dataverse.xlsx')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'application/octet-streamn'), parameters)
        assert len(docs) == 1
        assert docs[0].identifier
        assert docs[0].text
    json_file = source.with_suffix(".json")
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
