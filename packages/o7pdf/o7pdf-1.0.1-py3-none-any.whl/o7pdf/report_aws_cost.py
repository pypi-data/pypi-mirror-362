"""Module to Reports in PDF Format"""

import datetime
import logging

import pandas as pd

import o7pdf.pandas_chart as pdc
import o7pdf.pandas_table as pdt
from o7pdf.colors import PdfColors
from o7pdf.template import Template

logger = logging.getLogger(__name__)


# pylint: disable=singleton-comparison


# *************************************************
#
# *************************************************
def record_type_sort(record_type: str) -> int:
    if record_type == "Usage":
        return 1
    if record_type == "DiscountedUsage":
        return 2
    if record_type == "Recurring":
        return 3
    if record_type == "SubTotal":
        return 10
    if record_type == "Forecast":
        return 20
    if record_type == "Support":
        return 70
    if record_type == "Credit":
        return 80
    if record_type == "Tax":
        return 99
    if record_type == "Total":
        return 100

    return 10


class ColorDelta:
    def __init__(
        self,
        max_alm: float = 5.0,
        min_alm: float = None,
        max_wrn: float = None,
        min_wrn: float = None,
    ):
        self.max_alm = max_alm
        self.min_alm = min_alm if min_alm else -max_alm

        self.max_wrn = max_wrn if max_wrn else max_alm / 5.0
        self.min_wrn = min_wrn if min_wrn else -self.max_wrn

    # *************************************************
    #
    # *************************************************
    def color_delta_bg(self, diff: float) -> int:
        if diff > self.max_alm:
            return PdfColors.R600

        if diff < self.min_alm:
            return PdfColors.G600

        return PdfColors.N0

    # *************************************************
    #
    # *************************************************
    def color_delta_fg(self, diff: float) -> int:
        if diff > self.max_alm:
            return PdfColors.N0

        if diff > 1.0:
            return PdfColors.R600

        if diff < self.min_alm:
            return PdfColors.N0

        if diff < -1.0:
            return PdfColors.G600

        return PdfColors.N10


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class ReportAwsCost(Template):
    """Class temaplate to generate PDF Report"""

    def __init__(self, forecast: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.forecast = forecast
        self.title = (
            "AWS Montly Cost & Forecast Report" if self.forecast else "AWS Monthly Cost Report"
        )

        self.current_month: str = None
        self.current_month_long: str = None
        self.first_month: str = None
        self.last_month_long: str = None
        self.last_month: str = None
        self.previous_month: str = None
        self.previous_month_long: str = None
        self.months: list[datetime.date] = []

        self.first_day: datetime.date = None
        self.yesterday: datetime.date = None
        self.last_day: datetime.date = None

        self.df_usage: pd.DataFrame = None
        self.df_usage_daily: pd.DataFrame = None
        self.df_totals: pd.DataFrame = None
        self.df_accounts: pd.DataFrame = None

    # *************************************************
    #
    # *************************************************
    def chart_last_year(
        self, df_totals_last_year: pd.DataFrame, width: float = 80, height: float = 50
    ):
        """Fill Check historic charts"""
        title = "Last Year Montly **Usage** (USD)"

        series = [
            pdc.SerieParam(
                name="Usage",
                color=PdfColors.BM500,
                data="SubTotal",
                type="bar",
                y_axis="left",
                is_stacked=True,
            ),
        ]

        forecast_max = 0.0
        if self.forecast:
            series.insert(
                0,
                pdc.SerieParam(
                    name="Forecast",
                    color=PdfColors.O500,
                    data="Forecast",
                    type="bar",
                    y_axis="left",
                    is_stacked=True,
                ),
            )
            title = "Last Year Montly **Usage** & Forecast (USD)"
            forecast_max = (
                df_totals_last_year["Forecast"] + df_totals_last_year["SubTotal"]
            ).max() * 1.2

        chart = pdc.PandasChart(
            df=df_totals_last_year,
            series=series,
            width=width,
            height=height,
            pdf=self,
            font_size=6,
            title=title,
        )
        chart_max = df_totals_last_year["SubTotal"].max() * 1.2
        chart_max = max(chart_max, forecast_max)
        chart.axis["left"].min = 0
        chart.axis["left"].max = (int(chart_max / 100) + 1) * 100
        chart.param.spacing = 0.40
        chart.param.x_label_step = 3
        chart.generate()

    # *************************************************
    #
    # *************************************************
    def table_last_year(self, df_year_totals: pd.DataFrame):
        """Fill Check historic charts"""

        columns = [pdt.ColumnParam(name="Month", width=10, data="month", align="C", merge=False)]

        df_local = df_year_totals.copy()
        df_local["color_bg"] = [PdfColors.O100] * len(df_local.index)

        for record_type in df_year_totals.columns:
            if record_type in ("month", "7dmean"):
                continue

            params = {
                "name": record_type,
                "width": 10,
                "data": record_type,
                "align": "R",
                "merge": False,
                "text_format": "{:,.0f}",
                "footer": "sum",
            }

            if record_type in ("SubTotal", "Total"):
                params["color_bg"] = "color_bg"

            if record_type in ("SubTotal", "Usage", "Discount", "Recurring"):
                params["group"] = "Usage"

            columns.append(pdt.ColumnParam(**params))
        # print(df_local)
        pdt.PandasTable(
            df=df_local.reset_index().tail(12), columns=columns, pdf=self, font_size=6
        ).generate()

    # *************************************************
    #
    # *************************************************
    def table_usage_by_dimension(
        self,
        df_usage: pd.DataFrame,
        dimension: str,
        dimension_width: int = 15,
        months: int = 2,
        min_total: float = -1.0,
        title: str = None,
        df_usage_daily: pd.DataFrame = None,
    ):
        """Table of Account Usage"""

        # print(f"table_usage_by_dimension dimension={dimension} ")

        # ------------------------------------------
        # Print Title
        # ------------------------------------
        if title:
            with self.local_context():
                self.set_font("OpenSans", size=10)

                # https://py-pdf.github.io/fpdf2/fpdf/fpdf.html#fpdf.fpdf.FPDF.cell
                self.cell(
                    w=dimension_width,
                    h=self.font_size * 1.5,
                    text=f"**{title}**",
                    fill=False,
                    new_x="LEFT",
                    new_y="NEXT",
                    align="L",
                    border="",
                    markdown=True,
                )

        months = [month.strftime("%Y-%m") for month in self.months[-months:]]
        group_name = f"Last {len(months)} Month"
        # print(months)

        # ------------------------------------------
        # Compile Usage Details for dimension
        # ------------------------------------
        df_pivot = df_usage.pivot_table(
            values=["amount"],
            index=[dimension],
            columns=["month"],
            aggfunc="sum",
            fill_value=0.0,
        )
        df_pivot.columns = df_pivot.columns.droplevel()
        df_pivot["total"] = df_pivot.sum(axis=1)
        df_pivot = df_pivot.sort_values(by="total", ascending=False)
        df_pivot = df_pivot.fillna(0.0)

        df_pivot = df_pivot[df_pivot["total"] > min_total]

        if self.forecast:
            # print(df_usage_daily)
            df_last_2days = df_usage_daily[df_usage_daily["date"] >= self.yesterday]
            df_daily = df_usage_daily.groupby([dimension])["amount"].sum() / 7.0

            df_pivot["7dmean"] = df_daily
            df_pivot["2dmean"] = df_last_2days.groupby([dimension])["amount"].sum() / 2.0
            df_pivot["30d"] = df_pivot["7dmean"] * 30.5
            df_pivot = df_pivot.fillna(0.0)

            day_left_in_month = 30.5 - self.last_day.day

            if self.current_month not in df_pivot.columns:
                df_pivot[self.current_month] = 0.0

            df_pivot["forecast"] = df_pivot[self.current_month] + (
                df_pivot["7dmean"] * day_left_in_month
            )
            # print(df_daily)

        # print(df_pivot)
        # exit(0)

        previous_month = months[0]

        columns = [
            pdt.ColumnParam(
                name=dimension,
                width=dimension_width,
                data=dimension,
                align="L",
                merge=False,
                text_trim=True,
            ),
        ]
        columns.append(
            pdt.ColumnParam(
                name="12 Months",
                width=15,
                data="total",
                text_format="{:,.2f}$",
                cell_format="WEIGHT_SUM",
                align="R",
                footer="sum",
            )
        )
        columns.append(
            pdt.ColumnParam(
                name=previous_month,
                width=12,
                data=previous_month,
                text_format="{:,.2f}$",
                cell_format="WEIGHT_SUM",
                align="R",
                footer="sum",
                group=group_name,
            )
        )

        previous_month = months[0]
        last_month = months[-1]
        if previous_month not in df_pivot.columns:
            df_pivot[previous_month] = 0.0

        last_month_totals = df_pivot[last_month].sum() if last_month in df_pivot.columns else 0.0
        alarm_level = max(last_month_totals * 0.005, 5)
        # print(f"Last Month Total -> {last_month_totals}")

        color_obj = ColorDelta(max_alm=alarm_level)

        for month in months[1:]:
            delta_col = f"{month}_d"
            delta_col_bg = f"{delta_col}_bg"
            delta_col_fg = f"{delta_col}_fg"

            if month not in df_pivot.columns:
                df_pivot[month] = 0.0

            df_pivot[delta_col] = df_pivot[month] - df_pivot[previous_month]
            df_pivot[delta_col_bg] = df_pivot[delta_col].apply(color_obj.color_delta_bg)
            df_pivot[delta_col_fg] = df_pivot[delta_col].apply(color_obj.color_delta_fg)
            previous_month = month

            columns.append(
                pdt.ColumnParam(
                    name=month,
                    width=12,
                    data=month,
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group=group_name,
                )
            )
            if not self.forecast:
                columns.append(
                    pdt.ColumnParam(
                        name="+/-",
                        width=10,
                        data=delta_col,
                        text_format="{:,.0f}",
                        cell_format="DELTA_PLUS",
                        color_bg=delta_col_bg,
                        color_fg=delta_col_fg,
                        align="C",
                        footer="sum",
                        group=group_name,
                    )
                )

        if self.forecast:
            df_pivot["delta_forecast"] = df_pivot["30d"] - df_pivot[self.last_month]
            df_pivot["delta_forecast_bg"] = df_pivot["delta_forecast"].apply(
                color_obj.color_delta_bg
            )
            df_pivot["delta_forecast_fg"] = df_pivot["delta_forecast"].apply(
                color_obj.color_delta_fg
            )

            columns.append(
                pdt.ColumnParam(
                    name="Month",
                    width=12,
                    data=self.current_month,
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group="Current",
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name="7d mean",
                    width=12,
                    data="7dmean",
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group="Current",
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name="2d mean",
                    width=12,
                    data="2dmean",
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group="Current",
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name=self.current_month,
                    width=12,
                    data="forecast",
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group="Forecast",
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name="x 30.5",
                    width=12,
                    data="30d",
                    text_format="{:,.2f}$",
                    cell_format="WEIGHT_SUM",
                    align="R",
                    footer="sum",
                    group="Forecast",
                )
            )
            columns.append(
                pdt.ColumnParam(
                    name="+/-",
                    width=10,
                    data="delta_forecast",
                    text_format="{:,.0f}",
                    cell_format="DELTA_PLUS",
                    color_bg="delta_forecast_bg",
                    color_fg="delta_forecast_fg",
                    align="C",
                    footer="sum",
                    group="Forecast",
                )
            )

        # print(df_pivot.iloc[0])
        # import pprint
        # pprint.pprint(columns)
        # exit(0)

        pdt.PandasTable(
            df=df_pivot.reset_index(),
            columns=columns,
            pdf=self,
            font_size=6,
        ).generate()

        # exit(0)

    # *************************************************
    #
    # *************************************************
    def text_summary_forecast(self, df_year_totals: pd.DataFrame):
        # print(df_year_totals)

        last_month_totals = (
            df_year_totals.loc[self.last_month]["SubTotal"]
            if self.last_month in df_year_totals.index
            else 0.0
        )
        current_month_totals = (
            df_year_totals.loc[self.current_month]["SubTotal"]
            if self.current_month in df_year_totals.index
            else 0.0
        )
        current_month_endom = (
            df_year_totals.loc[self.current_month]["Forecast"]
            if self.current_month in df_year_totals.index
            else 0.0
        )

        current_month_forecast = current_month_totals + current_month_endom
        current_days = self.last_day.day

        mean_7d = df_year_totals.loc["NEXT30"]["7dmean"]
        next_30days_forecast = df_year_totals.loc["NEXT30"]["Forecast"]

        current_month_delta = current_month_forecast - last_month_totals
        next_30days_delta = next_30days_forecast - last_month_totals

        x_middle = self.l_margin + (self.w / 4)

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__{self.last_month_long} Usage__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=16)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{last_month_totals:.2f} USD** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        self.ln(1.0)

        # ---------------------------------------
        # 2nd row of data
        # ---------------------------------------
        last_y = self.get_y()
        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__{self.current_month_long} ({current_days} days) :__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=12)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{current_month_totals:.2f}**",
                fill=False,
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                border=0,
                markdown=True,
            )

        self.set_xy(x_middle, last_y)
        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text="__Last 7 days average :__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=12)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{mean_7d:.2f}**",
                fill=False,
                new_x="RIGHT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        self.ln(1.0)

        # ---------------------------------------
        # 3rd row of data
        # ---------------------------------------
        last_y = self.get_y()
        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__{self.current_month_long} + end of month forecast :__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=12)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{current_month_forecast:.2f}**",
                fill=False,
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                border=0,
                markdown=True,
            )

        cell_color = PdfColors.R600 if current_month_delta >= 0 else PdfColors.G600
        cell_text = (
            f"**(+ {current_month_delta:.2f})**"
            if current_month_delta >= 0
            else f"(**{current_month_delta:.2f})**"
        )
        with self.local_context():
            self.set_font("OpenSans", size=8)
            self.set_text_color(**cell_color)
            self.cell(
                text=cell_text,
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        self.set_xy(x_middle, last_y)
        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text="__Next 30.5 days forecast :__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=12)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{next_30days_forecast:.2f}**",
                fill=False,
                new_x="RIGHT",
                new_y="TOP",
                align="L",
                border=0,
                markdown=True,
            )

        cell_color = PdfColors.R600 if next_30days_delta >= 0 else PdfColors.G600
        cell_text = (
            f"**(+ {next_30days_delta:.2f})**"
            if next_30days_delta >= 0
            else f"(**{next_30days_delta:.2f})**"
        )
        with self.local_context():
            self.set_font("OpenSans", size=8)
            self.set_text_color(**cell_color)
            self.cell(
                text=cell_text,
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

    # *************************************************
    #
    # *************************************************
    def text_summary(self, df_year_totals: pd.DataFrame):
        if self.forecast:
            return self.text_summary_forecast(df_year_totals)

        last_month_subtotal = (
            df_year_totals.loc[self.last_month]["SubTotal"]
            if self.last_month in df_year_totals.index
            else 0.0
        )

        if len(df_year_totals) > 1:
            previous_month_totals = df_year_totals.iloc[-2]
            usage_delta = last_month_subtotal - previous_month_totals["SubTotal"]
        else:
            usage_delta = 0.0

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__{self.last_month_long} Usage__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=20)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"**{last_month_subtotal:.2f} USD** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"__Delta to {self.previous_month_long}:__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        cell_color = PdfColors.R600 if usage_delta >= 0 else PdfColors.G600
        cell_text = (
            f"**+ {usage_delta:.2f} USD**" if usage_delta >= 0 else f"**{usage_delta:.2f} USD**"
        )
        with self.local_context():
            self.set_font("OpenSans", size=10)
            self.set_text_color(**cell_color)
            self.cell(
                text=cell_text,
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

    # *************************************************
    #
    # *************************************************
    def get_totals_per_account(self, account: str = None):
        print(f"get_totals_per_account account={account}")

        df_totals = (
            self.df_totals[self.df_totals["account"] == account].copy()
            if account
            else self.df_totals
        )

        # If forecast add the forecast to the totals
        if self.forecast:
            df_usage_daily = (
                self.df_usage_daily[self.df_usage_daily["account"] == account].copy()
                if account
                else self.df_usage_daily
            )

            last_days_sum = df_usage_daily["amount"].sum()
            day_average = last_days_sum / 7.0
            day_left_in_month = 30.5 - self.last_day.day
            forecast_amount = day_average * day_left_in_month
            next_30days_amount = day_average * 30.5

            print("Forecast Total Amounts")
            print(f"Last 7 Days Sum -> {last_days_sum}")
            print(f"Day Average -> {day_average}")
            print(f"forecast_left-> {forecast_amount}")

            df_forecast = pd.DataFrame(
                [
                    {
                        "month": self.current_month,
                        "RECORD_TYPE": "Forecast",
                        "amount": forecast_amount,
                    },
                    {
                        "month": "NEXT30",
                        "RECORD_TYPE": "Forecast",
                        "amount": next_30days_amount,
                    },
                    {
                        "month": "NEXT30",
                        "RECORD_TYPE": "7dmean",
                        "amount": day_average,
                    },
                ]
            )

            df_totals = pd.concat([df_totals, df_forecast])

        df_totals = df_totals.groupby(["month", "RECORD_TYPE"])["amount"].sum()
        df_totals = df_totals.reset_index().pivot_table(
            values=["amount"],
            index=["month"],
            columns=["RECORD_TYPE"],
            aggfunc="sum",
            fill_value=0.0,
            margins=False,
        )
        df_totals.columns = df_totals.columns.droplevel()

        for record_type in ["Usage", "DiscountedUsage", "Recurring", "Support", "Credit", "Tax"]:
            if record_type not in df_totals.columns:
                df_totals[record_type] = 0.0

        df_totals["SubTotal"] = df_totals[["Usage", "DiscountedUsage", "Recurring"]].sum(axis=1)
        df_totals["Total"] = df_totals[["SubTotal", "Support", "Credit", "Tax"]].sum(axis=1)

        df_totals = df_totals.reindex(sorted(df_totals.columns, key=record_type_sort), axis=1)

        if "DiscountedUsage" in df_totals.columns:
            df_totals = df_totals.rename(columns={"DiscountedUsage": "Discount"})

        return df_totals

    # *************************************************
    #
    # *************************************************
    def clean_total_data(self, df_raw: pd.DataFrame, df_accounts: pd.DataFrame) -> pd.DataFrame:
        df_totals = df_raw
        usage_last_month = self.current_month if self.forecast else self.last_month

        df_totals = df_totals[
            (df_totals["date"] >= self.first_month) & (df_totals["date"] <= usage_last_month)
        ].copy()
        df_totals["month"] = df_totals["date"].dt.strftime("%Y-%m")

        df_totals = df_totals.merge(
            df_accounts[["Id", "Name"]], left_on="LINKED_ACCOUNT", right_on="Id", how="left"
        )
        df_totals["account"] = (
            df_totals["LINKED_ACCOUNT"].fillna(0).astype(str).str.removesuffix(".0")
            + " - "
            + df_totals["Name"]
        )
        df_totals = df_totals.drop(columns=["Id", "Name"])

        return df_totals

    # *************************************************
    #
    # *************************************************
    def clean_usage_data(
        self, df_raw: pd.DataFrame, df_accounts: pd.DataFrame, is_daily: bool = False
    ) -> pd.DataFrame:
        df_usage = df_raw
        usage_last_month = self.current_month if self.forecast else self.last_month

        if is_daily:
            df_usage = df_usage[
                (df_usage["date"] >= self.first_day) & (df_usage["date"] <= self.last_day)
            ].copy()
            df_usage["month"] = df_usage["date"].dt.strftime("%Y-%m-%d")
        else:
            df_usage = df_usage[
                (df_usage["date"] >= self.first_month) & (df_usage["date"] <= usage_last_month)
            ].copy()
            df_usage["month"] = df_usage["date"].dt.strftime("%Y-%m")

        df_usage = df_usage.merge(
            df_accounts[["Id", "Name"]], left_on="LINKED_ACCOUNT", right_on="Id", how="left"
        )
        df_usage["account"] = df_usage["LINKED_ACCOUNT"].astype(str) + " - " + df_usage["Name"]
        df_usage = df_usage.drop(columns=["Id", "Name"])

        df_usage["SERVICE"] = (
            df_usage["SERVICE"].str.replace("Amazon", "").str.replace("AWS", "").str.strip()
        )

        return df_usage

    # *************************************************
    #
    # *************************************************
    def compile_data(self, dfs: dict[pd.DataFrame]):
        """Compile the data for the report"""

        # Sanatize Data
        dfs["totals"]["date"] = dfs["totals"]["date"].apply(lambda x: pd.Timestamp(x))
        dfs["usage"]["date"] = dfs["usage"]["date"].apply(lambda x: pd.Timestamp(x))

        current_month = dfs["totals"]["date"].max()
        last_month = current_month.replace(day=1) - pd.DateOffset(months=1)
        self.months = [(last_month.replace(day=1) - pd.DateOffset(months=i)) for i in range(12)][
            ::-1
        ]

        if self.forecast:
            dfs["usage_daily"]["date"] = dfs["usage_daily"]["date"].apply(lambda x: pd.Timestamp(x))
            self.last_day = dfs["usage_daily"]["date"].max()
            self.yesterday = self.last_day - pd.DateOffset(days=1)
            self.first_day = self.last_day - pd.DateOffset(days=6)

        previous_month = self.months[-2]
        first_month = self.months[0]
        # print(self.months)

        self.current_month_long = current_month.strftime("%B %Y")
        self.last_month_long = last_month.strftime("%B %Y")
        self.previous_month_long = previous_month.strftime("%B %Y")

        self.current_month = current_month.strftime("%Y-%m")
        self.first_month = first_month.strftime("%Y-%m")
        self.last_month = last_month.strftime("%Y-%m")
        self.previous_month = previous_month.strftime("%Y-%m")

        print(f"Current Month -> {self.current_month}")
        print(f"Current Month -> {self.current_month_long}")

        print(f"First Month -> {self.first_month}")
        print(f"Previous Month -> {self.previous_month}")
        print(f"Last Month -> {self.last_month}")
        print(f"Last Month -> {self.last_month_long}")

        print(f"First Day -> {self.first_day}")
        print(f"Yesterday -> {self.yesterday}")
        print(f"Last Day -> {self.last_day}")

        df_accounts = dfs["accounts"]

        # ------------------------------------
        # Clean Up Totals
        # ------------------------------------
        self.df_totals = self.clean_total_data(dfs["totals"], df_accounts=df_accounts)
        print(self.df_totals)

        # ------------------------------------
        # Clean Up Usage
        # ------------------------------------
        # print(df_usage)
        self.df_usage = self.clean_usage_data(dfs["usage"], df_accounts=df_accounts)
        if self.forecast:
            self.df_usage_daily = self.clean_usage_data(
                dfs["usage_daily"], df_accounts=df_accounts, is_daily=True
            )

        self.df_accounts = (
            self.df_usage.groupby(["account"])["amount"]
            .sum()
            .reset_index()
            .sort_values(by="amount", ascending=False)
        )
        # print(self.df_accounts)

        return self

    # *************************************************
    #
    # *************************************************
    def generate_organization_page(self):
        print("generate_organization_page")

        start_y = self.get_y()
        middle = (self.w / 2) - 10.0
        df_year_totals = self.get_totals_per_account()

        self.text_summary(df_year_totals)
        self.ln(5)
        self.chart_last_year(df_year_totals, width=70, height=30)
        chart_y = self.get_y()

        self.set_xy(middle, start_y)
        self.table_last_year(df_year_totals)
        table_y = self.get_y()

        self.set_y(max(chart_y, table_y))

        self.ln(10)
        start_y = self.get_y()

        number_of_months = 6  # if self.forecast else 2

        self.set_xy(self.l_margin, start_y)
        self.table_usage_by_dimension(
            self.df_usage,
            dimension="account",
            dimension_width=40,
            title="Per Account",
            months=number_of_months,
            df_usage_daily=self.df_usage_daily,
        )

        self.ln(5)
        self.set_xy(self.l_margin, self.get_y())

        self.table_usage_by_dimension(
            self.df_usage,
            dimension="SERVICE",
            dimension_width=40,
            title="Per Service",
            months=number_of_months,
            df_usage_daily=self.df_usage_daily,
        )

    # *************************************************
    #
    # *************************************************
    def generate_account_page(self, account: str):
        print(f"generate_account_page account={account}")

        self.add_page()
        self.section_title(f"Account: {account}")

        start_y = self.get_y()
        middle = self.w / 2
        self.set_xy(self.l_margin, start_y)

        df_year_totals = self.get_totals_per_account(account=account)

        if len(df_year_totals) == 0:
            print(f"No data for account {account}")
            return

        self.text_summary(df_year_totals)
        self.ln(5)
        self.chart_last_year(df_year_totals, width=70, height=30)
        self.set_xy(middle, start_y)
        self.table_last_year(df_year_totals)

        start_y = 90

        df_usage = self.df_usage[self.df_usage["account"] == account]
        df_usage_daily = (
            self.df_usage_daily[self.df_usage_daily["account"] == account]
            if self.forecast
            else None
        )

        self.set_xy(self.l_margin, start_y)
        self.table_usage_by_dimension(
            df_usage=df_usage,
            dimension="SERVICE",
            dimension_width=40,
            months=6,
            min_total=0.01,
            title="Per Service",
            df_usage_daily=df_usage_daily,
        )

        self.ln(5)

        # Print details for top services (5% of total)
        self.sub_title("Detail Usage for Top Services")
        top_services = df_usage.groupby("SERVICE")["amount"].sum().sort_values(ascending=False)
        top_services_pct = top_services / top_services.sum()
        top_services_pct = top_services_pct[top_services_pct > 0.05]
        for service, percent in top_services_pct.items():
            df_service = df_usage[df_usage["SERVICE"] == service]
            df_service_daily = (
                df_usage_daily[df_usage_daily["SERVICE"] == service] if self.forecast else None
            )
            self.table_usage_by_dimension(
                df_usage=df_service,
                dimension="USAGE_TYPE",
                dimension_width=40,
                months=6,
                min_total=0.01,
                title=f"{service} ({percent * 100:.1f}%) per Usage Type",
                df_usage_daily=df_service_daily,
            )

    # *************************************************
    #
    # *************************************************
    def generate(self, dfs: dict[pd.DataFrame]):
        """Return Report from the notes in Pdf format"""

        print("Generate Cost Report")

        # import o7util.pandas
        # o7util.pandas.dfs_to_excel(dfs=dfs, filename="aws-cost-data-20250219.xlsx")

        self.compile_data(dfs)

        if self.forecast:
            self.title = f"AWS Cost & Forecast Report - {self.current_month_long}"
        else:
            self.title = f"AWS Cost Report - {self.last_month_long}"

        self.alias_nb_pages()
        self.add_page()
        self.report_head()

        self.generate_organization_page()

        for account in self.df_accounts["account"]:
            self.generate_account_page(account)

        return self


if __name__ == "__main__":
    import o7util.pandas

    #     dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data.xlsx")
    #     obj = ReportAwsCost(filename="cache/aws_cost.pdf")
    #     obj.generate(dfs=dfs)
    #     obj.save()

    #     dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data-big.xlsx")
    #     obj = ReportAwsCost(filename="cache/aws_cost-big.pdf")
    #     obj.generate(dfs=dfs)
    #     obj.save()

    # dfs = o7util.pandas.dfs_from_excel("tests/sechub-data-with-type.xlsx")
    # dfs = o7util.pandas.dfs_from_excel("aws-cost-report-data-forcast-20250325.xlsx")
    # obj = ReportAwsCost(filename="cache/aws-cpat-forecast.pdf", forecast=True)

    dfs = o7util.pandas.dfs_from_excel("aws-cost-report-norda-20250327.xlsx")
    obj = ReportAwsCost(filename="cache/aws-norda-forecast.pdf", forecast=True)

    obj.generate(dfs=dfs)
    obj.save()
