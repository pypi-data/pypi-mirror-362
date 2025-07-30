import fpdf
import pandas as pd

import o7pdf.pandas_basic as basic


def test_general():
    report = fpdf.FPDF()
    df = pd.DataFrame()

    obj = basic.PandasBasic(df=df, pdf=report)

    obj.prepare()
    obj.generate()
