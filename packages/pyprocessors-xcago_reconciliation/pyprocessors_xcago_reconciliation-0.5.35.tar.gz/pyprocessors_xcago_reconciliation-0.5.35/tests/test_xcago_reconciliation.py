import json
from pathlib import Path

from dirty_equals import IsPartialDict, Contains
from pymultirole_plugins.v1.schema import Document, Annotation, DocumentList
from pytest_check import check

from pyprocessors_xcago_reconciliation.xcago_reconciliation import (
    XCagoReconciliationProcessor,
    XCagoReconciliationParameters,
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
    model = XCagoReconciliationProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == XCagoReconciliationParameters


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


def test_xcago_reconciliation_whitelist():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/afp_ner_fr-document-test-whitelist2.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
    # linker
    doc = original_doc.copy(deep=True)
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(white_label="white")
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
        processor = XCagoReconciliationProcessor()
        parameters = XCagoReconciliationParameters()
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        # consolidated_groups_label = group_annotations(consolidated.annotations, by_label)
        result = Path(testdir, "data/x_cago_ner_en-document_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)


def test_x_cago_de():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/xcago_ner_de-document-test.json")
    with source.open("r") as fin:
        doc = json.load(fin)
        original_doc = Document(**doc)
        processor = XCagoReconciliationProcessor()
        parameters = XCagoReconciliationParameters(whitelisted_lexicons=["authors"], resolve_lastnames=True)
        docs = processor.process([original_doc.copy(deep=True)], parameters)
        consolidated: Document = docs[0]
        assert len(original_doc.annotations) > len(consolidated.annotations)
        result = Path(testdir, "data/xcago_ner_de-document-test_conso.json")
        with result.open("w") as fout:
            json.dump(consolidated.dict(), fout, indent=2)


# In Escrim xcago_reconciliation White list does not assign the right label
def test_SHERPA_2463():
    original_docs = get_bug_documents("SHERPA-2463")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(white_label="white",
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

    parameters = XCagoReconciliationParameters(
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


# Allow wikidata concepts wider than model annotation
def test_SHERPA_XXX1():
    original_docs = get_bug_documents("SHERPA-XXX1")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(wikidata_partial=True,
                                          resolve_lastnames=True)
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    olaf_scholz = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'Olaf Scholz')
    with check:
        assert olaf_scholz == IsPartialDict(label='Person', text='Olaf Scholz', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Olaf Scholz',
                          identifier='Q61053')
        ))

    doc2 = docs[2]
    abdullah_2 = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc2.annotations if
             a.text == 'Abdullah II.')
    with check:
        assert abdullah_2 == IsPartialDict(label='Person', text='Abdullah II.', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Abdullah II. bin al-Hussein',
                          identifier='Q57464')
        ))


# Allow wikidata location sub entities in other wider annotations
def test_SHERPA_XXX2():
    original_docs = get_bug_documents("SHERPA-XXX2")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(wikidata_partial=True,
                                          resolve_lastnames=True)
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    china = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'China')
    caeg = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
             a.text == 'China Arts and Entertainment Group')
    with check:
        assert china == IsPartialDict(label='Location', text='China', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='China',
                          identifier='Q148')
        ))
        assert caeg == IsPartialDict(label='Organization', text='China Arts and Entertainment Group', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='China Arts and Entertainment Group',
                          identifier='Q16829463')
        ))

    doc1 = docs[1]
    madrid = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc1.annotations if
             a.text == 'Madrid')
    real_madrid = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc1.annotations if
             a.text == 'Real Madrid')
    with check:
        assert madrid == IsPartialDict(label='Location', text='Madrid', terms=Contains(
            IsPartialDict(lexicon='wikidata',
                          identifier='Q5756')
        ))
        assert real_madrid == IsPartialDict(label='Organization', text='Real Madrid', terms=Contains(
            IsPartialDict(lexicon='wikidata',
                          identifier='Q54922')
        ))

    doc2 = docs[2]
    madrid = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc2.annotations if
                  a.text == 'Madrid')
    real_madrid = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc2.annotations if
                       a.text == 'Real Madrid')
    with check:
        assert madrid == IsPartialDict(label='Location', text='Madrid', terms=Contains(
            IsPartialDict(lexicon='wikidata',
                          identifier='Q5756')
        ))
        assert real_madrid == IsPartialDict(text='Real Madrid', terms=Contains(
            IsPartialDict(lexicon='wikidata',
                          identifier='Q54922')
        ))

    doc3 = docs[3]
    brazilian = next(a.dict(exclude_none=True, exclude_unset=True) for a in doc3.annotations if
                  a.text == 'Brazilian')
    with check:
        assert len(brazilian['terms']) == 1
        assert brazilian == IsPartialDict(label='Location', text='Brazilian', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Brazil',
                          identifier='Q155')
        ))


