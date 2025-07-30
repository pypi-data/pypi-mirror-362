import logging
import re
from typing import Type, List, cast

from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, AltText

logger = logging.getLogger(__name__)


class CapitalizerParameters(ProcessorParameters):
    exceptions: str = Field("am,auf,op,bei,on,the,de,do,dei,la,del,della,di,sur",
                            description="Comma-separated list of words to ignore",
                            extra="advanced", )
    original_altText: str = Field(
        "_original_text",
        description="""Stores the original text as an alternative text of the input document""",
        extra="advanced"
    )


class CapitalizerProcessor(ProcessorBase):
    __doc__ = """Capitalizer processor."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: CapitalizerParameters = cast(CapitalizerParameters, parameters)
        exceptions = comma_separated_to_list(params.exceptions)

        word_regex = r"\S+"

        def word_repl(m):  # m is a match data object
            word = m.group()
            return word.capitalize() if word not in exceptions else word

        for document in documents:
            if document.annotations:
                text = document.text
                is_modified = False
                sorted_annotations = sorted([a for a in document.annotations if not a.labelName == 'sentence'],
                                            key=natural_order,
                                            reverse=True,
                                            )
                res = []
                i = 0
                for a in sorted_annotations:
                    is_modified = True
                    atext = a.text or text[a.start:a.end]
                    aresult = re.sub(word_regex, word_repl, atext, 0, re.MULTILINE)
                    res.append(text[i:a.start] + aresult)
                    i = a.end
                res.append(text[a.end:])
                if is_modified:
                    altTexts = document.altTexts or []
                    altTexts.append(AltText(name=params.original_altText, text=document.text))
                    document.altTexts = altTexts
                document.text = ''.join(res)
                document.annotations = None
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return CapitalizerParameters


def left_longest_match(a: Annotation):
    return a.end - a.start, -a.start


def natural_order(a: Annotation):
    return -a.start, a.end - a.start
