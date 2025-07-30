from pathlib import Path
from typing import List

import pytest
from jinja2 import Environment, FileSystemLoader
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.datastructures import UploadFile

from pyconverters_pubmedfetcher.pubmedfetcher import InputFormat
from pyconverters_pubmedfetcher.pubmedfetcher import (
    PubmedFetcherConverter,
    PubmedFetcherParameters,
)


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("journal",
                         [
                             'SAGE Open Medical Case Reports',
                             'Case Reports in Neurology',
                             'Case Reports in Oncology',
                             'Case Reports in Pediatrics',
                             'Case Reports in Psychiatry',
                         ])
def test_pubmedfetcher_query(journal):
    testdir = Path(__file__).parent
    tmpldir = testdir / "data"
    env = Environment(loader=FileSystemLoader(tmpldir))
    template = env.get_template('query.txt')
    converter = PubmedFetcherConverter()
    parameters = PubmedFetcherParameters(input_format=InputFormat.Query, retmax=100)
    output_from_parsed_template = template.render(journal=journal)
    source_tmpl = tmpldir / f"query_{journal}.txt"
    with source_tmpl.open("w") as fh:
        fh.write(output_from_parsed_template)

    with source_tmpl.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source_tmpl.name, fin, "text/plain"), parameters
        )
        sum_file = testdir / tmpldir / f"query_{journal}.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_pubmedfetcher_list():
    model = PubmedFetcherConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == PubmedFetcherParameters
    converter = PubmedFetcherConverter()
    parameters = PubmedFetcherParameters(input_format=InputFormat.ID_List)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/list.txt")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/plain"), parameters
        )
        assert len(docs) == 5
        assert docs[0].identifier == '34239458'
        assert docs[1].identifier == "21886606"
        assert docs[2].identifier == "21886599"
        assert docs[2].metadata["DOI"] == "10.2174/157015911795017263"
        assert docs[3].identifier == "10.18585/inabj.v12i2.1171"
        assert docs[3].metadata["DOI"] == "10.18585/inabj.v12i2.1171"
        assert docs[4].identifier == "21886588"
        assert docs[4].metadata["PMC"] == "3137179"


@pytest.mark.skip(reason="Not a test")
def test_pubmedfetcher_allids():
    model = PubmedFetcherConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == PubmedFetcherParameters
    converter = PubmedFetcherConverter()
    parameters = PubmedFetcherParameters(input_format=InputFormat.ID_List)
    testdir = Path(__file__).parent
    source = Path(testdir, "data/DOIs-only.txt")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/plain"), parameters
        )
        assert len(docs) == 153


def test_pubmedfetcher_xml():
    converter = PubmedFetcherConverter()
    parameters = PubmedFetcherParameters(
        input_format=InputFormat.XML_PubmedArticleSet, discard_if_no_abstract=False
    )
    testdir = Path(__file__).parent
    source = Path(testdir, "data/MedLine2021-09-06-19-04-11.xml")
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/xml"), parameters
        )
        assert len(docs) == 91
        assert docs[0].identifier == "21886606"
