import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList
from pyprocessors_capitalizer.capitalizer import CapitalizerProcessor, CapitalizerParameters


def test_capitalizer():
    annotator = CapitalizerProcessor()
    parameters = CapitalizerParameters()
    testdir = Path(__file__).parent / 'data'
    json_file = testdir / "x_cago_ner_de-document-test2.json"
    with json_file.open("r") as fin:
        doc = json.load(fin)
    original_text = doc['text']
    docs = [Document(**doc)]
    docs = annotator.process(docs, parameters)
    new_text = docs[0].text
    assert len(new_text) == len(original_text)
    assert len(new_text) == len(docs[0].altTexts[0].text)
    json_file = testdir / "x_cago_ner_de-document-new2.json"
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
