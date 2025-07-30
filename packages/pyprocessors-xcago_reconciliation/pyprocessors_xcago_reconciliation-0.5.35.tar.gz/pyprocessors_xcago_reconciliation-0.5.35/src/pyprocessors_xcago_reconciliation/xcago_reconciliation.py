import copy
import logging
import string
from collections import defaultdict, OrderedDict
from enum import Enum
from itertools import groupby
from typing import Type, cast, List, Optional, Dict, Iterable

from collections_extended import RangeMap
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, AltText

logger = Logger("pymultirole")


class WrappedTerm(object):
    def __init__(self, term):
        self.term = term
        self.status = term.properties.get('status', "") if term.properties else ""

    def __eq__(self, other):
        return self.term.identifier == other.term.identifier and self.status == other.status

    def __hash__(self):
        return hash((self.term.identifier, self.status))


class XCagoReconciliationType(str, Enum):
    linker = "linker"


class XCagoReconciliationParameters(ProcessorParameters):
    type: XCagoReconciliationType = Field(
        XCagoReconciliationType.linker,
        description="""Type of consolidation, use<br />
    <li>**linker** to retain only known entities (extracted by a model)<br />""", extra="internal,advanced"
    )
    kill_label: Optional[str] = Field(None, description="Label name of the kill list", extra="label,advanced")
    wikidata_kill_label: Optional[str] = Field(None, description="Label name of the wikidata kill list", extra="label,advanced")
    white_label: Optional[str] = Field(
        None, description="Label name of the white list", extra="label,advanced"
    )
    whitelisted_lexicons: List[str] = Field(
        None,
        description="Lexicons to be considered as taking precedence over models",
        extra="lexicon,internal,advanced"
    )
    person_label: Optional[str] = Field(
        None, description="Label name of the person to apply the lastname resolution", extra="label,advanced"
    )
    wikidata_partial: bool = Field(
        True,
        description="Allow to link wikidata concepts wider than model annotations, for example `President Donald Trump` linked to `Donald Trump`",
        extra="advanced"
    )
    remove_suspicious: bool = Field(
        True,
        description="Remove suspicious annotations extracted by the model (numbers, percentages, phrases without uppercase words)",
        extra="advanced,internal"
    )
    resolve_lastnames: bool = Field(
        False,
        description="Try to resolve isolated family names and firstnames if they have been seen before in the document",
        extra="advanced"
    )
    as_altText: str = Field(
        "fingerprint",
        description="""If defined generate the fingerprint as an alternative text of the input document.""",
        extra="advanced"
    )
    original_altText: str = Field(
        "_original_text",
        description="""Restore the original text of the input document""",
        extra="advanced"
    )


