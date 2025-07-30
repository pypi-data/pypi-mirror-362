import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document
from pyprocessors_categories_from_annotations.categories_from_annotations import CategoriesFromAnnotationsProcessor, \
    CategoriesFromAnnotationsParameters, ProcessingUnit


def test_model():
    model = CategoriesFromAnnotationsProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == CategoriesFromAnnotationsParameters


def test_categories_from_annotations():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/SHERPA-1776-1.json")

    with source.open("r") as fin:
        jdoc = json.load(fin)
    docs = [Document(**jdoc)]
    processor = CategoriesFromAnnotationsProcessor()
    parameters = CategoriesFromAnnotationsParameters()
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.categories) == 0

    docs = [Document(**jdoc)]
    parameters.multi_label_threshold = 0.0
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.categories) == 9

    docs = [Document(**jdoc)]
    parameters.processing_unit = ProcessingUnit.segment
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.categories) == 0
    sent0 = doc0.sentences[0]
    assert len(sent0.categories) == 1


def test_categories_from_gazetteer():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/chatbot_sales_marketing_ner-document-test.json")

    with source.open("r") as fin:
        jdoc = json.load(fin)
    docs = [Document(**jdoc)]
    processor = CategoriesFromAnnotationsProcessor()
    parameters = CategoriesFromAnnotationsParameters(use_gazetteer=True)
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.categories) == 1
    assert doc0.categories[0].label == "AFP News"
