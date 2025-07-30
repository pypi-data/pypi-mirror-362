import logging
import os
import re
import urllib
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, cast, Type, Optional

import requests
from grobid_client import Client
from grobid_client.api.pdf import process_fulltext_document
from grobid_client.models import (
    ProcessForm,
    Article,
    TextWithRefs,
    Citation,
    ArticleCitations,
)
from grobid_client.types import File, TEI
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence, Boundary, Annotation, Term, AltText
from starlette.datastructures import UploadFile

# _home = os.path.expanduser('~')
# xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')
APP_GROBID_URI = os.environ.get(
    "APP_GROBID_URI", "https://entityfishing.kairntech.com/grobid/api"
)

logger = logging.getLogger("pymultirole")


class InputFormat(str, Enum):
    PDF = "PDF"
    URL_List = "URL List"


class GrobidParameters(ConverterParameters):
    input_format: InputFormat = Field(
        InputFormat.PDF,
        description="""Input format of the input file, among:<br/>
        <li>`PDF`: a PDF file.<br/>
        <li>`"URL List`: A plain text file with a list of urls to PDF articles one by line.""",
    )
    sourceText: bool = Field(False, description="Set source text in conversion output")
    sentences: bool = Field(False, description="Force sentence segmentation")
    authors_and_affiliations: bool = Field(True, description="Add a metadata authors_and_affiliations where an author is followed by its affiliation in parenthesis")
    figures: bool = Field(
        False, description="Do extract figures and tables descriptions"
    )
    citations: bool = Field(
        False, description="Do extract bibliographic references in text"
    )
    extract_abstract: bool = Field(
        False, description="Do extract an abstract as altText"
    )
    header_regex: Optional[str] = Field(
        None, description="Keeps only sections which header name matches the regex", extra="advanced"
    )


class GrobidConverter(ConverterBase):
    """Grodbid PDF converter ."""

    def convert(
        self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: GrobidParameters = cast(GrobidParameters, parameters)

        client = get_client()

        docs = []
        if params.input_format == InputFormat.URL_List:
            inputs = source.file.readlines()
            for line in inputs:
                line = str(line, "utf-8") if isinstance(line, bytes) else line
                input = line.strip()
                if input:
                    pdffile = None
                    try:
                        url = urllib.parse.urlparse(input)
                        url_path = Path(url.path)
                        r = requests.get(
                            input, headers={"User-Agent": "Mozilla/5.0"}, stream=True
                        )
                        if r.ok:
                            with NamedTemporaryFile(
                                suffix=".pdf", prefix=url_path.stem
                            ) as f:
                                for chunk in r.iter_content(chunk_size=8 * 1024):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)
                                f.seek(0)
                                doc = file_to_doc(
                                    UploadFile(url.path, f, "application/pdf"), params, client,
                                    original=input
                                )
                                docs.append(doc)

                    except BaseException:
                        logger.warning(
                            f"Cannot retrieve article with url {input}: ignoring",
                            exc_info=True,
                        )
                    finally:
                        if pdffile:
                            pdffile.close()
        else:
            try:
                doc = file_to_doc(source, params, client)
                docs.append(doc)
            except BaseException:
                logger.warning(
                    f"Cannot retrieve article from file {source.filename}: ignoring",
                    exc_info=True,
                )

        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return GrobidParameters


def file_to_doc(source: UploadFile, params, client, original=None):
    doc = None
    form = ProcessForm(
        segment_sentences="1" if params.sentences else "0",
        input_=File(
            file_name=source.filename,
            payload=source.file,
            mime_type=source.content_type,
        ),
    )
    r = process_fulltext_document.sync_detailed(client=client, multipart_data=form)
    if r.is_success:
        doc = article_to_doc(r, params)
        doc.metadata['original'] = original or source.filename
    else:
        r.raise_for_status()
    return doc


def article_to_doc(response, params):
    article: Article = TEI.parse(response.content, figures=params.figures, back=True)
    doc = Document(identifier=article.identifier, title=article.title)
    if params.sourceText:
        doc.sourceText = response.content.decode("utf-8")
    doc.metadata = citation_to_metadata(article.bibliography, params)
    sections_to_text(doc, article.sections, article.citations, params)
    return doc


