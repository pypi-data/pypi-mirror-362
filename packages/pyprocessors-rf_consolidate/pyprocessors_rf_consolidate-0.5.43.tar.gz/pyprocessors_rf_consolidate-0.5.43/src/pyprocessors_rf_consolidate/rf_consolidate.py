import copy
from collections import defaultdict
from itertools import groupby
from typing import Type, List, Dict

from collections_extended import RangeMap
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation

logger = Logger("pymultirole")


class RFConsolidateParameters(ProcessorParameters):
    pass


class RFConsolidateProcessor(ProcessorBase):
    """RFConsolidate processor ."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        # params: RFConsolidateParameters = cast(RFConsolidateParameters, parameters)
        acro_labels = ["Acronym", "Expanded"]
        for document in documents:
            with add_logging_context(docid=document.identifier):
                if document.annotations:
                    ann_groups = group_annotations(document, by_label)
                    other_labels = [
                        label for label in ann_groups.keys() if label not in acro_labels
                    ]
                    # Consolidate & links against thesaurus
                    conso_anns = consolidate_and_link(ann_groups, other_labels)
                    document.annotations = conso_anns
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return RFConsolidateParameters


def consolidate_and_link(ann_groups, other_labels):
    conso_anns = []
    for label in other_labels:
        for other_r in ann_groups[label].ranges():
            conso_anns.append(other_r.value)

    exp2kb = {}

    for exp_r in ann_groups["Expanded"].ranges():
        exp_ann = exp_r.value
        kb_r = annotation_in_group(exp_ann, ann_groups, other_labels)
        perfect, kb_match = one_match(exp_ann, kb_r)
        if kb_match:
            if perfect:
                if exp_ann.terms and kb_match.terms:
                    expid = exp_ann.terms[0].identifier
                    exp2kb[expid] = kb_match
            else:
                logger.warning("Found larger annotation in KB")
                logger.warning(f"=> {exp_ann}")
                logger.warning("and")
                logger.warning(f" -{kb_match}")
        elif kb_r and len(kb_r) > 1:
            logger.warning("Found overlapping annotations in KB")
            logger.warning(f"=> {exp_ann}")
            logger.warning("and")
            for r in kb_r.values():
                logger.warning(f" -{r}")
        else:  # it is a new expanded form, keep it
            conso_anns.append(exp_ann)

    for acro_r in ann_groups["Acronym"].ranges():
        acro_ann = acro_r.value
        acroid = acro_ann.terms[0].identifier if acro_ann.terms else None
        kb_r = annotation_in_group(acro_ann, ann_groups, other_labels)
        perfect, kb_match = one_match(acro_ann, kb_r)
        if kb_match:
            if perfect:
                if acroid and kb_match.terms:
                    if acroid in exp2kb:  # disambiguate
                        kb_match.terms = exp2kb[acroid].terms
            else:
                logger.warning("Found larger annotation in KB")
                logger.warning(f"=> {acro_ann}")
                logger.warning("and")
                logger.warning(f" -{kb_match}")
        elif kb_r and len(kb_r) > 1:
            logger.warning("Found overlapping annotations in KB")
            logger.warning(f"=> {acro_ann}")
            logger.warning("and")
            for r in kb_r.values():
                logger.warning(f" -{r}")
        else:
            if acroid in exp2kb:  # propagate term
                new_term = copy.deepcopy(exp2kb[acroid])
                new_term.start = acro_ann.start
                new_term.end = acro_ann.end
                new_term.text = acro_ann.text
                conso_anns.append(new_term)
            else:  # it is a new acronym, keep it
                conso_anns.append(acro_ann)

    return conso_anns


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
        lex = a.terms[0].lexicon.split("_")
        return lex[0]
    else:
        return ""


def by_label(a: Annotation):
    return a.label or a.labelName


def one_match(a: Annotation, matches: RangeMap):
    match = None
    perfect = False
    if matches and len(matches) == 1:
        match = matches.get(a.start) or matches.get(a.end)
        if match:
            perfect = a.start == match.start and a.end == match.end
    return perfect, match


# noqa: W503
def annotation_in_group(
        a: Annotation, ann_groups: Dict[str, RangeMap], gnames: List[str]
):
    for gname in gnames:
        if (
                gname in ann_groups
                and a.start in ann_groups[gname]
                or a.end in ann_groups[gname]
        ):
            return ann_groups[gname][a.start: a.end]
    return None
