from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_csv.excel import ExcelKnowledgeParser, ExcelOptionsModel


def check_expected(concepts):
    assert len(concepts) == 92
    c7: Term = concepts[7]
    assert c7.identifier == "https://opendata.inra.fr/EMTD/8"
    assert c7.preferredForm == "specific pathogen-free animal"
    assert len(c7.properties["altForms"]) == 2
    assert set(c7.properties["altForms"]) == {
        "SPF animal",
        "specific pathogen free animal",
    }


def test_xls():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Digestion.xls")
    parser = ExcelKnowledgeParser()
    options = ExcelOptionsModel(
        encoding="utf-8",
        identifier_col="ID",
        preferredForm_col="prefLabel_en",
        altForms_cols="altLabel_en",
        multivalue_separator="|",
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)


def test_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Digestion.xlsx")
    parser = ExcelKnowledgeParser()
    options = ExcelOptionsModel(
        encoding="utf-8",
        identifier_col="ID",
        preferredForm_col="prefLabel_en",
        altForms_cols="altLabel_en",
        multivalue_separator="|",
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)


def test_NAF():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Liste-des-codes-APE-NAF-excel-2017.xlsx")
    parser = ExcelKnowledgeParser()
    options = ExcelOptionsModel(
        encoding="utf-8", identifier_col="Id", preferredForm_col="Term"
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 1728


def test_zippd_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/lexicon.xlsx.zip")
    parser = ExcelKnowledgeParser()
    options = ExcelOptionsModel(
        identifier_col="identifier",
        preferredForm_col="preferredForm",
        altForms_cols="altForms",
        multivalue_separator="|",
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 11
    c7: Term = concepts[7]
    assert c7.identifier == "8"
    assert c7.preferredForm == "Explosives: missiles"
    assert len(c7.properties["altForms"]) == 15
    assert "Tomahawk" in c7.properties["altForms"]


def test_SHERPA_1348():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Lex_sample.xlsx")
    parser = ExcelKnowledgeParser()
    options = ExcelOptionsModel(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    c0 = concepts[0]
    assert c0.identifier == "1"
    assert c0.properties["altForms"] != "nan"