def citation_to_metadata(citation: Citation, params):
    metadata = {}
    if citation.main_title:
        metadata["main_title"] = str(citation.main_title)
    if citation.published:
        metadata["published"] = str(citation.published)
    if citation.publisher:
        metadata["publisher"] = citation.publisher
    if citation.ids:
        for k, v in citation.ids.additional_properties.items():
            metadata[k] = v
    if citation.authors:
        authors = authors_and_affiliations(citation.authors)
        lauthors = []
        laffiliations = set()
        lauthors_and_affiliations = []
        for author, affiliations in authors.items():
            lauthors.append(author)
            laffiliations.update(affiliations)
            auth_and_aff = '|'.join(affiliations)
            lauthors_and_affiliations.append(f"{author}: {auth_and_aff}")
        metadata["authors"] = lauthors
        metadata["affiliations"] = list(laffiliations)
        if params.authors_and_affiliations:
            metadata["authors_and_affiliations"] = lauthors_and_affiliations

    if citation.titles:
        for k, v in citation.titles.additional_properties.items():
            metadata["title_" + k] = v
    if citation.scopes:
        for k, v in citation.scopes.additional_properties.items():
            metadata[k] = v
    return metadata


def authors_and_affiliations(author_list):
    authors = defaultdict(set)
    if author_list:
        for author in author_list:
            auth = []
            if author.pers_name.firstname:
                auth.append(author.pers_name.firstname)
            if author.pers_name.middlename:
                auth.append(author.pers_name.middlename)
            if author.pers_name.surname:
                auth.append(author.pers_name.surname)
            author_name = " ".join(auth)
            affiliations = set()
            if author.affiliations:
                for affiliation in author.affiliations:
                    aff = []
                    if affiliation.institution:
                        aff.append(affiliation.institution)
                    if affiliation.department:
                        aff.append(affiliation.department)
                    if affiliation.laboratory:
                        aff.append(affiliation.laboratory)
                    affiliations.add(", ".join(aff))
            authors[author_name] = affiliations
    return authors


def sections_to_text(doc, sections, citations: ArticleCitations, params):
    header_pattern = re.compile(params.header_regex) if params.header_regex is not None else None

    ref2citations = {}
    if params.citations and citations:
        for ref, citation in citations.additional_properties.items():
            ref2citations["#" + ref] = citation_to_metadata(citation, params)
    if sections:
        text_buf = []
        sentences = []
        annotations = []
        boundaries = defaultdict(list)
        is_under_matching_header = False
        for section in sections:
            header_is_not_empty = len(section.paragraphs) > 0
            header_match = header_pattern is None
            if header_pattern is not None and section.name is not None:
                if header_pattern.match(section.name):
                    header_match = True
                    is_under_matching_header = True
                else:
                    if is_under_matching_header and header_is_not_empty:
                        header_match = True
                    else:
                        header_match = False
                        is_under_matching_header = False

            if header_match:
                start = sum(map(len, text_buf))
                bstart = start
                text_buf.append((section.name if section.name is not None else "") + "\n")
                end = sum(map(len, text_buf))
                sentences.append(Sentence(start=start, end=end))
                if section.paragraphs:
                    for paragraph in section.paragraphs:
                        if params.sentences:
                            for i, sentence in enumerate(paragraph):
                                sent, annots = add_references(
                                    sentence, text_buf, ref2citations
                                )
                                sentences.append(sent)
                                if params.citations:
                                    annotations.extend(annots)
                                if i < len(paragraph) - 1:
                                    text_buf.append(" ")
                            text_buf.append("\n")
                        else:
                            sent, annots = add_references(
                                paragraph, text_buf, ref2citations
                            )
                            sentences.append(sent)
                            if params.citations:
                                annotations.extend(annots)
                            text_buf.append("\n")
                text_buf.append("\n")
                bend = sum(map(len, text_buf))
                boundaries[section.name].append(Boundary(start=bstart, end=bend))

        doc.text = "".join(text_buf)
        if params.citations:
            doc.annotations = annotations
        if params.sentences:
            doc.sentences = sentences
        doc.boundaries = boundaries
        if params.extract_abstract and boundaries:
            bnames = [k for k in boundaries.keys() if k is not None and k.lower() != "title"]
            if bnames:
                abname = "ABSTRACT" if "ABSTRACT" in bnames else bnames[0]
                ab = boundaries[abname][0]
                atext = doc.text[ab.start:ab.end]
                doc.altTexts = [AltText(name="abstract", text=atext)]


def add_references(sentence: TextWithRefs, text_buf: List[str], ref2citations):
    annotations = []
    start = sum(map(len, text_buf))
    text_buf.append(sentence.text + " ")
    end = sum(map(len, text_buf))
    if sentence.refs:
        for ref in sentence.refs:
            if ref.type == "bibr":
                a = Annotation(
                    label="Citation",
                    labelName="citation",
                    text=sentence.text[ref.start : ref.end],
                    start=start + ref.start,
                    end=start + ref.end,
                )
                props = ref2citations.get(ref.target, None)
                if props:
                    term_id = props.pop("main_title", "Unknown")
                    a.terms = [
                        Term(identifier=term_id, lexicon="grobid", properties=props)
                    ]
                annotations.append(a)
    return Sentence(start=start, end=end), annotations


@lru_cache(maxsize=None)
def get_client():
    return Client(base_url=APP_GROBID_URI, timeout=600)
