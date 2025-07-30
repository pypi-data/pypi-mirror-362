import base64
import logging
import os
import xml.etree.ElementTree as ET
from enum import Enum
from functools import lru_cache
from time import sleep
from typing import List, cast, Type

import requests
from inscriptis import get_text
from markdownify import MarkdownConverter
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

ISAKO_URL = os.getenv(
    "ISAKO_URL", "https://secure-isako.com/TableAndImageWS/"
)

ISAKO_API_KEY = os.getenv(
    "ISAKO_API_KEY", "5h1zQ9hQ232Jacr9SvY0I4sifUQ85AtsjGJA4gk1JD9c10xig2spiV9cVAbr4b9r"
)

logger = logging.getLogger("pymultirole")


class OutputFormat(str, Enum):
    Text = "Text"
    Html = "Html"
    Markdown = "Markdown"


class IsakoParameters(ConverterParameters):
    output_format: OutputFormat = Field(
        OutputFormat.Text,
        description="""Output format (plain text or markdown)"""
    )
    isako_url: str = Field(
        ISAKO_URL,
        description="""ISAKO server base url.""", extra="advanced",
    )


class IsakoConverter(ConverterBase):
    """Isako PDF converter ."""

    def convert(
            self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: IsakoParameters = cast(IsakoParameters, parameters)

        client = get_client(params.isako_url)
        docs = []
        try:
            fileName, fileContent = file_to_base64(source)
            doc = client.convert(fileName, fileContent, params)
            docs.append(doc)
        except BaseException:
            logger.warning(
                f"Cannot retrieve article from file {source.filename}: ignoring",
                exc_info=True,
            )
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return IsakoParameters


@lru_cache(maxsize=None)
def get_client(base_url):
    client = IsakoClient(base_url)
    return client


def file_to_base64(source: UploadFile):
    data = source.file.read()
    rv = base64.b64encode(data)
    return source.filename, rv


def is_success(job_bean):
    return job_bean and job_bean["status"] == "COMPLETED"


class CustomMarkdownConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def __init__(self, **options):
        self.ignore_pagenum = options.pop("ignore_pagenum", True)
        super().__init__(**options)

    def convert_pagenum(self, el, text, convert_as_inline):
        return f"\n\npage {text}\n\n" if self.ignore_pagenum else ""


class IsakoClient:
    def __init__(self, base_url):
        self.base_url = base_url[0:-1] if base_url.endswith("/") else base_url
        self.dsession = requests.Session()
        self.dsession.headers.update({"Accept": "application/json", 'XApiKey': f"{ISAKO_API_KEY}"})
        self.dsession.verify = False

    def convert(self, fileName: str, fileContent: str, params: IsakoParameters):
        doc = None
        try:
            resp = self.dsession.post(
                f"{self.base_url}/Import/importDocument",
                json={"fileName": fileName,
                      "base64EncodedContent": fileContent.decode('utf-8')
                      },
                timeout=300,
            )
            if resp.ok:
                job_bean = resp.json()
                job_id = job_bean["jobId"]
                is_completed = self.wait_for_completion(job_id)
                if is_completed:
                    content = self.get_content(job_id)
                    if content is not None:
                        doc = self.parse_content(content, params.output_format)
                else:
                    logger.warning("Unsuccessful transcription: {url}")
                    resp.raise_for_status()
            else:
                logger.warning("Unsuccessful transcription: {url}")
                resp.raise_for_status()
        except BaseException as err:
            logger.warning("An exception was thrown!", exc_info=True)
            raise err
        return doc

    def wait_for_completion(self, job_id):
        is_completed = False
        is_errored = False
        if job_id:
            while (not (is_completed or is_errored)):
                sleep(10)
                resp = self.dsession.get(f"{self.base_url}/Import/getDocumentStatus?jobId={job_id}")
                if resp.ok:
                    job_bean = resp.json()
                    is_completed = job_bean.get("isCompleted", False)
                    is_errored = job_bean.get("isErrored", False)
                else:
                    logger.warning(
                        "Impossible to retrieve status of job: {job_id}"
                    )
                    resp.raise_for_status()
        return is_completed

    def get_content(self, job_id):
        content = None
        resp = self.dsession.get(f"{self.base_url}/Import/downloadDaisyContent?jobId={job_id}")
        if resp.ok:
            job_bean = resp.json()
            content = job_bean["daisyContent"]
        else:
            logger.warning(
                "Impossible to retrieve status of job: {job_id}"
            )
            resp.raise_for_status()
        return content

    def parse_content(self, content: str, output_format):
        md = CustomMarkdownConverter(sup_symbol=" ")
        root = ET.fromstring(content)
        for el in root.iter():
            _, _, el.tag = el.tag.rpartition("}")
        head = root.find("head")
        metadata = {}
        title = None
        docid = None
        text = ""
        if head is not None:
            for meta in head.iter("meta"):
                mname = meta.get("name")
                mcontent = meta.get("content")
                if mname == "dtb:uid":
                    docid = mcontent
                elif mname == "dc:Ttile":
                    title = mcontent
                else:
                    metadata[mname] = mcontent
        book = root.find("book")
        if book is not None:
            # frontmatter = book.find("frontmatter")
            bodymatter = book.find("bodymatter")
            if bodymatter is not None:
                level1 = bodymatter.find("level1")
                htmlText = ET.tostring(level1, encoding="unicode")
                if output_format == OutputFormat.Html:
                    text = htmlText
                elif output_format == OutputFormat.Text:
                    text = get_text(htmlText)
                else:
                    text = md.convert(htmlText)

            # rearmatter = book.find("rearmatter")
        doc = Document(identifier=docid, title=title, text=text, metadata=metadata)
        return doc
