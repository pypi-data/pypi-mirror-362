from pathlib import Path
from typing import Type, Dict, Any, Generator, Union, List
from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import (
    KnowledgeParserOptions,
    KnowledgeParserBase,
    Term,
    maybe_archive,
)


@dataclass
class TXTOptions(KnowledgeParserOptions):
    """
    Options for the TXT knowledge import
    """

    encoding: str = Query("utf-8", description="Encoding of the file")


TXTOptionsModel = TXTOptions.__pydantic_model__


class TXTKnowledgeParser(KnowledgeParserBase):
    def parse(
        self, source: Path, options: Union[BaseModel, Dict[str, Any]], bar: Bar
    ) -> Generator[Term, None, None]:
        options = TXTOptionsModel(**options) if isinstance(options, dict) else options
        with maybe_archive(source, encoding=options.encoding) as file:
            bar.max = file_len(file)
        bar.start()
        with maybe_archive(source, encoding=options.encoding) as fin:
            for line in fin:
                bar.next()
                term = line.strip()
                if term:
                    yield Term(identifier=term)

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return TXTOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return TXTOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["txt", "text", "zip"]


def file_len(file):
    return sum(1 for line in file)


def filepath_len(input_file: Path):
    with open(input_file) as f:
        nr_of_lines = file_len(f)
    return nr_of_lines
