import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict, IsNow, IsDatetime
from pymultirole_plugins.v1.schema import Document

from pyannotators_duckling.duckling import DucklingAnnotator, DucklingParameters, DEFAULT_DIM_LABEL


def test_duckling():
    model = DucklingAnnotator.get_model()
    model_class = model.construct().__class__
    assert model_class == DucklingParameters
    annotator = DucklingAnnotator()
    parameters = DucklingParameters()
    docs: List[Document] = annotator.annotate([Document(
        text="Aujourd'hui nous sommes quelle date? Le 1er Juillet 2021, OK alors tu me dois 15 euros et 50 cts!",
        metadata={'language': 'fr'})], parameters)
    doc0 = docs[0]
    assert doc0.annotations == HasLen(3)
    assert doc0.annotations == IsList(
        HasAttributes(label=DEFAULT_DIM_LABEL, properties=IsPartialDict(dim='time', grain='day',
                                                                        value=IsNow(delta=timedelta(days=1),
                                                                                    iso_string=True,
                                                                                    enforce_tz=False))),
        HasAttributes(label=DEFAULT_DIM_LABEL, properties=IsPartialDict(dim='time', grain='day',
                                                                        value=IsDatetime(approx=datetime(2021, 7, 1),
                                                                                         iso_string=True,
                                                                                         enforce_tz=False))),
        HasAttributes(label=DEFAULT_DIM_LABEL, properties=IsPartialDict(dim='amount-of-money', unit='EUR', value=15.5))
    )

    parameters.mapping = {
        "datetime": "time",
        "money": "amount-of-money"
    }
    docs: List[Document] = annotator.annotate([Document(
        text="Aujourd'hui nous sommes quelle date? Le 1er Juillet 2021, OK alors tu me dois 15 euros et 50 cts!",
        metadata={'language': 'fr'})], parameters)
    doc0 = docs[0]
    assert doc0.annotations == HasLen(3)
    assert doc0.annotations == IsList(
        HasAttributes(labelName="datetime", properties=IsPartialDict(dim='time', grain='day',
                                                                     value=IsNow(delta=timedelta(days=1),
                                                                                 iso_string=True,
                                                                                 enforce_tz=False))),
        HasAttributes(labelName="datetime", properties=IsPartialDict(dim='time', grain='day',
                                                                     value=IsDatetime(approx=datetime(2021, 7, 1),
                                                                                      iso_string=True,
                                                                                      enforce_tz=False))),
        HasAttributes(labelName="money", properties=IsPartialDict(dim='amount-of-money', unit='EUR', value=15.5))
    )


def test_duckling_file():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/sens_arret-document-JURITEXT000024487667.json")
    annotator = DucklingAnnotator()
    parameters = DucklingParameters()
    parameters.mapping = {
        "datetime": "time",
        "money": "amount-of-money"
    }
    with source.open("r") as fin:
        docs = json.load(fin)
        jdocs = [Document(**doc) for doc in docs]
        jdocs: List[Document] = annotator.annotate(jdocs, parameters)
        jdoc0 = jdocs[0]
        assert jdoc0.annotations == HasLen(75)
