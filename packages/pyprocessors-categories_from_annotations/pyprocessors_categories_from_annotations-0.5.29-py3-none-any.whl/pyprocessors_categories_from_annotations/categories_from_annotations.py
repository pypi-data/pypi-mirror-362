from collections import defaultdict
from enum import Enum
from itertools import groupby
from typing import Type, cast, List

from collections_extended import RangeMap
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Category, Annotation

logger = Logger("pymultirole")


class ProcessingUnit(str, Enum):
    document = "document"
    segment = "segment"


class CategoriesFromAnnotationsParameters(ProcessorParameters):
    use_gazetteer: bool = Field(False,
                                description="If true use preferred from of gazetteer annotation as category label")
    multi_label_threshold: float = Field(0.5,
                                         description="only categories with a score greater than threshold are kept")
    processing_unit: ProcessingUnit = Field(
        ProcessingUnit.document,
        description="""The processing unit to apply the classification in the input
                                            documents, can be one of:<br/>
                                            <li>`document`
                                            <li>`segment`""", extra="advanced"
    )


class CategoriesFromAnnotationsProcessor(ProcessorBase):
    """Create categories from annotations"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: CategoriesFromAnnotationsParameters = cast(CategoriesFromAnnotationsParameters, parameters)
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if params.processing_unit == ProcessingUnit.document:
                    document.categories = create_categories_from_annotations(document.annotations, params.multi_label_threshold, params.use_gazetteer)
                    document.annotations = None
                elif document.sentences:
                    grouped = group_annotations_by_sentences(document)
                    for isent, sent in enumerate(document.sentences):
                        sent.categories = create_categories_from_annotations(grouped[isent], params.multi_label_threshold, params.use_gazetteer)
                    document.annotations = None
                    document.categories = []
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return CategoriesFromAnnotationsParameters


def create_categories_from_annotations(annotations, threshold=0.0, use_gazetteer=False):
    categories = []
    if annotations:
        anns = defaultdict(list)
        for a in annotations:
            if use_gazetteer:
                if has_knowledge(a):
                    for term in a.terms:
                        anns[term.preferredForm].append(a)
            else:
                anns[a.labelName].append(a)
        for lbl, alist in anns.items():
            a = alist[0]
            score = float(len(alist) / len(annotations))
            if score > threshold:
                categories.append(Category(label=lbl,
                                           score=score))
    return categories


def group_annotations_by_sentences(document: Document):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    groups = defaultdict(list)
    sentMap = RangeMap()
    if document.sentences:
        for isent, sent in enumerate(document.sentences):
            sentMap[sent.start:sent.end] = isent

    def by_sentenceid(a: Annotation):
        return sentMap.get(a.start)

    for k, g in groupby(document.annotations, by_sentenceid):
        sorted_group = sorted(g, key=get_sort_key, reverse=True)
        groups[k] = sorted_group

    return groups


def has_knowledge(a: Annotation):
    return a.terms is not None and a.terms
