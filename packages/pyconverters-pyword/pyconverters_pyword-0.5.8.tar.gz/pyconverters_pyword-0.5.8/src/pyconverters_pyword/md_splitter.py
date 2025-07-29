import re
from typing import Union, List, Tuple

from pymultirole_plugins.v1.schema import Document, Sentence


class ExperimentalMarkdownSyntaxTextSplitter:
    """An experimental text splitter for handling Markdown syntax.

    This splitter aims to retain the exact whitespace of the original text while
    extracting structured metadata, such as headers. It is a re-implementation of the
    MarkdownHeaderTextSplitter with notable changes to the approach and
    additional features.

    Key Features:
    - Retains the original whitespace and formatting of the Markdown text.
    - Extracts headers, code blocks, and horizontal rules as metadata.
    - Splits out code blocks and includes the language in the "Code" metadata key.
    - Splits text on horizontal rules (`---`) as well.
    - Defaults to sensible splitting behavior, which can be overridden using the
      `headers_to_split_on` parameter.

    Parameters:
    ----------
    headers_to_split_on : List[Tuple[str, str]], optional
        Headers to split on, defaulting to common Markdown headers if not specified.
    return_each_line : bool, optional
        When set to True, returns each line as a separate chunk. Default is False.

    Usage example:
    --------------
    >>> headers_to_split_on = [
    >>>     ("#", "Header 1"),
    >>>     ("##", "Header 2"),
    >>> ]
    >>> splitter = ExperimentalMarkdownSyntaxTextSplitter(
    >>>     headers_to_split_on=headers_to_split_on
    >>> )
    >>> chunks = splitter.split(text)
    >>> for chunk in chunks:
    >>>     print(chunk)

    This class is currently experimental and subject to change based on feedback and
    further development.
    """

    DEFAULT_HEADER_KEYS = {
        "#": 0,
        "##": 1,
        "###": 2,
        "####": 3,
        "#####": 4,
        "######": 5,
    }

    def __init__(
        self,
        headers_to_split_on: int = -1,
        return_each_line: bool = False,
        strip_headers: bool = True,
    ):
        """Initialize the text splitter with header splitting and formatting options.

        This constructor sets up the required configuration for splitting text into
        chunks based on specified headers and formatting preferences.

        Args:
            headers_to_split_on (Union[List[Tuple[str, str]], None]):
                A list of tuples, where each tuple contains a header tag (e.g., "h1")
                and its corresponding metadata key. If None, default headers are used.
            return_each_line (bool):
                Whether to return each line as an individual chunk.
                Defaults to False, which aggregates lines into larger chunks.
            strip_headers (bool):
                Whether to exclude headers from the resulting chunks.
                Defaults to True.
        """
        self.chunks: List[Sentence] = []
        self.current_chunk = Document(text="", title="")
        self.current_header_stack: List[Tuple[int, str]] = []
        self.strip_headers = strip_headers
        if headers_to_split_on > 0:
            self.splittable_headers = {k: v for k, v in self.DEFAULT_HEADER_KEYS.items() if len(k) <= headers_to_split_on}
        else:
            self.splittable_headers = self.DEFAULT_HEADER_KEYS

        self.return_each_line = return_each_line

    @staticmethod
    def chunk_is_title_only(chunk):
        chunk_content = chunk.text.strip()
        chunk_title = chunk.title.strip()
        return chunk_title == chunk_content

    def split_text(self, text: str) -> List[Document]:
        """Split the input text into structured chunks.

        This method processes the input text line by line, identifying and handling
        specific patterns such as headers, code blocks, and horizontal rules to
        split it into structured chunks based on headers, code blocks, and
        horizontal rules.

        Args:
            text (str): The input text to be split into chunks.

        Returns:
            List[Document]: A list of `Document` objects representing the structured
            chunks of the input text. If `return_each_line` is enabled, each line
            is returned as a separate `Document`.
        """
        # Reset the state for each new file processed
        self.chunks.clear()
        self.current_chunk = Document(text="", title="", metadata={})
        self.current_header_stack.clear()

        raw_lines = text.splitlines(keepends=True)

        while raw_lines:
            raw_line = raw_lines.pop(0)
            header_match = self._match_header(raw_line)
            code_match = self._match_code(raw_line)
            horz_match = self._match_horz(raw_line)
            if header_match:
                self._complete_chunk_doc()

                if not self.strip_headers:
                    self.current_chunk.text += raw_line
                    self.current_chunk.title = raw_line

                # add the header to the stack
                header_depth = len(header_match.group(1))
                header_text = header_match.group(2)
                self._resolve_header_stack(header_depth, header_text)
            elif code_match:
                self._complete_chunk_doc()
                self.current_chunk.text = self._resolve_code_chunk(
                    raw_line, raw_lines
                )
                self.current_chunk.metadata["Code"] = code_match.group(1)
                self._complete_chunk_doc()
            elif horz_match:
                self._complete_chunk_doc()
            else:
                self.current_chunk.text += raw_line

        self._complete_chunk_doc()
        # I don't see why `return_each_line` is a necessary feature of this splitter.
        # It's easy enough to to do outside of the class and the caller can have more
        # control over it.
        if self.return_each_line:
            return [
                Document(text=line, metadata=chunk.metadata)
                for chunk in self.chunks
                for line in chunk.text.splitlines()
                if line and not line.isspace()
            ]
        return self.chunks

    def _resolve_header_stack(self, header_depth: int, header_text: str) -> None:
        for i, (depth, _) in enumerate(self.current_header_stack):
            if depth == header_depth:
                self.current_header_stack[i] = (header_depth, header_text)
                self.current_header_stack = self.current_header_stack[: i + 1]
                return
        self.current_header_stack.append((header_depth, header_text))

    def _resolve_code_chunk(self, current_line: str, raw_lines: List[str]) -> str:
        chunk = current_line
        while raw_lines:
            raw_line = raw_lines.pop(0)
            chunk += raw_line
            if self._match_code(raw_line):
                return chunk
        return ""

    def _complete_chunk_doc(self) -> None:
        chunk_content = self.current_chunk.text.strip()
        # Discard any empty chunk or chunk only containing a title
        if chunk_content:
            # Apply the header stack as metadata
            for depth, value in self.current_header_stack:
                header_key = self.splittable_headers.get("#" * depth)
                self.current_chunk.metadata[header_key] = value
            self.chunks.append(self.current_chunk)
        # Reset the current chunk
        self.current_chunk = Document(text="", title="", metadata={})

    # Match methods
    def _match_header(self, line: str) -> Union[re.Match, None]:
        match = re.match(r"^(#{1,6}) (.*)", line)
        # Only matches on the configured headers
        if match and match.group(1) in self.splittable_headers:
            return match
        return None

    def _match_code(self, line: str) -> Union[re.Match, None]:
        matches = [re.match(rule, line) for rule in [r"^```(.*)", r"^~~~(.*)"]]
        return next((match for match in matches if match), None)

    def _match_horz(self, line: str) -> Union[re.Match, None]:
        matches = [
            re.match(rule, line) for rule in [r"^\*\*\*+\n", r"^---+\n", r"^___+\n"]
        ]
        return next((match for match in matches if match), None)
