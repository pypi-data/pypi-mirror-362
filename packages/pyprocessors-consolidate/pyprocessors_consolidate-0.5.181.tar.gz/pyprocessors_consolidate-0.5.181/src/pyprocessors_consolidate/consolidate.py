import re
from enum import Enum
from typing import Type, cast, Iterable, List, Optional
from collections_extended import RangeMap
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation
import icu


class ConsolidationType(str, Enum):
    default = "default"
    linker = "linker"
    unknown = "unknown"
    unknown_only = "unknown_only"


class ConsolidateParameters(ProcessorParameters):
    type: ConsolidationType = Field(
        ConsolidationType.default,
        description="""Type of consolidation, use<br />
    <li>**default** deduplicate and if overlap keeps only the longest match<br />
    <li>**linker** to retain only known entities<br />
    <li>**unknown** to retain all but prepending the `unknown_prefix` to the label of unknown entities<br />
    <li>**unknown_only** to retain only unknown entities prepending `unknown_prefix` to their label br />""",
    )
    kill_label: Optional[str] = Field(None, description="Label name of the kill list", extra="label")
    unknown_prefix: Optional[str] = Field(
        "Unknown ", description="String to prepend to the label of 'unknown' entities", extra="advanced"
    )


class ConsolidateProcessor(ProcessorBase):
    """Consolidate processor ."""

    def process(
        self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        def has_knowledge(a: Annotation):
            return a.terms is not None or a.properties is not None

        params: ConsolidateParameters = cast(ConsolidateParameters, parameters)
        for document in documents:
            if document.annotations:
                anns = self.filter_annotations(document, params.kill_label)
                if params.type in [
                    ConsolidationType.unknown_only,
                    ConsolidationType.unknown,
                ]:
                    for a in anns:
                        unknown_labelName = sanitize_label(
                            params.unknown_prefix + (a.label or a.labelName)
                        )
                        if not has_knowledge(a):
                            a.labelName = unknown_labelName
                            if a.label:
                                a.label = params.unknown_prefix + a.label
                    if params.type == ConsolidationType.unknown_only:
                        anns = [a for a in anns if not has_knowledge(a)]
                elif params.type == ConsolidationType.linker:
                    anns = [a for a in anns if has_knowledge(a)]
                document.annotations = anns
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ConsolidateParameters

    def filter_annotations(self, input: Document, kill_label: str = None):
        """Filter a sequence of annotations and remove duplicates or overlaps. When spans overlap, the (first)
        longest span is preferred over shorter spans.
        annotations (iterable): The annotations to filter.
        RETURNS (list): The filtered annotations.
        """

        def get_sort_key(a: Annotation):
            return a.end - a.start, -a.start, a.labelName == kill_label

        sorted_annotations: Iterable[Annotation] = sorted(
            input.annotations, key=get_sort_key, reverse=True
        )
        result = []
        seen_offsets = RangeMap()
        for ann in sorted_annotations:
            # Check for end - 1 here because boundaries are inclusive
            if (
                seen_offsets.get(ann.start) is None
                and seen_offsets.get(ann.end - 1) is None
            ):
                if ann.text is None:
                    ann.text = input.text[ann.start : ann.end]
                result.append(ann)
                seen_offsets[ann.start : ann.end] = ann
            else:
                target = seen_offsets.get(ann.start) or seen_offsets.get(ann.end - 1)
                # if target.labelName in kb_labels and ann.labelName in white_labels and (target.start-ann.start != 0 or target.end-ann.end != 0):
                if target.labelName != kill_label:
                    if (
                        target.start - ann.start == 0 or target.end - ann.end == 0
                    ) and (ann.end - ann.start) / (target.end - target.start) > 0.8:
                        if ann.terms:
                            terms = set(target.terms or [])
                            terms.update(ann.terms)
                            target.terms = list(terms)
                        if ann.properties:
                            props = target.properties or {}
                            props.update(ann.properties)
                            target.properties = props
        if kill_label is not None:
            result = [ann for ann in result if ann.labelName != kill_label]
        result = sorted(
            result,
            key=lambda ann: ann.start,
        )
        return result


nonAlphanum = re.compile(r"[\W]+", flags=re.ASCII)
underscores = re.compile("_{2,}", flags=re.ASCII)
trailingAndLeadingUnderscores = re.compile(r"^_+|_+\$", flags=re.ASCII)
# see http://userguide.icu-project.org/transforms/general
transliterator = icu.Transliterator.createInstance(
    "Any-Latin; NFD; [:Nonspacing Mark:] Remove; NFC; Latin-ASCII; Lower;",
    icu.UTransDirection.FORWARD,
)


def sanitize_label(string):
    result = transliterator.transliterate(string)
    result = re.sub(nonAlphanum, "_", result)
    result = re.sub(underscores, "_", result)
    result = re.sub(trailingAndLeadingUnderscores, "", result)
    return result
