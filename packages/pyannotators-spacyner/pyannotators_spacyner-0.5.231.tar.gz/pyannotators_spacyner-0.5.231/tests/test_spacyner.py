import json
import string
from collections import defaultdict, Counter
from pathlib import Path
from typing import List

import pandas as pd
import pytest as pytest
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pybel.parser import BELParser
from pymultirole_plugins.v1.schema import Document, DocumentList, Sentence

from pyannotators_spacyner.spacyner import SpacyNERAnnotator, SpacyNERParameters


def test_spacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters()
    docs: List[Document] = annotator.annotate([Document(
        text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
        metadata={'language': 'en'})], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 4
    paris = doc0.annotations[0]
    france = doc0.annotations[1]
    macron = doc0.annotations[2]
    republic = doc0.annotations[3]
    assert paris.label == 'GPE'
    assert france.label == 'GPE'
    assert macron.label == 'PERSON'
    assert republic.label == 'GPE'

    parameters.mapping = {
        "location": ["LOC", "GPE"],
        "person": ["PERSON"],
        "organization": ["ORG"]
    }
    docs: List[Document] = annotator.annotate(
        [
            Document(
                text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
                metadata={'language': 'en'},
            )
        ],
        parameters
    )
    doc0 = docs[0]
    assert len(doc0.annotations) == 4
    paris = doc0.annotations[0]
    france = doc0.annotations[1]
    macron = doc0.annotations[2]
    republic = doc0.annotations[3]
    assert paris.labelName == "location"
    assert france.labelName == "location"
    assert macron.labelName == "person"
    assert republic.labelName == "location"


def test_scispacyner():
    model = SpacyNERAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == SpacyNERParameters
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model_type='sci')
    docs: List[Document] = annotator.annotate([Document(
        text="Myeloid derived suppressor cells (MDSC) are immature myeloid cells with immunosuppressive activity.\nThey accumulate in tumor-bearing mice and humans with different types of cancer, including hepatocellular carcinoma (HCC).",
        metadata={'language': 'en'})], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) == 12


def to_camel_case(s):
    return s[0].lower() + string.capwords(s, sep='_').replace('_', '')[1:] if s else s


@pytest.mark.skip(reason="Not a test")
def test_scai_parse():
    testdir = Path(__file__).parent / 'data'
    excel_file = testdir / "all_bel_relations.xlsx"
    bel_df = pd.read_excel(excel_file).fillna(value="")
    docs = {}
    docids = Counter()
    for index, row in bel_df.iterrows():
        subject = row['Subject']
        relation = row['Relation']
        object = row['Object']
        docid = str(row['PubMedID'])
        sentence = row['EvidenceSentence']
        title = row['PublicationTitle']
        sent = subject + " " + to_camel_case(relation) + " " + object
        docids.update([docid])
        docinc = docids[docid]
        doc = docs.get((docid, sentence))
        if doc is None:
            doc = Document(identifier=f"{docid}-{docinc}", title=title, text=sentence,
                           sentences=[Sentence(start=0, end=len(sentence))], metadata={"bel_sentences": [sent]})
            docs[(docid, sentence)] = doc
        else:
            doc.metadata['bel_sentences'].append(sent)
        # parsed_sent = pybel.parse(sent)
    dl = DocumentList(__root__=list(docs.values()))
    json_file = testdir / "all_bell_relations.json"
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_scai():
    annotator = SpacyNERAnnotator()
    parameters = SpacyNERParameters(model_type='sci', scispacy_linker='umls',
                                    types_filter=','.join(
                                        ['T028', 'T116', 'T123', 'T126', 'T043', 'T047', 'T121', 'T109',
                                         'T026', 'T025', 'T129', 'T192', 'T044', 'T048', 'T043', 'T131',
                                         'T125', 'T043', 'T130', 'T196', 'T005', 'T008', 'T010', 'T012',
                                         'T013', 'T014', 'T015', 'T016', 'T017', 'T018', 'T021', 'T022',
                                         'T023', 'T024', 'T025', 'T026'
                                         ]))
    parameters = SpacyNERParameters(model='en_core_sci_sm', scispacy_linker='umls')
    testdir = Path(__file__).parent / 'data'
    json_file = testdir / "all_bell_relations.json"
    with json_file.open("r") as fin:
        docs = json.load(fin)
    docs = [Document(**doc) for doc in docs]
    docs = annotator.annotate(docs, parameters)
    json_file = testdir / f"all_bell_relations_annotated_{parameters.scispacy_linker.value}.json"
    dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def find_in_forms(el, forms):
    for k in el:
        if 'name' in el[k]:
            name = el[k]['name']
            if name.lower() in forms:
                return k
    return None


def fuzzy_find_in_forms(el, forms, threshold=85):
    for k in el:
        if isinstance(el[k], dict):
            if 'name' in el[k]:
                name = el[k]['name']
                extracted = process.extractOne(name.lower(), forms, scorer=fuzz.WRatio)
                if extracted[1] > threshold:
                    copy_el = {k1: v1 for k1, v1 in el.items() if k1 in ['function', k]}
                    return copy_el
        elif k == 'members' and isinstance(el[k], list):
            for subel in el[k]:
                ret = fuzzy_find_in_forms(subel, forms, threshold)
                if ret is not None:
                    return ret
    return None