class XCagoReconciliationProcessor(ProcessorBase):
    """XCagoReconciliation processor ."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: XCagoReconciliationParameters = cast(XCagoReconciliationParameters, parameters)
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.annotations:
                    annotations = [a for a in document.annotations if a.labelName != 'sentence']
                    annotations = mark_whitelisted(annotations, params)
                    # 1. Compute document fingerprint
                    fingerprints, annotations = compute_fingerprint(annotations)
                    altTexts = document.altTexts or []
                    original_altText = next((alt for alt in altTexts if alt.name == params.original_altText), None)
                    if original_altText is not None:
                        document.text = original_altText.text
                    altTexts = [
                        alt
                        for alt in altTexts
                        if alt.name not in [params.as_altText, params.original_altText]
                    ]
                    if params.as_altText is not None and len(params.as_altText):
                        altTexts.append(
                            AltText(name=params.as_altText, text=" ".join(fingerprints))
                        )
                    document.altTexts = altTexts
                    ann_groups = group_annotations(annotations, keyfunc=by_lexicon)
                    # 2. Consolidate & links against KB and Wikidata
                    if params.type == XCagoReconciliationType.linker:
                        conso_anns = consolidate_linker(document.text,
                                                        ann_groups,
                                                        params
                                                        )
                    document.annotations = conso_anns
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return XCagoReconciliationParameters


EUROVOC_NS = "http://eurovoc.europa.eu/"


def compute_fingerprint(annotations):
    def get_sort_key(r: Annotation):
        return -r.start, r.end - r.start

    fingerprints = []
    anns = []
    sorted_ann = sorted(
        annotations,
        key=get_sort_key,
        reverse=True,
    )
    for ann in sorted_ann:
        keep_ann = True
        if by_lexicon(ann) in ["wikidata", "eurovoc"]:
            if ann.terms and len(ann.terms):
                if by_lexicon(ann) == "wikidata":
                    if ann.labelName == 'wikidata':
                        keep_ann = False
                    fingerprints.append(ann.terms[0].identifier)
                    fingerprint = ann.terms[0].properties.get("fingerprint", None)
                    if fingerprint and isinstance(fingerprint, str):
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
                elif by_lexicon(ann) == "eurovoc" and ann.terms[
                    0
                ].identifier.startswith(EUROVOC_NS):
                    keep_ann = False
                    fingerprints.append("E" + ann.terms[0].identifier[len(EUROVOC_NS):])
        if keep_ann:
            anns.append(ann)
    return fingerprints, anns


def mark_whitelisted(annotations, params: XCagoReconciliationParameters):
    new_annotations = []
    white_label = params.white_label
    white_lexicons = params.whitelisted_lexicons or []
    for a in annotations:
        new_annotations.append(a)
        if has_knowledge(a):
            if (
                    a.labelName == white_label
            ):  # Consider whitelisted terms as entities coming from the model
                a.terms = None
            elif a.terms[0].lexicon in white_lexicons:
                new_a = copy.deepcopy(a)
                new_a.terms = None
                new_annotations.append(new_a)
    return new_annotations


def compute_geo_labels(kb_match):
    return "location", "Location"


RESERVED_NAMES = [
    'Donald Trump',
    'Joe Biden',
    'Emmanuel Macron',
]


def consolidate_linker(
        text,
        ann_groups,
        params: XCagoReconciliationParameters
):
    conso_anns = []
    partial_anns = {}
    kill_names = defaultdict(set)
    kb_names = defaultdict(set)
    wiki_names = defaultdict(set)
    white_names = defaultdict(set)
    for k, v in ann_groups.items():
        if k not in ["", "eurovoc"]:
            for a in v.values():
                if a.labelName == params.kill_label or a.labelName == params.wikidata_kill_label:
                    kill_names[k].add(a.labelName)
                elif a.labelName == params.white_label:
                    white_names[k].add(a.labelName)
                else:
                    if k == "wikidata":
                        wiki_names[k].add(a.labelName)
                    else:
                        kb_names[k].add(a.labelName)

    if kill_names and params.wikidata_kill_label is not None:
        for wiki_r in ann_groups["wikidata"].ranges():
            wiki_ann = wiki_r.value
            if kill_names:
                kill_r = annotation_in_group(wiki_ann, ann_groups, params, kill_names)
                perfect, kill_match = one_match(wiki_ann, kill_r)
                if perfect and kill_match:
                    wiki_qids = {t.identifier for t in wiki_ann.terms}
                    kill_qids = {t.identifier for t in wiki_ann.terms}
                    if wiki_qids & kill_qids:
                        logger.warning("Kill wikidata annotation")
                        logger.warning(f"=> {wiki_ann}")
                        ann_groups["wikidata"].delete(start=wiki_ann.start, stop=wiki_ann.end)
        kill_names.pop(params.wikidata_kill_label, None)

    for model_r in ann_groups[""].ranges():
        model_ann = model_r.value

        if params.remove_suspicious and is_suspicious(model_ann):
            logger.warning("Kill suspicious annotation")
            logger.warning(f"=> {model_ann}")
            continue
        if kill_names:
            kill_r = annotation_in_group(model_ann, ann_groups, params, kill_names)
            perfect, kill_match = one_match(model_ann, kill_r)
            if perfect and kill_match:
                logger.warning("Kill annotation")
                logger.warning(f"=> {model_ann}")
                continue

        kb_r = annotation_in_group(model_ann, ann_groups, params, kb_names)
        perfect, kb_match = one_match(model_ann, kb_r)
        if kb_match:
            if perfect:
                if labels_are_compatible(model_ann.labelName, kb_match.labelName, params):
                    model_ann.labelName = kb_match.labelName
                    model_ann.label = kb_match.label
                    model_ann.terms = model_ann.terms or []
                    model_ann.terms.extend(kb_match.terms)
                else:
                    logger.warning("Found wrong label annotation in KB")
                    logger.warning(f"=> {model_ann}")
                    logger.warning("and")
                    logger.warning(f" -{kb_match}")
            else:
                logger.warning("Found larger annotation in KB")
                logger.warning(f"=> {model_ann}")
                logger.warning("and")
                logger.warning(f" -{kb_match}")
        elif kb_r and len(kb_r) > 1:
            logger.warning("Found overlapping annotations in KB")
            logger.warning(f"=> {model_ann}")
            logger.warning("and")
            for r in kb_r.values():
                logger.warning(f" -{r}")

        wiki_r = annotation_in_group(model_ann, ann_groups, params, wiki_names)
        sub_geo = 0
        for wiki_match in all_matches(model_ann, wiki_r):
            if almost_perfect_match(model_ann, wiki_match) or (params.wikidata_partial and wider_match(model_ann, wiki_match)):
                if labels_are_compatible(model_ann.labelName, wiki_match.labelName, params):
                    if model_ann.labelName == params.white_label:
                        model_ann.labelName = wiki_match.labelName
                        model_ann.label = wiki_match.label
                    model_ann.terms = model_ann.terms or []
                    wiki_match.terms[0].properties.pop("fingerprint", None)
                    model_ann.terms.extend(wiki_match.terms)
                    if perfect_match(model_ann, wiki_match) and is_geo_label(wiki_match.labelName):
                        sub_geo += 1

            elif sub_geo == 0:
                allow_subgeo = True
                # Allow 1 sub entities géo
                if is_subgeo_label(
                        wiki_match.labelName, params) and narrower_match(model_ann, wiki_match):
                    if kill_names:
                        kill_r = annotation_in_group(wiki_match, ann_groups, params, kill_names)
                        perfect, kill_match = one_match(wiki_match, kill_r)
                        if kill_match and wiki_match.start >= kill_match.start and wiki_match.end <= kill_match.end:
                            logger.warning("Kill annotation")
                            logger.warning(f"=> {wiki_match}")
                            allow_subgeo = False
                    if allow_subgeo:
                        sub_geo += 1
                        geo_label_name, geo_label = compute_geo_labels(wiki_match)
                        wiki_match.labelName = geo_label_name
                        wiki_match.label = geo_label
                        partial_anns[(wiki_match.start, wiki_match.end)] = wiki_match

        conso_anns.append(model_ann)
    sorted_annotations = sorted(conso_anns,
                                key=natural_order,
                                reverse=True,
                                )
    seen_names = defaultdict(set)
    for ann in sorted_annotations:
        if ann.text != text[ann.start:ann.end]:
            ann.text = text[ann.start:ann.end]
        if params.resolve_lastnames and ann.labelName == 'person':
            lastnames = person_varnames(ann, text)
            if lastnames is not None:
                for composed_name in lastnames:
                    if len(lastnames) > 1:
                        if has_knowledge(ann):
                            for t in ann.terms:
                                seen_names[composed_name].add(WrappedTerm(t))
                        else:
                            if lastnames[0] not in RESERVED_NAMES:
                                seen_names[composed_name].add(None)
                    else:
                        if composed_name in seen_names:
                            ann.terms = [wt.term for wt in seen_names[composed_name] if wt is not None]
                            break
        if is_geo_label(ann.labelName) and (ann.start, ann.end) in partial_anns:
            partial_anns.pop((ann.start, ann.end))
    sorted_annotations.extend(partial_anns.values())
    return sorted_annotations


def group_annotations(annotations, keyfunc):
    groups = defaultdict(RangeMap)
    sorted_annotations = sorted(annotations, key=keyfunc)
    for k, g in groupby(sorted_annotations, keyfunc):
        sorted_group = sorted(g, key=left_longest_match, reverse=True)
        for a in sorted_group:
            addit = True
            if a.start in groups[k] and a.end - 1 in groups[k]:
                b = groups[k][a.start]
                if a.start - b.start == 0 and a.end - b.end == 0:
                    terms = set(WrappedTerm(t) for t in b.terms) if b.terms else set()
                    if a.terms:
                        terms.update(set(WrappedTerm(t) for t in a.terms))
                    b.terms = [t.term for t in terms]
                    addit = False
            if addit:
                groups[k][a.start:a.end] = a
    return groups


def left_longest_match(a: Annotation):
    return a.end - a.start, -a.start, ord(a.labelName[0]), -a.score or -1.0


def natural_order(a: Annotation):
    return -a.start, a.end - a.start


def has_knowledge(a: Annotation):
    return a.terms is not None and a.terms


def is_whitelist(a: Annotation):
    if has_knowledge(a):
        for term in a.terms:
            props = term.properties or {}
            status = props.get("status", "")
            if "w" in status.lower():
                return True
    return False


def person_varnames(a: Annotation, text):
    if 'person' in a.labelName:
        atext = a.text or text[a.start:a.end]
        words = atext.split()
        if words is not None:
            variant_names = OrderedDict.fromkeys([' '.join(words[i:]) for i in range(len(words))])
            if len(words) > 1:
                variant_names2 = OrderedDict.fromkeys([' '.join(words[0:i - 1]) for i in range(2, len(words) + 1)])
                variant_names.update(variant_names2)
            return list(variant_names.keys())
    return None


def by_lexicon(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon
        return lex
    else:
        return ""


def by_lexicon_or_label(a: Annotation):
    if a.terms:
        lex = a.terms[0].lexicon
        return lex
    else:
        return a.labelName


def by_label(a: Annotation):
    return a.labelName


def perfect_match(a: Annotation, b: Annotation):
    return a.start == b.start and a.end == b.end


def almost_perfect_match(a: Annotation, b: Annotation):
    perfect = a.start == b.start and a.end == b.end
    if not perfect and a.text and b.text:
        if a.text in b.text or b.text in a.text:
            diff = set(a.text).symmetric_difference(b.text)
            perfect = all(c in string.punctuation for c in diff)
    return perfect


def wider_match(a: Annotation, b: Annotation):
    return (b.start < a.start or b.end > a.end)


def narrower_match(a: Annotation, b: Annotation):
    return b.start > a.start or b.end < a.end


def one_match(a: Annotation, matches: RangeMap):
    match = None
    perfect = False
    if matches and len(matches) >= 1:
        for match in matches.values():
            perfect = a.start == match.start and a.end == match.end
            if perfect:
                break
    return perfect, match


def all_matches(a: Annotation, matches: RangeMap):
    if matches and len(matches) >= 1:
        sorted_matches = sorted(matches.values(), key=left_longest_match, reverse=True)
        for match in sorted_matches:
            yield match


def is_suspicious(a: Annotation):
    suspicious = False
    # if a.text:
    #     words = a.text.split()
    #     has_upper = any([w[0].isupper() for w in words])
    #     suspicious = not has_upper
    return suspicious


# noqa: W503
# def annotation_in_group(
#         a: Annotation, ann_groups: Dict[str, RangeMap], gnames: List[str] = None
# ):
#     gname = by_lexicon_or_label(a)
#     if gname in gnames:
#         gnames = [gname]
#     for gname in gnames:
#         if (
#                 gname in ann_groups
#                 and a.start in ann_groups[gname]
#                 or a.end in ann_groups[gname]
#         ):
#             ga = ann_groups[gname][a.start: a.end]
#             return ga
#     return None

def is_kill_or_white_label(label: str, params: XCagoReconciliationParameters):
    return label == params.white_label or label == params.kill_label or label == params.wikidata_kill_label


def is_geo_label(label: str):
    return 'loc' in label


def is_subgeo_label(label: str, params: XCagoReconciliationParameters):
    return is_geo_label(label) and 'wikidata' in label


def is_org_label(label: str):
    return 'org' in label


def is_org_or_role_label(label: str):
    return is_org_label(label) or is_geo_label(label) or 'role' in label


def labels_are_compatible(a: str, b: str, params: XCagoReconciliationParameters):
    return a == b or (is_org_or_role_label(a) and is_geo_label(b)) or (is_org_label(a) and is_org_label(b)) or is_kill_or_white_label(a, params) or is_kill_or_white_label(b, params)


def annotation_in_group(
        a: Annotation, ann_groups: Dict[str, RangeMap], params: XCagoReconciliationParameters,
        gnames: Dict[str, Iterable[str]] = None
):
    for gkey, glabels in gnames.items():
        if any((labels_are_compatible(a.labelName, glabel, params) for glabel in glabels)):
            if (
                    gkey in ann_groups
                    and (a.start in ann_groups[gkey]
                         or a.end - 1 in ann_groups[gkey])
            ):
                ga = ann_groups[gkey][a.start: a.end]
                return ga
    return None
