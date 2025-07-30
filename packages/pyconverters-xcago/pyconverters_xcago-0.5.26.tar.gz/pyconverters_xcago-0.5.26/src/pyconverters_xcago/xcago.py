import json
import logging
import os
from typing import List, Type

from blingfire import text_to_sentences_and_offsets
from pydantic import BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence
from starlette.datastructures import UploadFile

_home = os.path.expanduser("~")


class XCagoParameters(ConverterParameters):
    pass


logger = logging.getLogger("pymultirole")


class XCagoConverter(ConverterBase):
    """XCago converter ."""

    def convert(
            self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        docs = []
        try:
            jdoc = json.load(source.file)
            lang = jdoc['source'].get('language_code', None)
            metadata = {
                'language': lang,
                'date': jdoc['source']['date'],
                'publication_name': jdoc['source']['name'],
                'publication_code': jdoc['source']['id'],
                'country_code': jdoc['source'].get('country_code', None),
                'word_count': int(jdoc['word_count'])
            }
            text = ""
            sentences = []
            text += 'HEADLINE' + '\n'
            title, text, sentences = add_paragraph(text, sentences, jdoc['headline'], source="headline", path="headline")
            text += '\n' + 'BYLINES' + '\n'
            for i, byline in enumerate(jdoc.get('bylines', [])):
                path = f"bylines[{i}].name"
                if 'name' in byline:
                    _, text, sentences = add_paragraph(text, sentences, byline['name'], source="byline", path=path)
            text += '\n' + 'QUOTES' + '\n'
            for i, quote in enumerate(jdoc.get('quotes', [])):
                path = f"quotes[{i}].text"
                if 'text' in quote:
                    _, text, sentences = add_paragraph(text, sentences, quote['text'], source="quote", path=path)
            text += '\n' + 'BOXOUTS' + '\n'
            for i, boxout in enumerate(jdoc.get('boxouts', [])):
                path = f"boxouts[{i}].text"
                if 'text' in boxout:
                    _, text, sentences = add_paragraph(text, sentences, boxout['text'], source="boxout", path=path)
            text += '\n' + 'IMAGES' + '\n'
            for i, image in enumerate(jdoc.get('images', [])):
                if 'photographer' in image:
                    path = f"images[{i}].photographer"
                    _, text, sentences = add_paragraph(text, sentences, image['photographer'], source="imageCredit", path=path)
                if 'text' in image:
                    path = f"images[{i}].text"
                    _, text, sentences = add_paragraph(text, sentences, image['text'], source="imageCaption", path=path)
            text += '\n' + 'BODY' + '\n'
            result = text_to_sentences_and_offsets(jdoc['story'])
            offset = len(text)
            if result:
                text += jdoc['story']
                for start, end in result[1]:
                    sentences.append(Sentence(start=start + offset, end=end + offset, metadata={'path' : "story", 'source' : "body"}))
            doc = Document(identifier=jdoc['local_id'], title=title, text=text, sentences=sentences, metadata=metadata)
            doc.metadata['original'] = source.filename
            docs.append(doc)
        except BaseException as err:
            logger.warning(
                f"Cannot parse document {source.filename}",
                exc_info=True,
            )
            raise err
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return XCagoParameters


def add_paragraph(text, sentences, item_text, source=None, path=None):
    sstart = len(text)
    text += item_text + '\n'
    metadata = {'path': path, 'source': source}
    sentences.append(Sentence(start=sstart, end=len(text), metadata=metadata))
    return item_text, text, sentences