def add2rows(el, rows):
    row = {}
    for k in el:
        if k == "function":
            row[k] = el[k]
        elif 'namespace' in el[k]:
            row[k] = el[k]['namespace']
    rows.append(row)


greek_alphabet = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
latin_alphabet = 'AaBbGgDdEeZzHhJjIiKkLlMmNnXxOoPpRrSssTtUuFfQqYyWw'
greek2latin = str.maketrans(greek_alphabet, latin_alphabet)


@pytest.mark.skip(reason="Not a test")
def test_scai_eval():
    testdir = Path(__file__).parent / 'data'
    linker = "umls"
    bel_parser = BELParser(skip_validation=True, citation_clearing=False, allow_naked_names=True)
    log_file = testdir / f"all_bell_relations_annotated_{linker}.log"
    with log_file.open("w") as log:
        json_file = testdir / f"all_bell_relations_annotated_{linker}.json"
        with json_file.open("r") as fin:
            docs = json.load(fin)
        docs = [Document(**doc) for doc in docs]
        rows = []
        functions = defaultdict(list)
        ok = 0
        for doc in docs:
            bel_sents = doc.metadata.get("bel_sentences", [])
            bels = []
            for bel_sent in bel_sents:
                try:
                    bels.append(bel_parser.parse(bel_sent))
                except BaseException:
                    print(f"Invalid BEL sentence: {bel_sent}")
                    bels.append(None)
            doc.metadata["bels"] = bels
            for a in doc.annotations:
                a.properties = defaultdict(list)
                forms = set()
                forms.add(a.text.lower())
                forms.add(a.text.translate(greek2latin).lower())
                for term in a.terms:
                    forms.add(term.preferredForm.lower())
                    if term.properties:
                        forms.update([f.lower() for f in term.properties.get('aliases', [])])
                a.properties['forms'] = list(forms)

            new_bels = []
            new_bel_sentences = []
            for ibel, bel in enumerate(doc.metadata['bels']):
                if bel is not None:
                    bel_sentence = doc.metadata['bel_sentences'][ibel]
                    src_found, tgt_found = False, False
                    source = bel['source']
                    add2rows(source, rows)
                    target = bel['target']
                    add2rows(target, rows)
                    for a in doc.annotations:
                        forms = a.properties['forms']
                        copy_source = fuzzy_find_in_forms(source, forms)
                        if copy_source is not None:
                            a.properties['source'].append(json.dumps(copy_source))
                            a.label = copy_source['function']
                            a.labelName = a.label.lower()
                            if a.terms:
                                for term in a.terms:
                                    functions[source['function']].extend(term.properties['types'])
                            if 'concept' in copy_source:
                                src_found = True
                        copy_target = fuzzy_find_in_forms(target, forms)
                        if copy_target is not None:
                            a.properties['target'].append(json.dumps(copy_target))
                            a.label = copy_target['function']
                            a.labelName = a.label.lower()
                            if a.terms:
                                for term in a.terms:
                                    functions[source['function']].extend(term.properties['types'])
                            if 'concept' in copy_target:
                                tgt_found = True
                    if src_found and tgt_found:
                        new_bels.append(bel)
                        new_bel_sentences.append((bel_sentence))
                    else:
                        print(f"Not found in sentence: {doc.text}", file=log)
                        print(f"BEL sentence: {bel_sentence}", file=log)
                        if not src_found:
                            print(f"\t- {source}", file=log)
                        if not tgt_found:
                            print(f"\t- {target}", file=log)
            del doc.metadata['bels']
            doc.metadata['bel_sentences'] = new_bel_sentences
            if len(new_bels) > 0:
                ok += 1
                doc.metadata['corpus'] = "train"
            else:
                doc.metadata['corpus'] = "test"
            for a in doc.annotations:
                del a.properties['forms']
                if 'source' in a.properties:
                    a.properties['source'] = [json.loads(x) for x in list(set(a.properties['source']))]
                if 'target' in a.properties:
                    a.properties['target'] = [json.loads(x) for x in list(set(a.properties['target']))]
        print(f"{ok}/{len(docs)} complete sentences")
        c = Counter()
        for function, flist in functions.items():
            print(function)
            print(Counter(flist))
            c = c + Counter(flist)
        print(c, file=log)
        print([k for k, v in c.items() if v >= 100])
        row_file = testdir / f"all_bell_relations_matched_{linker}.xlsx"
        df = pd.DataFrame.from_records(rows)
        df['function'].value_counts()
        df['concept'].value_counts()
        df['location'].value_counts()
        df.groupby('function').count()
        df.to_excel(row_file)
        json_file = testdir / f"all_bell_relations_matched_{linker}.json"
        dl = DocumentList(__root__=docs)
    with json_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