# Compute fingerprint
def test_SHERPA_XXX3():
    original_docs = get_bug_documents("SHERPA-XXX3")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(wikidata_partial=True,
                                          resolve_lastnames=True)
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    assert doc0.altTexts[0] == IsPartialDict(name='fingerprint')


# Wikidata Kill list
def test_SHERPA_XXX4():
    original_docs = get_bug_documents("SHERPA-XXX4")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(wikidata_partial=True,
                                               resolve_lastnames=True)
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    wang_jins = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                 a.text == 'Wang Jin']
    donalds = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
               a.text == 'Donald']
    gettys = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'GETTY']
    trumps = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'Trump']
    bidens = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'Biden']
    with check:
        assert len(wang_jins) == 1
        assert wang_jins[0] == IsPartialDict(label='Person', text='Wang Jin', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Wang Jin (archer)',
                          identifier='Q48307579')
        ))
        assert len(donalds) == 0
        assert len(gettys) == 1
        assert len(trumps) == 1
        assert trumps[0] == IsPartialDict(label='Person', text='Trump', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Donald Trump',
                          identifier='Q22686')
        ))
        assert len(bidens) == 1
        assert bidens[0] == IsPartialDict(label='Person', text='Biden', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Joe Biden',
                          identifier='Q6279')
        ))

    original_docs = get_bug_documents("SHERPA-XXX4")
    parameters.wikidata_kill_label = "wikidata_kill"
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    wang_jins = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
                 a.text == 'Wang Jin']
    donalds = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
               a.text == 'Donald']
    gettys = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'GETTY']
    trumps = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'Trump']
    bidens = [a.dict(exclude_none=True, exclude_unset=True) for a in doc0.annotations if
              a.text == 'Biden']
    with check:
        assert len(wang_jins) == 1
        assert 'terms' not in wang_jins[0]
        assert len(donalds) == 0
        assert len(gettys) == 0
        assert len(trumps) == 1
        assert trumps[0] == IsPartialDict(label='Person', text='Trump', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Donald Trump',
                          identifier='Q22686')
        ))
        assert len(bidens) == 1
        assert bidens[0] == IsPartialDict(label='Person', text='Biden', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Joe Biden',
                          identifier='Q6279')
        ))

    doc1 = docs[1]
    trumps = [a.dict(exclude_none=True, exclude_unset=True) for a in doc1.annotations if
              a.text == 'Trump']
    bidens = [a.dict(exclude_none=True, exclude_unset=True) for a in doc1.annotations if
              a.text == 'Biden']
    with check:
        assert len(trumps) == 1
        assert trumps[0] == IsPartialDict(label='Person', text='Trump', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Donald Trump',
                          identifier='Q22686')
        ))
        assert len(bidens) == 3
        assert bidens[0] == IsPartialDict(label='Person', text='Biden', terms=Contains(
            IsPartialDict(lexicon='wikidata', preferredForm='Joe Biden',
                          identifier='Q6279')
        ))

    doc2 = docs[2]
    pios = [a.dict(exclude_none=True, exclude_unset=True) for a in doc2.annotations if
            a.text == 'Pio']
    with check:
        assert len(pios) == 0

    doc3 = docs[3]
    nicaraguans = [a.dict(exclude_none=True, exclude_unset=True) for a in doc3.annotations if
                   a.text == 'Nicaraguan']
    with check:
        assert len(nicaraguans) == 1

    doc4 = docs[4]
    germanys = [a.dict(exclude_none=True, exclude_unset=True) for a in doc4.annotations if
                a.text == "Germany’s"]
    with check:
        assert len(germanys) == 1


# Restore original text
def test_SHERPA_XXX5():
    original_docs = get_bug_documents("SHERPA-XXX5")
    processor = XCagoReconciliationProcessor()
    parameters = XCagoReconciliationParameters(wikidata_partial=True,
                                               resolve_lastnames=True)
    docs = processor.process(original_docs, parameters)
    doc0 = docs[0]
    with check:
        for a in doc0.annotations:
            assert a.text == doc0.text[a.start:a.end]
