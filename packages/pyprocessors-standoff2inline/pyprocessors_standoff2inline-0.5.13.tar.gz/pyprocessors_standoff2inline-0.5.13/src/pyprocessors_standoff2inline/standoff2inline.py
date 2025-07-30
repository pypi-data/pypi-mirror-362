import inspect
from collections import defaultdict
from functools import lru_cache
from itertools import groupby
from typing import Type, cast, List, Optional

import jinja2
from collections_extended import RangeMap
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, Span, AltText

from .standoff2inline_processor import Standoff2Inline

logger = Logger("pymultirole")


class StandoffToInlineParameters(ProcessorParameters):
    d_open: Optional[str] = Field(
        None,
        description="""Contains the document open tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    d_close: Optional[str] = Field(
        None,
        description="""Contains the document close tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    s_open: str = Field(
        "<p>",
        description="""Contains the segment open tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    s_close: str = Field(
        "</p>",
        description="""Contains the segment close tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    a_open: str = Field(
        "<{{a.labelName}}>",
        description="""Contains the annotation open tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    a_close: str = Field(
        "</{{a.labelName}}>",
        description="""Contains the annotation close tag as a (jinja2 template)[https://jinja.palletsprojects.com/en/3.1.x/] string"""
    )
    as_altText: str = Field(
        None,
        description="""<li>If defined: generates the completion as an alternative text of the input document,
    <li>if not: replace the text of the input document.""",
    )


class StandoffToInlineProcessor(ProcessorBase):
    """Create categories from annotations"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: StandoffToInlineParameters = cast(StandoffToInlineParameters, parameters)
        d_open , d_close, s_open, s_close, a_open, a_close = get_templates(params)
        try:
            for document in documents:
                with add_logging_context(docid=document.identifier):
                    inliner = Standoff2Inline(end_is_stop=True)
                    altTexts = document.altTexts or []
                    if not document.sentences:
                        document.sentences = [Span(start=0, end=len(document.text))]
                    inliner.add((0, render_template(d_open, d=document)),
                                (len(document.text), render_template(d_close, d=document)))
                    grouped = group_annotations_by_sentences(document)
                    for isent, sent in enumerate(document.sentences):
                        inliner.add((sent.start, render_template(s_open, d=document, s=sent)),
                                    (sent.end, render_template(s_close, d=document, s=sent)))
                        if a_open is not None or a_close is not None:
                            for a in grouped[isent]:
                                inliner.add((a.start, render_template(a_open, d=document, s=sent, a=a)),
                                            (a.end, render_template(a_close, d=document, s=sent, a=a)))
                    result = inliner.apply(document.text)
                    if params.as_altText is not None and len(
                            params.as_altText
                    ):
                        altTexts.append(
                            AltText(name=params.as_altText, text=result)
                        )
                    else:
                        document.text = result
                        document.sentences = []
                        document.annotations = []
                        document.categories = []
                    document.altTexts = altTexts
        except BaseException as err:
            logger.warning("An exception was thrown!", exc_info=True)
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return StandoffToInlineParameters


def get_templates(params: StandoffToInlineParameters):
    return get_template(params.d_open), get_template(params.d_close), get_template(
        params.s_open), get_template(params.s_close), get_template(params.a_open), get_template(
        params.a_close)


@lru_cache(maxsize=None)
def get_template(prompt: str, default: str = None):
    prompt_templ = default
    environment = get_jinja2_env()
    if prompt is not None and prompt.strip() != "":
        prompt_dedented = inspect.cleandoc(prompt)
        prompt_templ = environment.from_string(prompt_dedented)
    return prompt_templ


def render_template(prompt_templ, **kwargs):
    prompt = ""
    if prompt_templ is not None:
        prompt = prompt_templ.render(kwargs)
    return prompt


def left_longest_match(a):
    return a.end - a.start, -a.start


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

    if document.annotations:
        for k, g in groupby(document.annotations, by_sentenceid):
            sorted_group = sorted(g, key=get_sort_key, reverse=True)
            groups[k] = sorted_group

    return groups


@lru_cache(maxsize=None)
def get_jinja2_env():
    return jinja2.Environment(extensions=["jinja2.ext.do"])
