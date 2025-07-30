import json
from collections import defaultdict
from itertools import groupby
from pathlib import Path

import pytest
from pymultirole_plugins.v1.schema import Document, Annotation
from pyprocessors_consolidate.consolidate import (
    ConsolidateProcessor,
    ConsolidateParameters,
    ConsolidationType,
)


def by_lexicon(a: Annotation):
    if a.terms:
        return a.terms[0].lexicon
    else:
        return ""


def by_label(a: Annotation):
    return a.labelName or a.label


def group_annotations(doc: Document, keyfunc):
    groups = defaultdict(list)
    for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
        groups[k] = list(g)
    return groups


def test_model():
    model = ConsolidateProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == ConsolidateParameters


# Arrange
@pytest.fixture
def original_doc():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/response_1622736571452.json")
    with source.open("r") as fin:
        docs = json.load(fin)
        original_doc = Document(**docs[0])
        return original_doc


def assert_original_doc(original_doc):
    original_groups_lexicon = group_annotations(original_doc, by_lexicon)
    original_groups_label = group_annotations(original_doc, by_label)
    assert len(original_groups_lexicon[""]) == 22
    assert len(original_groups_lexicon["lex_location"]) == 1
    assert len(original_groups_lexicon["lex_person"]) == 8
    assert len(original_groups_label["organization"]) == 4
    assert len(original_groups_label["location"]) == 4
    assert len(original_groups_label["person"]) == 23
    return original_groups_lexicon, original_groups_label


def test_consolidate_linker(original_doc):
    # linker
    original_groups_lexicon, original_groups_label = assert_original_doc(original_doc)
    assert original_groups_lexicon is not None
    assert original_groups_label is not None
    doc = original_doc.copy(deep=True)
    processor = ConsolidateProcessor()
    parameters = ConsolidateParameters(type=ConsolidationType.linker)
    docs = processor.process([doc], parameters)
    consolidated: Document = docs[0]
    consolidated_groups_lexicon = group_annotations(consolidated, by_lexicon)
    assert len(original_doc.annotations) > len(consolidated.annotations)
    assert len(consolidated_groups_lexicon[""]) == 0


def test_consolidate_unknown(original_doc):
    # unknown
    original_groups_lexicon, original_groups_label = assert_original_doc(original_doc)
    assert original_groups_lexicon is not None
    assert original_groups_label is not None
    doc = original_doc.copy(deep=True)
    processor = ConsolidateProcessor()
    parameters = ConsolidateParameters(type=ConsolidationType.unknown)
    docs = processor.process([doc], parameters)
    consolidated: Document = docs[0]
    # consolidated_groups_lexicon = group_annotations(consolidated, by_lexicon)
    consolidated_groups_label = group_annotations(consolidated, by_label)
    assert len(original_doc.annotations) > len(consolidated.annotations)
    knowns_unknowns = defaultdict(list)
    for label, anns in consolidated_groups_label.items():
        k = "unknown" if label.startswith("unknown_") else "known"
        knowns_unknowns[k].extend(anns)
    assert len(knowns_unknowns["known"]) > 0
    assert len(knowns_unknowns["unknown"]) > 0


def test_consolidate_unknown_only(original_doc):
    # unknwon only
    original_groups_lexicon, original_groups_label = assert_original_doc(original_doc)
    assert original_groups_lexicon is not None
    assert original_groups_label is not None
    doc = original_doc.copy(deep=True)
    processor = ConsolidateProcessor()
    parameters = ConsolidateParameters(
        type=ConsolidationType.unknown_only, unknown_prefix="Candidate "
    )
    docs = processor.process([doc], parameters)
    consolidated: Document = docs[0]
    # consolidated_groups_lexicon = group_annotations(consolidated, by_lexicon)
    consolidated_groups_label = group_annotations(consolidated, by_label)
    assert len(original_doc.annotations) > len(consolidated.annotations)
    knowns_unknowns = defaultdict(list)
    for label, anns in consolidated_groups_label.items():
        k = "unknown" if label.startswith("candidate_") else "known"
        knowns_unknowns[k].extend(anns)
    assert len(knowns_unknowns["known"]) == 0
    assert len(knowns_unknowns["unknown"]) > 0


def test_kill():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/atos_demo-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = ConsolidateProcessor()
        parameters = ConsolidateParameters(
            type=ConsolidationType.default, kill_label="killed"
        )
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        consolidated_groups_label = group_annotations(consolidated, by_label)
        assert "killed" not in consolidated_groups_label.keys()


def test_acronyms():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/acronyms.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = ConsolidateProcessor()
        parameters = ConsolidateParameters(
            type=ConsolidationType.unknown, kill_label="killed"
        )
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        consolidated_groups_label = group_annotations(consolidated, by_label)
        assert "killed" not in consolidated_groups_label.keys()
        assert len(consolidated_groups_label["Acronym"]) > 0
        assert len(consolidated_groups_label["Expanded"]) > 0
        assert len(consolidated_groups_label["concept_4_3"]) > 0
        assert len(consolidated_groups_label["unknown_concept_4_3"]) > 0
        result = Path(testdir, "data/acronyms_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)
