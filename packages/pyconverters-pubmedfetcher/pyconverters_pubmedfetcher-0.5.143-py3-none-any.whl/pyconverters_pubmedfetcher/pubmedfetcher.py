import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import List, cast, Type, Tuple
from blingfire import text_to_sentences_and_offsets
from lxml import etree as ET
from metapub import PubMedFetcher, PubMedArticle, CrossRefFetcher
from metapub.crossref import CrossRefWork
from metapub.exceptions import MetaPubError
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence
from ratelimit import sleep_and_retry, limits
from requests import HTTPError
from starlette.datastructures import UploadFile

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")
NCBI_API_KEY = os.environ.get("NCBI_API_KEY")
DOI_REGEX = re.compile("^10.\\d{4,9}/[-._;()/:A-Z0-9]+$", flags=re.I)
PMID_REGEX = re.compile("^\\d{7,8}$", flags=re.I)
PMCID_REGEX = re.compile("^PMC\\d{6,8}$", flags=re.I)


class InputFormat(str, Enum):
    XML_PubmedArticleSet = "XML PubmedArticleSet"
    ID_List = "ID List"
    Query = "Query"


class PubmedFetcherParameters(ConverterParameters):
    input_format: InputFormat = Field(
        InputFormat.XML_PubmedArticleSet,
        description="""Input format of the input file, among:<br/>
        <li>`XML PubmedArticleSet`: an XML file with PubmedArticleSet as root element.<br/>
        <li>`ID List`: A plain text file with a mix of Pubmed ids, PMC ids, DOIDs one by line.""",
    )
    segment: bool = Field(True, description="Force fast sentence segmentation")
    retmax: int = Field(10, description="Maximum number of hits to return")
    discard_if_no_abstract: bool = Field(
        True, description="Discard article if no abstract"
    )


logger = logging.getLogger("pymultirole")


