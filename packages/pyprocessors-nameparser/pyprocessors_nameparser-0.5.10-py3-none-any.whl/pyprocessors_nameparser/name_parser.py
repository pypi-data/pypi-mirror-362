from logging import Logger
from typing import List, Type, cast
from log_with_context import add_logging_context
from nameparser import HumanName
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document

logger = Logger("pymultirole")


class NameParserParameters(ProcessorParameters):
    name_labels: List[str] = Field(None, description="List of labels to analyze", extra="label")


class NameParserProcessor(ProcessorBase):
    __doc__ = """NameParser based on [Nameparser](https://github.com/derek73/python-nameparser)."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: NameParserParameters = cast(NameParserParameters, parameters)
        try:
            for document in documents:
                with add_logging_context(docid=document.identifier):
                    if document.annotations:
                        for a in document.annotations:
                            if a.labelName in params.name_labels:
                                atext = a.text or document.text[a.start:a.end]
                                name = HumanName(atext)
                                props = a.properties or {}
                                props.update(name.as_dict())
                                a.properties = props
        except BaseException as err:
            raise err
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return NameParserParameters
