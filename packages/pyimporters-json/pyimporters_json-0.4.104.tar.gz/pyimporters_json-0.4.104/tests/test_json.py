from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_json.json_sherpa import JSONKnowledgeParser, JSONOptionsModel


def test_json():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/organization_en.json")
    parser = JSONKnowledgeParser()
    options = JSONOptionsModel()
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 1527
    c7: Term = concepts[7]
    assert c7.identifier == "afporganization:2021"
    assert c7.preferredForm == "REYNOLDS AMERICAN"
    assert len(c7.properties["altForms"]) == 1
    assert "Reynolds American" in c7.properties["altForms"]


def test_zip():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/tmpymh9kthe.zip")
    parser = JSONKnowledgeParser()
    options = JSONOptionsModel()
    concepts = list(parser.parse(source, options.dict(), Bar("Processing")))
    assert len(concepts) == 3
    c0: Term = concepts[0]
    assert c0.identifier == "afpperson:1698"
    assert c0.properties["status"] == "W"
    c2: Term = concepts[2]
    assert c2.identifier == "afpperson:999999"
    assert c2.properties["status"] == "M"
