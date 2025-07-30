import logging
import os
from enum import Enum
from functools import lru_cache
from typing import List, cast, Type

import requests
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Boundary, Sentence
from starlette.datastructures import UploadFile

from pyconverters_mistralocr.md_splitter import ExperimentalMarkdownSyntaxTextSplitter

MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY"
)
MISTRAL_URL = os.getenv(
    "MISTRAL_URL", "https://api.mistral.ai/v1/"
)

logger = logging.getLogger("pymultirole")


class MistralOCRModel(str, Enum):
    mistral_ocr_latest = "mistral-ocr-latest"


class MistralOCRParameters(ConverterParameters):
    model: MistralOCRModel = Field(
        MistralOCRModel.mistral_ocr_latest,
        description="""Latest Mistral OCR [model](https://docs.mistral.ai/capabilities/document/)"""
    )
    segment: bool = Field(
        False,
        description="""Make chunks using the structure, such as headers"""
    )
    level_to_split_on: int = Field(
        -1,
        description="""Levels of headers to split on (default is all)"""
    )


class MistralOCRConverter(ConverterBase):
    """MistralOCR PDF converter ."""

    def convert(
            self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: MistralOCRParameters = cast(MistralOCRParameters, parameters)

        client = get_client(MISTRAL_URL)
        docs = []
        doc = client.convert(source, params)
        docs.append(doc)
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return MistralOCRParameters


@lru_cache(maxsize=None)
def get_client(base_url):
    client = MistralClient(base_url)
    return client


class MistralClient:
    def __init__(self, base_url):
        self.base_url = base_url[0:-1] if base_url.endswith("/") else base_url
        self.dsession = requests.Session()
        self.dsession.headers.update({
            'Authorization': f"Bearer {MISTRAL_API_KEY}",
            'Accept': 'application/json',
            'user-agent': "speakeasy-sdk/python 1.2.6 2.486.1 0.0.2 mistralai_azure"
        })
        self.dsession.verify = False

    def upload(self, source: UploadFile):
        file_url = None
        try:
            payload = {'file': (source.filename, source.file, 'application/pdf')}
            resp = self.dsession.post(
                f"{self.base_url}/files",
                files=payload,
                data={'purpose': "ocr"},
            )
            if resp.ok:
                result = resp.json()
                file_id = result["id"]
                resp = self.dsession.get(
                    f"{self.base_url}/files/{file_id}/url",
                    params={'expiry': 1},
                    headers={'Accept': 'application/json'},
                )
                if resp.ok:
                    result = resp.json()
                    file_url = result['url']
                else:
                    logger.warning(f"Unsuccessful file upload: {source.filename}")
                    resp.raise_for_status()
            else:
                logger.warning(f"Unsuccessful file upload: {source.filename}")
                resp.raise_for_status()
        except BaseException as err:
            logger.warning("An exception was thrown!", exc_info=True)
            raise err
        return file_url

    def convert(self, source: UploadFile, params: MistralOCRParameters):
        doc = None
        splitter = ExperimentalMarkdownSyntaxTextSplitter(headers_to_split_on=params.level_to_split_on,
                                                          strip_headers=False) if params.segment else None
        try:
            file_url = self.upload(source)
            if file_url is not None:
                resp = self.dsession.post(
                    f"{self.base_url}/ocr",
                    json={'model': params.model.value,
                          'document': {
                              'type': 'document_url',
                              'document_url': file_url
                          }},
                    headers={'content-type': 'application/json'},
                )
                if resp.ok:
                    result = resp.json()
                    pages = []
                    sentences = []
                    start = 0
                    text = ""
                    title = None
                    for pi, page in enumerate(result['pages']):
                        markdown = page['markdown']
                        if pi == 0:
                            if markdown.startswith("# ") and "\n" in markdown:
                                firstline = markdown.split('\n', 1)[0]
                                title = firstline[2:]
                        text += page['markdown'] + '\n'
                        pages.append(Boundary(start=start, end=len(text)))
                        start = len(text)
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
                    doc = Document(identifier=source.filename, title=title or source.filename, text=text, sentences=sentences,
                                   boundaries={'page': pages}, metadata={'original': source.filename})
                else:
                    logger.warning(f"Unsuccessful OCR conversion: {source.filename}")
                    resp.raise_for_status()
        except BaseException as err:
            logger.warning("An exception was thrown!", exc_info=True)
            raise err
        return doc
