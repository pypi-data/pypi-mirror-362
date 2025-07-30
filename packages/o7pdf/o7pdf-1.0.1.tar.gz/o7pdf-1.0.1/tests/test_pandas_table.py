import fpdf
import pandas as pd

from o7pdf.template import Template
import o7pdf.pandas_table as pdt
from o7pdf.colors import PdfColors

from .nhl_standing_23_24 import data as nhl_standing_23_24


def test_pandas_chart():
    report = Template(filename="cache/pandas_table.pdf", title="Pandas Table Demo")
    report.add_page()

    df_data = pd.DataFrame(nhl_standing_23_24)
    df_data.sort_values(by="points", ascending=False, inplace=True)
    df_data["plusminus"] = df_data["gf"] - df_data["ga"]
    df_data["plusminusp"] = df_data["plusminus"].divide(df_data["plusminus"].abs().max()).add(1)
    df_data["pts-diff"] = df_data["points"].diff()
    df_data["ppg-diff"] = df_data["ppg"].diff()

    # print()
    # print(df_data)

    report.section_title("Pandas Table - All Cell Formats")

    columns = [
        pdt.ColumnParam(name="Team", width=40, data="teamname", align="L", merge=False),
        pdt.ColumnParam(
            name="INFO",
            width=20,
            data="arenaname",
            cell_format="INFO",
            align="L",
            group="cell_format",
        ),
        pdt.ColumnParam(
            name="WEIGHT",
            width=10,
            data="points",
            cell_format="WEIGHT",
            align="C",
            text_format="{:.0f}",
            group="cell_format",
            footer="mean",
        ),
        pdt.ColumnParam(
            name="UNDER",
            width=10,
            data="plusminusp",
            cell_format="UNDER",
            text_format="",
            group="cell_format",
        ),
        pdt.ColumnParam(
            name="OVER",
            width=10,
            data="plusminusp",
            cell_format="OVER",
            align="R",
            text_format="{:.2f}",
            group="cell_format",
        ),
        pdt.ColumnParam(
            name="DELTA",
            width=10,
            data="ppg-diff",
            cell_format="DELTA",
            align="C",
            text_format="{:.0f}",
            group="cell_format",
        ),
        pdt.ColumnParam(
            name="Footer Sum",
            width=20,
            data="ppg",
            align="C",
            text_format="{:.0f}",
            group="cell_format",
            footer="sum",
        ),
        pdt.ColumnParam(
            name="DELTA_PLUS & outofgrid",
            width=35,
            data="ppg-diff",
            cell_format="DELTA_PLUS",
            align="L",
            text_format="{:.0f}",
            outofgrid=True,
        ),
    ]

    pdt.PandasTable(
        title="NHL Standing 2023-2024",
        df=df_data,
        columns=columns,
        pdf=report,
        font_size=6,
    ).generate()

    report.section_title("Pandas Table - Multipage Break - Cell Merge")
    columns = [
        pdt.ColumnParam(name="Country", width=40, data="country", align="C", merge=True),
        pdt.ColumnParam(name="State", width=40, data="state", align="C", merge=True),
        pdt.ColumnParam(name="Team", width=40, data="teamname", align="L", merge=False),
        pdt.ColumnParam(
            name="points",
            width=10,
            data="points",
            cell_format="WEIGHT",
            align="C",
            text_format="{:.0f}",
        ),
        pdt.ColumnParam(
            name="GF",
            width=10,
            data="gf",
        ),
        pdt.ColumnParam(
            name="GA",
            width=10,
            data="ga",
        ),
        pdt.ColumnParam(
            name="",
            width=35,
            data="ppg-diff",
            cell_format="DELTA_PLUS",
            align="L",
            text_format="{:.0f}",
            outofgrid=True,
        ),
    ]

    pdt.PandasTable(
        df=df_data.sort_values(by=["country", "state", "points"], ascending=[True, True, False]),
        columns=columns,
        pdf=report,
        font_size=8,
    ).generate()

    report.section_title("Pandas Table - Row Oriented")

    df_color = pd.DataFrame()
    df_color["intensity"] = [
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "800",
        "900",
    ]
    df_color["blue"] = [
        PdfColors.B100,
        PdfColors.B200,
        PdfColors.B300,
        PdfColors.B400,
        PdfColors.B500,
        PdfColors.B600,
        PdfColors.B700,
        PdfColors.B800,
        PdfColors.B900,
    ]
    df_color["orange"] = [
        PdfColors.O100,
        PdfColors.O200,
        PdfColors.O300,
        PdfColors.O400,
        PdfColors.O500,
        PdfColors.O600,
        PdfColors.O700,
        PdfColors.O800,
        PdfColors.O900,
    ]
    df_color["red"] = [
        PdfColors.R100,
        PdfColors.R200,
        PdfColors.R300,
        PdfColors.R400,
        PdfColors.R500,
        PdfColors.R600,
        PdfColors.R700,
        PdfColors.R800,
        PdfColors.R900,
    ]
    # df_color["orangered"] = [
    #     PdfColors.OR100,
    #     PdfColors.OR200,
    #     PdfColors.OR300,
    #     PdfColors.OR400,
    #     PdfColors.OR500,
    #     PdfColors.OR600,
    #     PdfColors.OR700,
    #     PdfColors.OR800,
    #     PdfColors.OR900
    # ]
    # df_color["orangeyellow"] = [
    #     PdfColors.OY100,
    #     PdfColors.OY200,
    #     PdfColors.OY300,
    #     PdfColors.OY400,
    #     PdfColors.OY500,
    #     PdfColors.OY600,
    #     PdfColors.OY700,
    #     PdfColors.OY800,
    #     PdfColors.OY900
    # ]
    df_color["yellow"] = [
        PdfColors.Y100,
        PdfColors.Y200,
        PdfColors.Y300,
        PdfColors.Y400,
        PdfColors.Y500,
        PdfColors.Y600,
        PdfColors.Y700,
        PdfColors.Y800,
        PdfColors.Y900,
    ]

    df_color["green"] = [
        PdfColors.G100,
        PdfColors.G200,
        PdfColors.G300,
        PdfColors.G400,
        PdfColors.G500,
        PdfColors.G600,
        PdfColors.G700,
        PdfColors.G800,
        PdfColors.G900,
    ]
    df_color["bluemarin"] = [
        PdfColors.BM100,
        PdfColors.BM200,
        PdfColors.BM300,
        PdfColors.BM400,
        PdfColors.BM500,
        PdfColors.BM600,
        PdfColors.BM700,
        PdfColors.BM800,
        PdfColors.BM900,
    ]

    df_color["neutra-light"] = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
    df_color["neutra-dark"] = [
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "800",
        "900",
    ]
    df_color["light"] = [
        PdfColors.N10,
        PdfColors.N20,
        PdfColors.N30,
        PdfColors.N40,
        PdfColors.N50,
        PdfColors.N60,
        PdfColors.N70,
        PdfColors.N80,
        PdfColors.N90,
    ]
    df_color["dark"] = [
        PdfColors.N100,
        PdfColors.N200,
        PdfColors.N300,
        PdfColors.N400,
        PdfColors.N500,
        PdfColors.N600,
        PdfColors.N700,
        PdfColors.N800,
        PdfColors.N900,
    ]

    columns = [
        pdt.ColumnParam(
            name="Intensity",
            width=15,
            data="intensity",
            align="C",
        ),
        pdt.ColumnParam(
            name="O7 Orange",
            width=15,
            color_fg="orange",
            color_bg="orange",
            data="orange",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="O7 Blue",
            width=15,
            color_fg="blue",
            color_bg="blue",
            data="blue",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="Red",
            width=15,
            color_fg="red",
            color_bg="red",
            data="red",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        # pdt.ColumnParam(
        #     name="Orange-Red",
        #     width=15,
        #     color_fg="orangered",
        #     color_bg="orangered",
        #     data="orangered",
        #     cell_format="INFO",
        #     align="C",
        #     text_format="",
        # ),
        # pdf.ColumnParam(
        #     name="Orange-Yellow",
        #     width=15,
        #     color_fg="orangeyellow",
        #     color_bg="orangeyellow",
        #     data="orangeyellow",
        #     cell_format="INFO",
        #     align="C",
        #     text_format="",
        # ),
        pdt.ColumnParam(
            name="Yellow",
            width=15,
            color_fg="yellow",
            color_bg="yellow",
            data="yellow",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="Green",
            width=15,
            color_fg="green",
            color_bg="green",
            data="green",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="Blue Marin",
            width=15,
            color_fg="bluemarin",
            color_bg="bluemarin",
            data="bluemarin",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="Intensity",
            width=15,
            data="neutra-light",
            align="C",
        ),
        pdt.ColumnParam(
            name="Neutral Light",
            width=15,
            color_fg="light",
            color_bg="light",
            data="light",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
        pdt.ColumnParam(
            name="Intensity",
            width=15,
            data="neutra-dark",
            align="C",
        ),
        pdt.ColumnParam(
            name="Neutral Dark",
            width=15,
            color_fg="dark",
            color_bg="dark",
            data="dark",
            cell_format="INFO",
            align="C",
            text_format="",
        ),
    ]
    obj = pdt.PandasTable(
        df=df_color, columns=columns, pdf=report, font_size=6, orientation="row"
    ).generate()

    charth_height = obj.get_height()

    report.save()
