import logging
from collections import defaultdict
from itertools import groupby, chain
from typing import Type, cast, List

from collections_extended import RangeMap, MappedRange
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, AltText

logger = Logger("pymultirole")


class DocumentFingerprintParameters(ProcessorParameters):
    as_altText: str = Field(
        "fingerprint",
        description="""If defined generate the fingerprint as an alternative text of the input document.""",
    )


class DocumentFingerprintProcessor(ProcessorBase):
    """DocumentFingerprint processor ."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: DocumentFingerprintParameters = cast(
            DocumentFingerprintParameters, parameters
        )
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.annotations:
                    ann_groups = group_annotations(document, by_lexicon)
                    # 1. Compute document fingerprint
                    fingerprints = compute_fingerprint(ann_groups)
                    if params.as_altText is not None and len(params.as_altText):
                        document.altTexts = document.altTexts or []
                        altTexts = [
                            alt
                            for alt in document.altTexts
                            if alt.name != params.as_altText
                        ]
                        altTexts.append(
                            AltText(name=params.as_altText, text=" ".join(fingerprints))
                        )
                        document.altTexts = altTexts
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DocumentFingerprintParameters


EUROVOC_NS = "http://eurovoc.europa.eu/"


def compute_fingerprint(ann_groups):
    def get_sort_key(r: MappedRange):
        return -r.start, r.stop - r.start

    fingerprints = []
    sorted_ann = sorted(
        chain(ann_groups["wikidata"].ranges(), ann_groups["eurovoc"].ranges()),
        key=get_sort_key,
        reverse=True,
    )
    for r in sorted_ann:
        ann = r.value
        if ann.terms and len(ann.terms):
            if ann.terms[0].lexicon == "wikidata":
                fingerprints.append(ann.terms[0].identifier)
                fingerprint = ann.terms[0].properties.get("fingerprint", None)
                if fingerprint:
                    props_vals = [
                        (p, v)
                        for p, v in [
                            pv.split(":", maxsplit=1) for pv in fingerprint.split(",")
                        ]
                    ]
                    ann.terms[0].properties["fingerprint"] = props_vals
                    try:
                        fingerprints.extend(
                            [v for p, v in props_vals if v.startswith("Q")]
                        )
                    except BaseException:
                        logging.exception()
            elif ann.terms[0].lexicon == "eurovoc" and ann.terms[
                0
            ].identifier.startswith(EUROVOC_NS):
                fingerprints.append("E" + ann.terms[0].identifier[len(EUROVOC_NS):])
    return fingerprints


def group_annotations(doc: Document, keyfunc):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    groups = defaultdict(RangeMap)
    for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
        sorted_group = sorted(g, key=get_sort_key, reverse=True)
        groups[k] = RangeMap((a.start, a.end, a) for a in sorted_group)
    return groups


def has_knowledge(a: Annotation):
    return a.terms is not None


def by_lexicon(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon
        return lex
    else:
        return ""


def by_label(a: Annotation):
    return a.labelName
