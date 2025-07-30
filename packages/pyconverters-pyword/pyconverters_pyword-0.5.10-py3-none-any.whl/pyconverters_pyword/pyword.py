import logging
from tempfile import SpooledTemporaryFile
from typing import List, Type, cast

import mammoth
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence
from starlette.datastructures import UploadFile

from pyconverters_pyword.md_splitter import ExperimentalMarkdownSyntaxTextSplitter

logger = logging.getLogger("pymultirole")


class PyWordParameters(ConverterParameters):
    segment: bool = Field(
        False,
        description="""Make chunks using the structure, such as headers"""
    )
    level_to_split_on: int = Field(
        -1,
        description="""Levels of headers to split on (default is all)"""
    )


class PyWordConverter(ConverterBase):
    """Convert DOCX to Markdown using [mammoth](https://github.com/mwilliamson/python-mammoth)
    """

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: PyWordParameters = cast(PyWordParameters, parameters)
        doc: Document = None
        splitter = ExperimentalMarkdownSyntaxTextSplitter(headers_to_split_on=params.level_to_split_on,
                                                          strip_headers=False) if params.segment else None
        md = CustomMarkdownConverter(heading_style='atx', sup_symbol=" ")
        try:
            input_file = source.file._file if isinstance(source.file, SpooledTemporaryFile) else source.file
            result = mammoth.convert_to_html(input_file)
            html = auto_table_headers(result.value)
            text = md.convert(html)
            sentences = []
            if splitter is not None:
                chunks = splitter.split_text(text)
                ctext = ""
                start = 0
                for chunk in chunks:
                    ctext += chunk.text
                    headers = [v for k, v in sorted(chunk.metadata.items()) if isinstance(k, int)]
                    smetadata = {}
                    if headers:
                        smetadata['Headers'] = ' / '.join(headers)
                    if not ExperimentalMarkdownSyntaxTextSplitter.chunk_is_title_only(chunk):
                        sentences.append(Sentence(start=start, end=len(ctext), metadata=smetadata))
                    start = len(ctext)
                assert ctext == text
            doc = Document(identifier=source.filename, text=text, sentences=sentences)
        except BaseException:
            logger.warning(
                f"Cannot convert PDF from file {source.filename}: ignoring",
                exc_info=True,
            )
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PyWordParameters


class CustomMarkdownConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """

    def __init__(self, **options):
        self.ignore_pagenum = options.pop("ignore_pagenum", True)
        super().__init__(**options)

    def convert_pagenum(self, el, text, convert_as_inline):
        return f"\n\npage {text}\n\n" if self.ignore_pagenum else ""


def auto_table_headers(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        first_row = table.find("tr")
        if first_row:
            for cell in first_row.find_all("td", recursive=False):
                cell.name = "th"
    return str(soup)

# def lint_markdown(md: str) -> str:
#     # Optionnel – simulate basic Markdown fixes (e.g., trailing spaces, consistent bullets)
#     lines = md.strip().split('\n')
#     cleaned = []
#     for line in lines:
#         line = re.sub(r'[ \t]+$', '', line)  # Trim trailing spaces
#         if line.startswith('* '):
#             line = '- ' + line[2:]
#         cleaned.append(line)
#     return '\n'.join(cleaned).strip()
