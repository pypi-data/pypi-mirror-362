import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document
from pyprocessors_iptc_mapper.iptc_mapper import IPTCMapper, \
    IPTCMapperParameters


def test_model():
    model = IPTCMapper.get_model()
    model_class = model.construct().__class__
    assert model_class == IPTCMapperParameters


def test_iptc_mapper():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/x_cago_iptc_de-document-test.json")

    with source.open("r") as fin:
        jdoc = json.load(fin)
    docs = [Document(**jdoc)]
    processor = IPTCMapper()
    parameters = IPTCMapperParameters(label2iptc_mapping={
        'automobile_industry': '20000296',
        'automobile_review': '20000566',
        'motorcycle_industry': '20000571',
        'motorcycles': '20000571',
        'other': '',
    })
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len([c for c in doc0.categories if 'automobile enthusiasm' in c.label]) == 1
