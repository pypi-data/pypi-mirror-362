import pandas as pd

import o7pdf.pandas_chart as pdc
from o7pdf.colors import PdfColors
from o7pdf.template import Template


def test_class_serie_param():
    try:
        pdc.SerieParam(type="invalid")
        assert False
    except ValueError as e:
        assert "Invalid type" in str(e)

    try:
        pdc.SerieParam(type=2.3)
        assert False
    except ValueError as e:
        assert "Invalid type" in str(e)


def test_prepare():
    report = Template(filename="cache/pandas_chart.pdf", title="Pandas Chart Demo")
    df_data = pd.DataFrame(
        {
            "date": [
                "2021-01-01",
                "2021-01-02",
                "2021-01-03",
                "2021-01-04",
                "2021-01-05",
                "2021-01-06",
                "2021-01-07",
            ],
            "critical": [1, 2, 3, 4, 5, 6, 7],
            "high": [2, 3, 4, 5, 6, 7, 8],
        }
    )
    series = [
        pdc.SerieParam(
            data="critical",
            is_stacked=True,
        ),
        pdc.SerieParam(
            data="high",
            is_stacked=True,
        ),
        pdc.SerieParam(
            data="critical",
            is_stacked=False,
            y_axis="right",
        ),
        pdc.SerieParam(
            data="high",
            is_stacked=False,
            y_axis="right",
        ),
    ]
    obj = pdc.PandasChart(
        df=df_data,
        series=series,
        width=100,
        height=100,
        pdf=report,
    )
    obj.prepare()

    assert obj.axis["left"].min == 3
    assert obj.axis["left"].max == 15

    assert obj.axis["right"].min == 1
    assert obj.axis["right"].max == 8


def test_pandas_chart():
    report = Template(filename="cache/pandas_chart.pdf", title="Pandas Chart Demo")
    report.add_page()

    df_data = pd.DataFrame(
        {
            "date": [
                "2021-01-01",
                "2021-01-02",
                "2021-01-03",
                "2021-01-04",
                "2021-01-05",
                "2021-01-06",
                "2021-01-07",
            ],
            "critical": [1, 2, 3, 4, 5, 6, 7],
            "high": [2, 3, 4, 5, 6, 7, 8],
            "min": [60.1, 62.3, 62.4, 63, 64.5, 66, 69],
            "max": [91, 91, 91.2, 91.5, 90.9, 91, 91],
            "mean": [85, 88, 88, 88, 89.3, 89, 89.9],
        }
    )
    df_data = df_data.set_index("date")

    now_value = pd.Series({"critical": 1, "high": 4})
    now_value.name = "Now"

    report.section_title("Vertical Bar Chart")

    series_stacked = [
        pdc.SerieParam(
            name="Critical",
            color=PdfColors.O900,
            data="critical",
            type="bar",
            y_axis="left",
            is_stacked=True,
        ),
        pdc.SerieParam(
            name="High",
            color=PdfColors.O700,
            data="high",
            type="bar",
            y_axis="left",
            is_stacked=True,
        ),
    ]

    x_pos = report.get_x()
    y_pos = report.get_y()
    width = (report.epw / 2) * 0.9

    pdc.PandasChart(
        df=df_data,
        series=series_stacked,
        width=width,
        height=70,
        pdf=report,
        font_size=6,
        title="Stacked Bar Chart",
    ).generate()

    series_side = [
        pdc.SerieParam(
            name="Critical",
            color=PdfColors.O300,
            data="critical",
            type="bar",
            y_axis="left",
            is_stacked=False,
        ),
        pdc.SerieParam(
            name="High",
            color=PdfColors.O100,
            data="high",
            type="bar",
            y_axis="left",
            is_stacked=False,
        ),
    ]

    report.set_xy(x_pos + (report.epw / 2), y_pos)

    pdc.PandasChart(
        df=df_data,
        series=series_side,
        width=80,
        height=70,
        pdf=report,
        font_size=6,
        title="Side by Side Bar Chart",
    ).generate()

    # Modify Min and Max
    y_pos = y_pos + 80
    report.set_xy(x_pos, y_pos)

    chart = pdc.PandasChart(
        df=df_data,
        current=now_value,
        series=series_stacked,
        width=width,
        height=70,
        pdf=report,
        font_size=6,
        title="Modified Min and Max + Current",
    )
    chart.axis["left"].min = 0
    chart.axis["left"].max = 20
    chart.param.x_label_step = 2
    chart.generate()

    report.set_xy(x_pos + (report.epw / 2), y_pos)

    chart = pdc.PandasChart(
        df=df_data,
        series=series_side,
        width=80,
        height=70,
        pdf=report,
        font_size=6,
        title="Modified x_label_step",
    )
    chart.axis["left"].min = -5
    chart.axis["left"].max = 5
    chart.param.x_label_step = 4
    chart.generate()

    report.add_page()
    report.section_title("Line Chart")

    series_line = [
        pdc.SerieParam(
            name="Min-Max",
            color=PdfColors.B100,
            data_min="min",
            data_max="max",
            type="zone",
            y_axis="left",
        ),
        pdc.SerieParam(
            name="Average",
            color=PdfColors.B700,
            data="mean",
            type="line",
            y_axis="left",
        ),
    ]

    chart = pdc.PandasChart(
        df=df_data,
        series=series_line,
        width=80,
        height=70,
        pdf=report,
        font_size=6,
        title="Standard Line Chart",
    )
    chart.axis["left"].min = 50
    chart.axis["left"].max = 120
    chart.param.x_label_step = 2
    chart.generate()

    report.save()