class PubmedFetcherConverter(ConverterBase):
    """PubmedFetcher converter ."""

    def convert(
        self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: PubmedFetcherParameters = cast(PubmedFetcherParameters, parameters)

        docs = []
        if params.input_format in [InputFormat.ID_List, InputFormat.Query]:
            pm_fetcher, cr_fetcher = get_fetchers()
            pmids = []
            if params.input_format == InputFormat.ID_List:
                inputs = source.file.readlines()
                for line in inputs:
                    line = str(line, "utf-8") if isinstance(line, bytes) else line
                    input = line.strip()
                    pmids.append(input)
            elif params.input_format == InputFormat.Query:
                query = source.file.read()
                query = str(query, "utf-8") if isinstance(query, bytes) else query
                try:
                    pmids = pm_fetcher.pmids_for_query(query=query, retmax=params.retmax)
                except MetaPubError:
                    logger.warning(
                        f"Cannot retrieve articles with query {query}: ignoring",
                        exc_info=True,
                    )
            if pmids:
                for pmid in pmids:
                    try:
                        art = get_article(pm_fetcher, cr_fetcher, pmid)
                        doc = None
                        if art is not None:
                            doc = article_to_document(
                                art, params.segment, params.discard_if_no_abstract
                            )
                        if doc is not None:
                            doc.metadata['original'] = pmid
                            docs.append(doc)
                    except MetaPubError:
                        logger.warning(
                            f"Cannot retrieve article with identifier {pmid}: ignoring",
                            exc_info=True,
                        )

        elif params.input_format == InputFormat.XML_PubmedArticleSet:
            tree = ET.parse(source.file)
            for article in tree.iter("PubmedArticle"):
                art_xml = ET.tostring(article[0])
                art = PubMedArticle(art_xml)
                doc = article_to_document(
                    art, params.segment, params.discard_if_no_abstract
                )
                if doc is not None:
                    doc.metadata['original'] = source.filename
                    docs.append(doc)
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return PubmedFetcherParameters


def article_to_document(art, segment=False, discard_if_no_abstract=True):
    doc = None
    if art.abstract is not None or art.title is not None:
        if art.abstract is not None or not discard_if_no_abstract:
            art.abstract = art.abstract or ""
            text = art.title + "\n\n" + art.abstract if art.title else art.abstract
            metadata = {
                "journal": art.journal,
                "year": art.year,
                "authors": art.authors_str,
                "url": art.url,
            }
            if art.doi:
                metadata["DOI"] = art.doi
            if art.pmc:
                metadata["PMC"] = art.pmc
            doc = Document(
                identifier=str(art.pmid),
                title=art.title or str(art.pmid),
                text=text,
                metadata=metadata,
                annotations=[],
                sentences=[],
            )
            if segment:
                result = text_to_sentences_and_offsets(doc.text)
                if result:
                    for start, end in result[1]:
                        doc.sentences.append(Sentence(start=start, end=end))
    return doc


@dataclass
class FakePubMedArticle:
    doi: str
    pmc: str = None
    pmid: str = None
    title: str = None
    abstract: str = None
    journal: str = None
    year: str = None
    authors_str: str = None
    url: str = None


def doi2art(pm_fetch: PubMedFetcher, cr_fetch: CrossRefFetcher, doi):  # noqa:  W503
    """uses CrossRef and PubMed eutils to lookup a PMID given a known doi.

    Warning: NO validation of input DOI performed here. Use
             metapub.text_mining.find_doi_in_string beforehand if needed.

    If a PMID can be found, return it. Otherwise return None.

    In very rare cases, use of the CrossRef->pubmed citation method used
    here may result in more than one pubmed ID. In this case, this function
    will return instead the word 'AMBIGUOUS'.

    :param pmid: (str or int)
    :return doi: (str) if found; 'AMBIGUOUS' if citation count > 1; None if no results.
    """
    # for PMA, skip the validation; some pubmed XML has weird partial strings for DOI.
    # We should allow people to search using these oddball strings.
    doi = doi.strip()
    try:
        pma = pm_fetch.article_by_doi(doi)
        logger.debug("doi2pmid: Found PubMedArticle for DOI %s via eutils fetch", doi)
        return pma
    except MetaPubError:
        pass

    # Try doing a DOI lookup right in an advanced query string. Sometimes works and has
    # benefit of being a cached query so it is quick to do again, should we need.
    pmids = pm_fetch.pmids_for_query(doi)
    if len(pmids) == 1:
        # we need to cross-check; pubmed sometimes screws us over by giving us an article
        # with a SIMILAR doi. *facepalm*
        pma = pm_fetch.article_by_pmid(pmids[0])
        if pma.doi == doi:
            logger.debug(
                "doi2pmid: Found PMID via PubMed advanced query for DOI %s", doi
            )
            return pma

        logger.debug("Pubmed advanced query gave us a problematic result...")
        logger.debug("\tSearch: %s" % doi)
        logger.debug("\tReturn: %s" % pma.doi)

    # Try Looking up DOI in CrossRef, then feeding results to pubmed citation query tool...
    try:
        res = cr_fetch.cr.works(doi)
        work = CrossRefWork(**res["message"])
        if "abstract" in res["message"]:
            parser = ET.XMLParser(recover=True)
            root = ET.fromstring(res["message"]["abstract"], parser)
            work.abstract = "\n".join(root.itertext())
        else:
            work.abstract = None
        logger.debug("doi2pmid: Found CrossRef article for DOI %s", doi)
    except HTTPError as error:
        if str(error).find("404") > -1:
            logger.info("doi2pmid: DOI %s was not found in CrossRef.  Giving up.", doi)
            return None
        logger.debug("doi2pmid: Unexpected HTTP error occurred during CrossRef lookup:")
        logger.debug(error)
        return None

    try:
        pmids = pm_fetch.pmids_for_citation(**work.to_citation())

        if pmids:
            if (
                len(pmids) == 1
                and not pmids[0].startswith("NOT_FOUND")
                and not pmids[0].startswith("AMBIGUOUS")
            ):
                pma = pm_fetch.article_by_pmid(str(pmids[0]))
                if pma.doi == doi:
                    logger.debug(
                        "doi2pmid: Found PMID via PubMed advanced query for DOI %s", doi
                    )
                    return pma
    except BaseException:
        pass
    fpma = FakePubMedArticle(
        doi=work.doi,
        pmid=work.doi,
        title=work.title[0],
        abstract=work.abstract,
        year=str(work.pubyear),
        url=work.url,
        authors_str=work.authors_str_lastfirst if work.author else "",
        journal=work.container_title[0] if work.container_title else "",
    )
    return fpma


@sleep_and_retry
@limits(calls=10, period=1 if NCBI_API_KEY else 10)
def get_article(
    pm_fetcher: PubMedFetcher, cr_fetcher: CrossRefFetcher, identifier: str
) -> PubMedArticle:
    article: PubMedArticle = None
    if re.match(PMID_REGEX, identifier):
        article = pm_fetcher.article_by_pmid(identifier)
    elif re.match(PMCID_REGEX, identifier):
        article = pm_fetcher.article_by_pmcid(identifier)
    elif re.match(DOI_REGEX, identifier):
        article = doi2art(pm_fetcher, cr_fetcher, identifier)
    else:
        raise MetaPubError(f"Unknown identifier pattern for {identifier}")
    return article


@lru_cache(maxsize=None)
def get_fetchers() -> Tuple[PubMedFetcher, CrossRefFetcher]:
    return PubMedFetcher(), CrossRefFetcher()
