from pathlib import Path

from starlette.datastructures import UploadFile

from pyconverters_inscriptis.inscriptis import InscriptisConverter, InscriptisParameters


def test_inscriptis():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/test.html")
    result = Path(testdir, "data/test.txt")
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(UploadFile(source.name, fin), options)
        assert len(docs) == 1
        assert docs[0].title == "This is the title"
        assert len(docs[0].sentences) > 0
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<html>")


def test_table_in_table():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/table-in-table.html")
    result = Path(testdir, "data/table-in-table.txt")
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(UploadFile(source.name, fin), options)
        assert len(docs) == 1
        assert len(docs[0].sentences) > 0
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<h1>")


def test_table_pre():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/table-pre.html")
    result = Path(testdir, "data/table-pre.txt")
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(UploadFile(source.name, fin), options)
        assert len(docs) == 1
        assert len(docs[0].sentences) > 0
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<h1>")


def test_encodings():
    testdir = Path(__file__).parent
    for enc in ["utf-8", "windows-1252", "shift_jis"]:
        source = Path(testdir, f"data/page_{enc}.html")
        with source.open("rb") as fin:
            converter = InscriptisConverter()
            options = InscriptisParameters()
            docs = converter.convert(UploadFile(source.name, fin), options)
            assert len(docs) == 1
            assert len(docs[0].sentences) > 0
            assert docs[0].properties["encoding"] == enc


def test_xhtml():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/sample_odt.html")
    result = Path(testdir, "data/sample_odt.txt")
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(UploadFile(source.name, fin), options)
        assert len(docs) == 1
        assert len(docs[0].sentences) > 0
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<!DOCTYPE html PUBLIC")
