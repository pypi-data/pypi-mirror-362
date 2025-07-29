from collections import defaultdict
from pathlib import Path
from typing import Type, Dict, Any, Generator, Optional, Union, List

import pandas as pd
import structlog
from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import (
    KnowledgeParserBase,
    Term,
    KnowledgeParserOptions,
    maybe_archive,
)

from pyimporters_csv.text import TXTOptions

logger = structlog.get_logger("pyimporters-excel")


@dataclass
class ExcelOptions(TXTOptions):
    """
    Options for the Excel knowledge import
    """

    multivalue_separator: str = Query(
        "|", description="Additional separator to split multivalued columns if any"
    )
    header: Optional[int] = Query(
        0,
        description="""Row number (0-indexed) to use as the column names,
                                  leave blank if there is no header""",
    )
    identifier_col: str = Query(
        "identifier",
        description="""Column to use as the identifier of the concept,
                                either given as string name or column index""",
    )
    preferredForm_col: str = Query(
        "preferredForm",
        description="""Column to use as the preferred form of the term,
                                   either given as string name or column index""",
    )
    altForms_cols: str = Query(
        "altForms",
        description="""Column(s) to use as the alternative forms of the term,
                               either given as a (list of) string name(s) or column index(es)""",
    )


ExcelOptionsModel = ExcelOptions.__pydantic_model__


class ExcelKnowledgeParser(KnowledgeParserBase):
    def parse(
        self, source: Path, options: Union[BaseModel, Dict[str, Any]], bar: Bar
    ) -> Generator[Term, None, None]:
        options = ExcelOptionsModel(**options) if isinstance(options, dict) else options
        with maybe_archive(source, mode="rb") as file:
            lines = pd.read_excel(file, header=options.header)
            identifier_col = get_col_index(lines, options.identifier_col, 0)
            prefLabel_col = get_col_index(
                lines, options.preferredForm_col, identifier_col
            )
            altLabel_cols = get_col_index(lines, options.altForms_cols, None)
            all_cols = (
                [
                    col
                    for col in lines.columns
                    if col not in [prefLabel_col, identifier_col]
                ]
                if altLabel_cols
                else None
            )
            skipped_empty_lines = (
                lines.dropna(subset=[identifier_col]).fillna(value="").astype(str)
            )
            bar.max = len(skipped_empty_lines)
            bar.start()
            for index, row in skipped_empty_lines.iterrows():
                bar.next()
                prefLabel = row[prefLabel_col].strip()
                identifier = row[identifier_col].strip()
                concept: Term = Term(identifier=identifier, preferredForm=prefLabel)
                if altLabel_cols:
                    concept.properties = defaultdict(list)
                    alts_cols = [col_index(x.strip()) for x in altLabel_cols.split(",")]
                    restrict = any(col.startswith("-") for col in alts_cols)
                    if restrict:
                        list_cols = [
                            col for col in all_cols if f"-{col}" not in alts_cols
                        ]
                        alts_cols = list_cols
                    for alt_col in alts_cols:
                        altLabel = row[alt_col].strip()
                        if altLabel:
                            if options.multivalue_separator:
                                altLabels = [
                                    x.strip()
                                    for x in altLabel.split(
                                        options.multivalue_separator
                                    )
                                ]
                                concept.properties["altForms"].extend(altLabels)
                            else:
                                concept.properties["altForms"].append(altLabel)
                yield concept

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return ExcelOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ExcelOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["xls", "xlsx"]


def col_index(col):
    return int(col) if col.lstrip("+-").isdigit() else col


def get_col_index(df, col, default=None):
    colid = default
    if col is not None:
        col = col.strip()
        if col and col in df.columns:
            colid = col_index(col)
        else:
            logger.warning(f"Unknown column {col}, ignoring")
    return colid
