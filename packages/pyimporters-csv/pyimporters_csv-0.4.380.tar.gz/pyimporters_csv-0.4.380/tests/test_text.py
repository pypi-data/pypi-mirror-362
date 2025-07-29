from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_csv.text import TXTKnowledgeParser, TXTOptionsModel


def check_expected(concepts):
    assert len(concepts) == 158
    c1: Term = concepts[2]
    assert c1.identifier == "Euro"
    assert c1.preferredForm is None
    assert c1.properties is None


def test_text():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/currencies.txt")
    parser = TXTKnowledgeParser()
    options = TXTOptionsModel(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)


def test_zipped_text():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/currencies.zip")
    parser = TXTKnowledgeParser()
    options = TXTOptionsModel(encoding="utf-8")
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    check_expected(concepts)
