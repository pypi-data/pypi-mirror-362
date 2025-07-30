import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document
from starlette.responses import Response

from pyformatters_afp_quality.afp_quality import (
    AFPQualityFormatter,
    AFPQualityParameters,
    CompareWith,
)


def test_metadata_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_doc.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = AFPQualityFormatter()
        options = AFPQualityParameters(text=True)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert (
            resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        result = Path(testdir, "data/afp_doc.xlsx")
        with result.open("wb") as fout:
            fout.write(resp.body)


def test_creator_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/326V7RT.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs)
        formatter = AFPQualityFormatter()
        options = AFPQualityParameters(text=True, compare=CompareWith.CREATOR)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert (
            resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        result = Path(testdir, "data/326V7RT.xlsx")
        with result.open("wb") as fout:
            fout.write(resp.body)


def test_creator_es_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/336Y6FE.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs)
        formatter = AFPQualityFormatter()
        options = AFPQualityParameters(text=True, compare=CompareWith.CREATOR)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert (
            resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        result = Path(testdir, "data/336Y6FE.xlsx")
        with result.open("wb") as fout:
            fout.write(resp.body)


def test_creator_de_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/9X726G.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs)
        formatter = AFPQualityFormatter()
        options = AFPQualityParameters(text=True, compare=CompareWith.CREATOR)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert (
                resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        result = Path(testdir, "data/9X726G.xlsx")
        with result.open("wb") as fout:
            fout.write(resp.body)
