import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document
from pyprocessors_standoff2inline.standoff2inline import StandoffToInlineProcessor, \
    StandoffToInlineParameters


def test_model():
    model = StandoffToInlineProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == StandoffToInlineParameters


def test_standoff2inline():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/evalLLM1.json")

    with source.open("r") as fin:
        jdoc = json.load(fin)
    docs = [Document(**jdoc)]
    processor = StandoffToInlineProcessor()
    parameters = StandoffToInlineParameters()
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert '<p>' in doc0.text
    assert '<non_inf_disease>' in doc0.text

    docs = [Document(**jdoc)]
    parameters.as_altText = "Inlined"
    parameters.s_open = " "
    parameters.s_close = " "
    parameters.a_open = '<{{a.labelName}} id="{{d.identifier}}-{{a.start}}:{{a.end}}">'
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.altTexts) == 1

    docs = [Document(**jdoc)]
    parameters.as_altText = "Inlined"
    parameters.d_open = '<segments>{{"\n\n"}}'
    parameters.d_close = '{{"\n\n"}}</segments>{{"\n\n"}}'
    parameters.s_open = '<segment "id"="{{s.start}}:{{s.end}}">{{"\n\n"}}'
    parameters.s_close = '{{"\n\n"}}</segment">{{"\n\n"}}'
    parameters.a_open = ''
    parameters.a_close = ''
    docs = processor.process(docs, parameters)
    doc0 = docs[0]
    assert len(doc0.altTexts) == 1
