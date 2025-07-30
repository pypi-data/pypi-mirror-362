import json
from pathlib import Path

from dirty_equals import IsPartialDict, Contains
from pymultirole_plugins.v1.schema import Document, Annotation, DocumentList
from pytest_check import check

from pyprocessors_reconciliation.reconciliation import (
    ReconciliationProcessor,
    ReconciliationParameters,
    group_annotations,
)


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


def write_bug_result(bug, docs, type):
    datadir = Path(__file__).parent / "data"
    result = Path(datadir, f"result_{bug}_{type}.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_model():
    model = ReconciliationProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == ReconciliationParameters


def by_lexicon(a: Annotation):
    if a.terms:
        return a.terms[0].lexicon
    else:
        return ""


def by_label(a: Annotation):
    return a.labelName or a.label


def by_linking(a: Annotation):
    if a.terms:
        links = sorted({t.lexicon.split("_")[0] for t in a.terms})
        return "+".join(links)
    else:
        return "candidate"


def test_reconciliation_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = ReconciliationProcessor()
    parameters = ReconciliationParameters(white_label="white")
    docs = processor.process([doc], parameters)
    conso: Document = docs[0]
    assert len(conso.annotations) < len(original_doc.annotations)
    conso_groups = group_annotations(conso.annotations, by_linking)
    assert len(conso_groups["candidate"]) == 1
    assert len(conso_groups["wikidata"]) == 6


def test_x_cago_en():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/x_cago_ner_en-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = ReconciliationProcessor()
        parameters = ReconciliationParameters()
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        # consolidated_groups_label = group_annotations(consolidated.annotations, by_label)
        result = Path(testdir, "data/x_cago_ner_en-document_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)


def test_x_cago_de():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/x_cago_ner_ge-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = ReconciliationProcessor()
        parameters = ReconciliationParameters(resolve_lastnames=True)
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        result = Path(testdir, "data/x_cago_ner_ge-document_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)


# In Escrim reconciliation White list does not assign the right label
def test_SHERPA_2463():
    original_docs = get_bug_documents("SHERPA-2463")
    processor = ReconciliationProcessor()
    parameters = ReconciliationParameters(white_label="white",
                                          resolve_lastnames=True)
    totos = [a.dict(exclude_none=True, exclude_unset=True) for a in original_docs[0].annotations if
             a.text == 'Toto']
    with check:
        assert len(totos) == 2

    docs = processor.process([original_docs[0]], parameters)
    doc0 = docs[0]
    totos = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'Toto']
    with check:
        assert len(totos) == 1
        assert totos[0] == IsPartialDict(label='Personne', text='Toto', terms=Contains(
            IsPartialDict(lexicon='escrim_person', preferredForm='Toto',
                          identifier='Toto')
        ))

    parameters = ReconciliationParameters(
        whitelisted_lexicons=["escrim_person", "person"],
        resolve_lastnames=True)
    totos = [a.dict(exclude_none=True, exclude_unset=True) for a in original_docs[1].annotations if
             a.text == 'Toto' and a.label == 'Personne']
    with check:
        assert len(totos) == 1

    docs = processor.process(original_docs[1:], parameters)
    write_bug_result("SHERPA-2463", docs, parameters.type)
    doc0 = docs[0]
    totos = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'Toto']

    paris = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'Paris')

    with check:
        assert len(totos) == 1
        assert totos[0] == IsPartialDict(label='Personne', text='Toto', terms=Contains(
            IsPartialDict(lexicon='escrim_person', preferredForm='Toto',
                          identifier='Toto')
        ))

        assert paris == IsPartialDict(label='Lieu', text='Paris',
                                      terms=Contains(IsPartialDict(lexicon='wikidata', preferredForm='Paris',
                                                                   identifier='Q90')))
