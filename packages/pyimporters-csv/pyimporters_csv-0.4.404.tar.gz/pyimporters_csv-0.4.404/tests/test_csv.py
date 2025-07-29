from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_csv.csv_parser import CSVKnowledgeParser, CSVOptionsModel


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


def test_csv():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Digestion.csv")
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(
        encoding="utf-8",
        identifier_col="ID",
        preferredForm_col="prefLabel_en",
        altForms_cols="altLabel_en",
        multivalue_separator="|",
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)


def test_zipped_csv():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Digestion.zip")
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(
        encoding="utf-8",
        identifier_col="ID",
        preferredForm_col="prefLabel_en",
        altForms_cols="altLabel_en",
        multivalue_separator="|",
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)


def test_composers():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/composers.csv")
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 4
    c0 = concepts[0]
    assert c0.identifier == "Johann Sebastian Bach"
    assert c0.preferredForm == "Johann Sebastian Bach"


def test_lex1():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/lex1.csv")
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(
        encoding="utf-8",
        identifier_col="identifier",
        preferredForm_col="preferredForm",
        altForms_cols="altForms"
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    c0 = concepts[0]
    assert c0.identifier == "1|2"
    assert c0.preferredForm == "toto"
    assert c0.properties["altForms"] != "nan"


def test_vivo():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/Sample50Kategories4Vivo.csv")
    parser = CSVKnowledgeParser()
    options = CSVOptionsModel(
        encoding="utf-8",
        separator="\t",
        header=0,
        multivalue_separator=";",
        identifier_col="ID",
        preferredForm_col="PrefTerm",
        altForms_cols="AltTerm "
    )
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 81
    c0 = concepts[0]
    assert c0.identifier == 'b2find:3.2.1-de'
    assert c0.preferredForm == 'Mikrobiologie, Virologie Und Immunolog'
    assert len(c0.properties["altForms"]) == 15
