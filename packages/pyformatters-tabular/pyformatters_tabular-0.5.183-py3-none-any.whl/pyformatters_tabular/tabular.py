import io
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Type

import pandas as pd
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.v1.schema import Document
from starlette.responses import Response


class OutputFormat(str, Enum):
    xlsx = 'xlsx'
    csv = 'csv'


class TabularParameters(FormatterParameters):
    format: OutputFormat = Field(OutputFormat.xlsx, description="Output format")
    as_slots: bool = Field(False, description="""If true, the result is one row, each column contains one label type.
    If several annotations share the same label they are separated by a semi-colon""")
    multivalue_separator: str = Field(";",
                                      description="Additional separator to split multivalued columns if any")
    document_fields: str = Field("identifier,title",
                                 description="Comma separated document properties to add as additional columns")


class TabularFormatter(FormatterBase):
    """Tabular formatter.
    """

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Response.
        """
        parameters: TabularParameters = parameters
        try:
            df = doc_to_slots(document, parameters) if parameters.as_slots else doc_to_records(document, parameters)
            document_fields = comma_separated_to_list(parameters.document_fields)
            if document_fields:
                if 'title' in parameters.document_fields:
                    df.insert(0, 'document.title', document.title)
                if 'identifier' in parameters.document_fields:
                    df.insert(0, 'document.identifier', document.identifier)
            resp: Response = None
            filename = f"file.{parameters.format.value}"
            if document.properties and "fileName" in document.properties:
                filepath = Path(document.properties['fileName'])
                filename = f"{filepath.stem}.{parameters.format.value}"
            if parameters.format == OutputFormat.xlsx:
                bio = io.BytesIO()
                df.to_excel(bio, index=False)
                resp = Response(content=bio.getvalue(),
                                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            elif parameters.format == OutputFormat.csv:
                sio = io.StringIO()
                df.to_csv(sio, index=False)
                resp = Response(content=sio.getvalue(),
                                media_type="text/csv")
                resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return resp
        except BaseException as err:
            raise err

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return TabularParameters


def doc_to_slots(document: Document, parameters: TabularParameters) -> pd.DataFrame:
    slots = defaultdict(list)
    if document.annotations:
        for a in document.annotations:
            slots[a.label].append(document.text[a.start:a.end])
    for label, texts in slots.items():
        slots[label] = [parameters.multivalue_separator.join(texts)]
    df = pd.DataFrame.from_dict(slots).sort_index(axis=1)
    return df


def doc_to_records(document: Document, parameters: TabularParameters) -> pd.DataFrame:
    records = []
    if document.annotations:
        for a in document.annotations:
            record = a if isinstance(a, dict) else a.dict()
            record['text'] = document.text[record['start']:record['end']]
            props = record.pop('properties', None)
            if props:
                for prop, val in props.items():
                    record[f"properties.{prop}"] = str(val)
            terms = record.pop('terms', None)
            if terms:
                for i, term in enumerate(terms):
                    for key, val in term.items():
                        record[f"terms.{i}.{key}"] = str(val)
            records.append(record)
    # if document.categories:
    #     for c in document.categories:
    #         record = c if isinstance(c, dict) else c.dict()
    #         props = record.pop('properties', None)
    #         if props:
    #             for prop, val in props.items():
    #                 record[f"properties.{prop}"] = str(val)
    #         records.append(record)
    df: pd.DataFrame = pd.DataFrame.from_records(records)
    return df
