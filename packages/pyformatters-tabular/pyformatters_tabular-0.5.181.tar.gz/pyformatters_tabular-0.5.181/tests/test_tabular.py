import io
import json
import pandas as pd
from pathlib import Path

from pymultirole_plugins.v1.schema import Document
from starlette.responses import Response

from pyformatters_tabular.tabular import TabularFormatter, TabularParameters, OutputFormat


def test_xlsx():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/response_1621334812115.json')
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = TabularFormatter()
        options = TabularParameters(format=OutputFormat.xlsx)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        result = Path(testdir, 'data/response_1621334812115.xlsx')
        with result.open("wb") as fout:
            fout.write(resp.body)


def test_csv():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/response_1621334812115.json')
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = TabularFormatter()
        options = TabularParameters(format=OutputFormat.csv)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type == "text/csv"
        result = Path(testdir, 'data/response_1621334812115.csv')
        with result.open("wb") as fout:
            fout.write(resp.body)


def test_slots():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/slots.json')
    output_file = Path(testdir, 'data/slots.xlsx')
    formatter = TabularFormatter()
    options = TabularParameters(format=OutputFormat.csv, as_slots=True)
    with source.open("r") as fin:
        docs = json.load(fin)
        dfs = []
        for doc in docs:
            doc = Document(**doc)
            resp: Response = formatter.format(doc, options)
            assert resp.status_code == 200
            content = io.TextIOWrapper(io.BytesIO(resp.body), encoding=resp.charset)
            df = pd.read_csv(content)
            dfs.append(df)
        concatenated = pd.concat(dfs, ignore_index=True)
        concatenated.to_excel(str(output_file), index=False)
