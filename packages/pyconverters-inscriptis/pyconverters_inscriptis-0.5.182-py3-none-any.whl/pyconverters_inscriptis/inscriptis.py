import io
from typing import Type, List, Union

from bs4 import BeautifulSoup
from inscriptis import RE_STRIP_XML_DECLARATION, Inscriptis
from inscriptis.model.config import ParserConfig
from itertools import chain
from html import unescape
from lxml.html import fromstring
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile


class InscriptisParameters(ConverterParameters):
    display_images: bool = Field(
        False, description="whether to include image tiles/alt texts."
    )
    deduplicate_captions: bool = Field(
        False,
        description="whether to deduplicate captions such as image\
                titles (many newspaper include images and video previews with\
                identical titles).",
    )
    display_links: bool = Field(
        False,
        description="whether to display link targets\
                           (e.g. `[Python](https://www.python.org)`).",
    )
    display_anchors: bool = Field(
        False, description="whether to display anchors (e.g. `[here](#here)`)."
    )


class InscriptisConverter(ConverterBase):
    """[Inscriptis](https://inscriptis.readthedocs.io/en/latest/) HTML pretty converter ."""

    def convert(
        self, source: Union[io.IOBase, UploadFile], parameters: ConverterParameters
    ) -> List[Document]:
        """Parse the input source file and return a list of documents.

        :param source: A file object containing the data.
        :param parameters: options of the converter.
        :returns: List of converted documents.
        """
        parameters: InscriptisParameters = parameters

        config = ParserConfig(
            display_images=parameters.display_images,
            deduplicate_captions=parameters.deduplicate_captions,
            display_links=parameters.display_links,
            display_anchors=parameters.display_anchors,
        )
        # Guess encoding if necessary
        soup = BeautifulSoup(source.file, "html.parser")
        title = soup.find("title")
        html = str(soup)
        doc: Document = self.get_doc(html, config=config)
        doc.title = title.text if title else source.filename
        doc.identifier = source.filename
        doc.properties = {
            "fileName": source.filename,
            "encoding": soup.original_encoding or "utf-8",
        }
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return InscriptisParameters

    def get_doc(self, html_content, config=None):
        """
        Converts an HTML string to  Document with sentences, optionally including and deduplicating
        image captions, displaying link targets and using either the standard
        or extended indentation strategy.


        Args:
          html_content (str): the HTML string to be converted to text.
          config: An optional ParserConfig object.

        Returns:
          str -- The text representation of the HTML content.
        """
        html_content = html_content.strip()
        if not html_content:
            return ""

        # strip XML declaration, if necessary
        if html_content.startswith("<?xml "):
            html_content = RE_STRIP_XML_DECLARATION.sub("", html_content, count=1)
            html_content = html_content.strip()

        html_tree = fromstring(html_content)
        parser = Inscriptis(html_tree, config)
        doc = Document(text=None, sourceText=html_content)
        doc.text = ""
        doc.sentences = []
        start = 0
        for line in chain(*parser.clean_text_lines):
            line = unescape(line)
            doc.text += line + "\n"
            end = len(doc.text)
            doc.sentences.append({"start": start, "end": end})
            start = end
        if doc.text:
            doc.text.rstrip()
            doc.sentences[-1]["end"] -= 1
        return doc
