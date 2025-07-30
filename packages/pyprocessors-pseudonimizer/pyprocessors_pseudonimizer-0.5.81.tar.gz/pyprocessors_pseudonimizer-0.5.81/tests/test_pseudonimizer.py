import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_pseudonimizer.pseudonimizer import (
    PseudonimizerProcessor,
    PseudonimizerParameters, OPERATOR_IDENTITY_STR
)


def test_pseudo1():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/afp_ner_fr-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        formatter = PseudonimizerProcessor()
        options = PseudonimizerParameters()
        options.mapping = {
            'wikidata': OPERATOR_IDENTITY_STR,
            'organization': json.dumps({
                "type": "mask",
                "masking_char": "X",
                "chars_to_mask": 3,
                "from_end": False,
            }),
            'afporganization': json.dumps({
                "type": "faker",
                "provider": "company",
                "locale": "en_US"
            }),
            'person': json.dumps({
                "type": "faker",
                "provider": "name",
                "locale": "fr_FR"
            }),
            'afpperson': json.dumps({
                "type": "faker",
                "provider": "name",
                "locale": "fr_FR"
            }
            )
        }
        anonymizeds = formatter.process([doc], options)
        norm_file = testdir / "data/afp_ner_fr-document-test-anon.json"
        dl = DocumentList(__root__=anonymizeds)
        with norm_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_pseudo2():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/terrorisme_ner_v2-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        formatter = PseudonimizerProcessor()
        options = PseudonimizerParameters()
        options.mapping = {
            'victimes': json.dumps({"type": "replace", "new_value": "_ANONYMIZED_NB_"}),
            'date': json.dumps({"type": "faker", "provider": "date_between", "locale": "fr_FR"}),
            'organisation': json.dumps({"type": "faker", "provider": "random_element",
                                        "elements": ["Al-Qaïda", "FARC", "Boko Haram", "Organisation État islamique"]})
        }
        anonymizeds = formatter.process([doc], options)
        norm_file = testdir / "data/terrorisme_ner_v2-document-test-anon.json"
        dl = DocumentList(__root__=anonymizeds)
        with norm_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_pseudo3():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/mindspeak_demo-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        formatter = PseudonimizerProcessor()
        options = PseudonimizerParameters(default_operator=json.dumps({'type': 'redact'}))
        options.mapping = {
            'person': json.dumps({'type': 'replace', 'new_value': '_ANONYMIZED_'})
        }
        anonymizeds = formatter.process([doc], options)
        norm_file = testdir / "data/mindspeak_demo-document-test-anon.json"
        dl = DocumentList(__root__=anonymizeds)
        with norm_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
