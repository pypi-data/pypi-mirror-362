import logging
from tempfile import SpooledTemporaryFile
from typing import List, Type, cast, Optional

import pandas as pd
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence
from starlette.datastructures import UploadFile

logger = logging.getLogger("pymultirole")


class PyExcelParameters(ConverterParameters):
    header: Optional[int] = Field(
        0,
        description="""Row number (0-indexed) to use as the column names,
                                  leave blank if there is no header""",
    )
    text_cols: str = Field(
        None,
        description="""Comma-separated list of column(s) to use as text""",
    )
    metadata_cols: str = Field(
        "*",
        description="""Comma-separated list of column(s) to use as metadata""",
    )


class PyExcelConverter(ConverterBase):
    """Convert DOCX to Markdown using [mammoth](https://github.com/mwilliamson/python-mammoth)
    """

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: PyExcelParameters = cast(PyExcelParameters, parameters)
        doc: Document = None
        sentences = []
        start = 0
        end = 0
        text = ""
        try:
            input_file = source.file._file if isinstance(source.file, SpooledTemporaryFile) else source.file
            lines = pd.read_excel(input_file, header=params.header)

            text_cols = get_col_indexes(lines, comma_separated_to_list(params.text_cols))
            all_cols = (
                [
                    col
                    for col in lines.columns
                    if col not in text_cols
                ]
            )
            metadata_cols = get_col_indexes(lines, comma_separated_to_list(params.metadata_cols)) if params.metadata_cols != "*" else all_cols
            for index, row in lines.iterrows():
                start = len(text)
                segtexts = [row[text_col].strip() for text_col in text_cols]
                text += '\n'.join(segtexts)
                end = len(text)
                text += '\n\n'
                metadata = {}
                for metadata_col in metadata_cols:
                    metadata[metadata_col] = row[metadata_col].strip()
                sentences.append(Sentence(start=start, end=end, metadata=metadata))
            doc = Document(identifier=source.filename, text=text, sentences=sentences)
        except BaseException:
            logger.warning(
                f"Cannot convert XLSX from file {source.filename}: ignoring",
                exc_info=True,
            )
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PyExcelParameters


def col_index(col):
    return int(col) if col.lstrip("+-").isdigit() else col


def get_col_indexes(df, cols):
    colids = []
    if cols:
        for col in cols:
            colid = get_col_index(df, col)
            if colid is not None:
                colids.append(colid)
    return colids


def get_col_index(df, col, default=None):
    colid = default
    if col is not None:
        col = col.strip()
        if col and col in df.columns:
            colid = col_index(col)
        else:
            logger.warning(f"Unknown column {col}, ignoring")
    return colid
