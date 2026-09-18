from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'
def app():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    return at

def test_each_injected_defect_fails_its_quality_gate():
    at=app()
    expected={'Duplicate booking ID':'unique','Missing customer reference':'relationships','Negative ACV':'non_negative'}
    for scenario,test in expected.items():
        at.selectbox[0].select(scenario).run()
        assert not at.exception
        checks=at.dataframe[1].value
        assert checks.loc[checks.test==test,'passed'].eq(False).all()
        assert checks.passed.sum()==3
    at.selectbox[0].select('Clean data').run()
    assert at.dataframe[1].value.passed.all()
