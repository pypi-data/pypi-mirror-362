import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_afp_sports.afp_sports import AFPSportsProcessor, AFPSportsParameters


def test_model():
    model = AFPSportsProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AFPSportsParameters


# Arrange
@pytest.fixture
def original_docs():
    original_docs = []
    testdir = Path(__file__).parent
    for f in (testdir / "data").glob("afp*.json"):
        with f.open("r") as fin:
            doc = json.load(fin)
            original_doc = Document(**doc)
            original_docs.append(original_doc)
    return original_docs


def test_afp_sports(original_docs):
    # linker
    processor = AFPSportsProcessor()
    parameters = AFPSportsParameters()
    parameters.ignore_topics = "20000965"
    docs = processor.process(original_docs, parameters)
    for doc in docs:
        fired_by_rule = [
            c.properties["firedBy"] for c in doc.categories if c.properties
        ]
        assert len(fired_by_rule) > 0


def get_bug_documents(bug):
    datadir = Path(__file__).parent / "data"
    docs = {}
    for bug_file in datadir.glob(f"{bug}*.json"):
        with bug_file.open("r") as fin:
            doc = json.load(fin)
            doc['identifier'] = bug_file.stem
            docs[bug_file.stem] = Document(**doc)
    myKeys = list(docs.keys())
    myKeys.sort()
    sorted_docs = {i: docs[i] for i in myKeys}
    return list(sorted_docs.values())


def write_bug_result(bug, docs):
    datadir = Path(__file__).parent / "data"
    result = Path(datadir, f"result_{bug}.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# [AFP] Rule-based classification for sports is too noisy
def test_SHERPA_17777():
    docs = get_bug_documents("SHERPA-1777")
    processor = AFPSportsProcessor()
    parameters = AFPSportsParameters()
    docs = processor.process(docs, parameters)
    write_bug_result("SHERPA-1777", docs)
    doc0 = docs[0]
    cats = [c.label for c in doc0.categories]
    assert all(["horse racing" not in cat for cat in cats])
    assert all(["boxing" not in cat for cat in cats])
    assert all(["soccer" not in cat for cat in cats])

    doc1 = docs[1]
    cats = [c.label for c in doc1.categories]
    assert all(["horse racing" not in cat for cat in cats])
    # assert all(["padel" not in cat for cat in cats])
    assert all(["rugby union" not in cat for cat in cats])
