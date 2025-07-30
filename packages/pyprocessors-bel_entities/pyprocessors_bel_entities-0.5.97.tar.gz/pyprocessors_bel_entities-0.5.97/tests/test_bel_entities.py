import json
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document, DocumentList
from pyprocessors_bel_entities.bel_entities import BELEntitiesProcessor, BELEntitiesParameters


# Arrange
@pytest.fixture
def original_docs():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/response_1642503730100.json')
    with source.open("r") as fin:
        docs = json.load(fin)
        original_docs = [Document(**doc) for doc in docs]
        return original_docs


def test_bel_entities(original_docs):
    testdir = Path(__file__).parent
    docs = [original_doc.copy(deep=True) for original_doc in original_docs]
    processor = BELEntitiesProcessor()
    parameters = BELEntitiesParameters(kill_label='killed')
    docs = processor.process(docs, parameters)
    doc0: Document = docs[0]
    assert len(doc0.annotations) < len(original_docs[0].annotations)
    dl = DocumentList(__root__=docs)
    json_file = testdir / "data/bel_relations.json"
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    pass
