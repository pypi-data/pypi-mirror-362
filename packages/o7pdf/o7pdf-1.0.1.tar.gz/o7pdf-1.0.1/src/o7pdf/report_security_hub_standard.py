"""Module to Reports in PDF Format"""

import ast
import dataclasses
import logging

import pandas as pd

import o7pdf.pandas_chart as pdc
import o7pdf.pandas_table as pdt
from o7pdf.colors import PdfColors
from o7pdf.template import Template

logger = logging.getLogger(__name__)


# pylint: disable=singleton-comparison


@dataclasses.dataclass
class ReportCompiledData:  # pylint: disable=too-many-instance-attributes
    """Compiled data for the report"""

    standard_short: str
    standard_name: str
    standard_description: str
    standard_control_count: int
    standard_score: float
    standard_total: int
    standard_pass: int
    accounts_mean_score: float
    df_accounts: pd.DataFrame
    df_controls: pd.DataFrame
    df_suppressed: pd.DataFrame = None
    df_history: pd.DataFrame = None
    df_findings_summary: pd.DataFrame = None
    df_findings_top: pd.DataFrame = None


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class ReportSecurityHubStandard(Template):
    """Class temaplate to generate PDF Report"""

    COLOR_CRITICAL = PdfColors.R800  # hex_to_rgb("#7d2105")
    COLOR_HIGH = PdfColors.R500  # .hex_to_rgb("#ba2e0f")
    COLOR_MEDIUM = PdfColors.O500  # hex_to_rgb("#cc5f21")
    COLOR_LOW = PdfColors.Y500  # .hex_to_rgb("#b2911c")

    COLOR_PASSED = PdfColors.G500  # .hex_to_rgb("#67a353")
    COLOR_FAILED = PdfColors.R500  # .hex_to_rgb("#ba2e0f")
    COLOR_NODATA = PdfColors.N80  # .hex_to_rgb("#3184c2")
    COLOR_UNKNOWN = PdfColors.B500
    COLOR_DISABLED = PdfColors.N80

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Security Hub Standard Report"

    # *************************************************
    #
    # *************************************************
    def get_score_color(self, score: float):
        """Return the color for the score"""
        return self.COLOR_PASSED if score > 0.8 else self.COLOR_FAILED

    # *************************************************
    #
    # *************************************************
    def standard_info(self, data: ReportCompiledData, width: float = 100):
        """Fill the Standard Information Section"""

        # print(standard)
        with self.local_context():
            self.set_text_color(**self.TEXT_FG)
            self.set_draw_color(**self.SUB_TITLE_BG)
            self.set_fill_color(**self.SUB_TITLE_BG)
            self.set_line_width(0.2)
            self.set_font("OpenSans", size=10)
            height = self.font_size * 1.5

            self.cell(
                w=width,
                h=height,
                text=f"**{data.standard_short}** ",
                fill=True,
                new_x="LEFT",
                new_y="NEXT",
                align="C",
                border=1,
                markdown=True,
            )

            self.set_font("OpenSans", size=8)
            self.cell(
                w=width,
                h=height,
                text=f"**Name:** {data.standard_name}",
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=1,
                markdown=True,
            )
            self.multi_cell(
                w=width,
                h=height,
                text=f"**Decription:** {data.standard_description}",
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=1,
                markdown=True,
            )
            self.cell(
                w=width,
                h=height,
                text=f"**Number of Controls:** {data.standard_control_count:,.0f}",
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=1,
                markdown=True,
            )

    # *************************************************
    #
    # *************************************************
    def standard_results(self, data: ReportCompiledData):
        """Fill the Results Block"""

        # print(standard)

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text="__Global Security score__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=24)
            self.set_text_color(**self.get_score_color(data.standard_score))
            self.cell(
                text=f"**{(data.standard_score * 100):.1f}%** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=8)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"{data.standard_pass} of {data.standard_total} controls passed",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        self.ln(7)

        with self.local_context():
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text="__Account Average Security score__",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=24)
            self.set_text_color(**self.get_score_color(data.accounts_mean_score))
            self.cell(
                text=f"**{(data.accounts_mean_score * 100):.1f}%** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        with self.local_context():
            self.set_font("OpenSans", size=8)
            self.set_text_color(**self.TEXT_FG)
            self.cell(
                text=f"{len(data.df_accounts.index)} Accounts",
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
    def checks_summary_table(self, data: ReportCompiledData):
        """Fill Check summary table"""

        with self.local_context():
            self.set_text_color(**self.TEXT_FG)
            self.set_font("OpenSans", size=10)

            self.cell(
                w=100,
                h=7,
                text="**Summary of all checks** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        columns = [
            pdt.ColumnParam(
                name="Severity",
                width=20,
                data="SeverityRating",
                color_bg="SeverityColor",
                color_fg="TextColor",
                align="C",
            ),
            pdt.ColumnParam(
                name="Count",
                width=20,
                data="CheckCount",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
            ),
            pdt.ColumnParam(
                name="Failed",
                width=20,
                data="CheckFail",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
            ),
            pdt.ColumnParam(
                name="Passed",
                width=20,
                data="CheckPass",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
            ),
            # pdt.ColumnParam(
            #     name="Suppressed",
            #     width=20,
            #     data="suppressed",
            #     text_format="{:,.0f}",
            #     align="C",
            #     footer="sum",
            # ),
            pdt.ColumnParam(
                name="Pass %",
                width=20,
                data="passed_percent",
                text_format="{:.1%}",
                align="C",
            ),
        ]

        pdt.PandasTable(
            df=data.df_findings_summary, columns=columns, pdf=self, font_size=8
        ).generate()

    # *************************************************
    #
    # *************************************************
    def accounts_historic_chart(self, data: ReportCompiledData):
        if data.df_history is None:
            print("No historical data")
            return

        serie = [
            pdc.SerieParam(
                name="MinMax",
                color=PdfColors.B100,
                data_min="score_min",
                data_max="score_max",
                type="zone",
                y_axis="left",
            ),
            pdc.SerieParam(
                name="Average",
                color=PdfColors.O500,
                data="score_mean",
                type="line",
                y_axis="left",
            ),
        ]

        chart = pdc.PandasChart(
            df=data.df_history,
            series=serie,
            width=160,
            height=35,
            pdf=self,
            font_size=6,
            title="Historical Account Security Score",
        )
        chart.axis["left"].min = round(max(data.df_history["score_min"].min() - 15, 0) / 10) * 10
        chart.axis["left"].max = 110
        chart.param.x_label_step = 4
        chart.generate()

    # *************************************************
    #
    # *************************************************
    def checks_historic_charts(self, data: ReportCompiledData):
        """Fill Check historic charts"""

        if data.df_history is None:
            print("No historical data")
            return

        current_y = self.get_y()

        current_checks = pd.Series(
            {
                "critical": data.df_findings_summary[
                    data.df_findings_summary["SeverityRating"] == "CRITICAL"
                ]["CheckFail"].sum(),
                "high": data.df_findings_summary[
                    data.df_findings_summary["SeverityRating"] == "HIGH"
                ]["CheckFail"].sum(),
                "medium": data.df_findings_summary[
                    data.df_findings_summary["SeverityRating"] == "MEDIUM"
                ]["CheckFail"].sum(),
                "low": data.df_findings_summary[
                    data.df_findings_summary["SeverityRating"] == "LOW"
                ]["CheckFail"].sum(),
            }
        )
        current_checks.name = "Now"

        series = [
            pdc.SerieParam(
                name="Critical",
                color=self.COLOR_CRITICAL,
                data="critical",
                type="bar",
                y_axis="left",
                is_stacked=True,
            ),
            pdc.SerieParam(
                name="High",
                color=self.COLOR_HIGH,
                data="high",
                type="bar",
                y_axis="left",
                is_stacked=True,
            ),
        ]

        chart = pdc.PandasChart(
            df=data.df_history,
            current=current_checks,
            series=series,
            width=80,
            height=70,
            pdf=self,
            font_size=6,
            title="Weekly Historical Critical & High Failed Checks",
        )
        chart_max = data.df_history[["critical", "high"]].max().max() * 1.2
        chart.axis["left"].min = 0
        chart.axis["left"].max = (int(chart_max / 10) + 1) * 10
        chart.param.spacing = 0.60
        chart.param.x_label_step = 4
        chart.generate()

        self.set_xy(100, current_y)

        series = [
            pdc.SerieParam(
                name="Medium",
                color=self.COLOR_MEDIUM,
                data="medium",
                type="bar",
                y_axis="left",
                is_stacked=False,
            ),
            pdc.SerieParam(
                name="Low",
                color=self.COLOR_LOW,
                data="low",
                type="bar",
                y_axis="left",
                is_stacked=False,
            ),
        ]

        chart = pdc.PandasChart(
            df=data.df_history,
            current=current_checks,
            series=series,
            width=80,
            height=70,
            pdf=self,
            font_size=6,
            title="Weekly Historical Medium & Low Failed Checks",
        )
        chart_max = data.df_history[["medium", "low"]].max().max() * 1.2
        chart.axis["left"].min = 0
        chart.axis["left"].max = (int(chart_max / 100) + 1) * 100
        chart.param.spacing = 0.60
        chart.param.x_label_step = 4
        chart.generate()

    # *************************************************
    #
    # *************************************************
    def accounts_section(self, data: ReportCompiledData):
        """Fill the Standard Information Section"""

        self.section_title("**Account Summary**")

        columns = [
            pdt.ColumnParam(name="Id", width=20, data="AwsAccountId", align="L", merge=False),
            pdt.ColumnParam(
                name="Account Name",
                width=30,
                data="AccountName",
                align="L",
                text_trim=True,
            ),
            pdt.ColumnParam(
                name="Score",
                width=10,
                data="ScorePercent",
                color_fg="ScoreColor",
                text_format="{:,.1f}%",
                align="C",
                footer="mean",
            ),
            pdt.ColumnParam(
                name="Critical",
                width=10,
                data="Critical",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Controls",
            ),
            pdt.ColumnParam(
                name="High",
                width=10,
                data="High",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Controls",
            ),
            pdt.ColumnParam(
                name="Medium",
                width=10,
                data="Medium",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Controls",
            ),
            pdt.ColumnParam(
                name="Low",
                width=10,
                data="Low",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Controls",
            ),
            #
            pdt.ColumnParam(
                name="Critical",
                width=10,
                data="FindingsCritical",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Checks",
            ),
            pdt.ColumnParam(
                name="High",
                width=10,
                data="FindingsHigh",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Checks",
            ),
            pdt.ColumnParam(
                name="Medium",
                width=10,
                data="FindingsMedium",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Checks",
            ),
            pdt.ColumnParam(
                name="Low",
                width=10,
                data="FindingsLow",
                text_format="{:,.0f}",
                align="C",
                footer="sum",
                group="Failed Checks",
            ),
        ]

        pdt.PandasTable(df=data.df_accounts, columns=columns, pdf=self, font_size=6).generate()

    # *************************************************
    #
    # *************************************************
    def controls_section(self, data: ReportCompiledData):
        """Fill the Controls  summary Information Section"""

        self.section_title(f"**List of Controls for {data.standard_short}**")

        columns = [
            pdt.ColumnParam(name="Id", width=20, data="ControlId", align="L"),
            pdt.ColumnParam(
                name="Title",
                width=100,
                data="Title",
                align="L",
                text_trim=True,
                link="RemediationUrl",
            ),
            pdt.ColumnParam(
                name="Status",
                width=20,
                data="Status",
                color_fg="StatusColor",
                align="C",
            ),
            pdt.ColumnParam(
                name="Severity",
                width=20,
                data="SeverityRating",
                color_fg="SeverityColor",
                align="C",
            ),
            pdt.ColumnParam(name="Failed Check", width=20, data="Failed_Check", align="C"),
        ]

        pdt.PandasTable(df=data.df_controls, columns=columns, pdf=self, font_size=6).generate()

    # *************************************************
    #
    # *************************************************
    def top_findings_section(self, data: ReportCompiledData):
        """Fill the Controls  summary Information Section"""

        self.section_title("**List of Top Failed Checks**")

        columns = [
            pdt.ColumnParam(
                name="Account Name",
                width=30,
                data="AwsAccountName",
                align="C",
                text_trim=True,
            ),
            pdt.ColumnParam(name="Region", width=20, data="Region", align="C"),
            pdt.ColumnParam(
                name="Severity",
                width=15,
                data="SeverityL",
                color_fg="SeverityColor",
                align="C",
            ),
            pdt.ColumnParam(
                name="Started",
                width=20,
                data="Started",
                color_fg="SeverityColor",
                align="C",
            ),
            pdt.ColumnParam(name="Workflow", width=10, data="WorkflowState", align="C"),
            pdt.ColumnParam(name="Note", width=30, data="WorkflowNote", align="L", text_trim=True),
            pdt.ColumnParam(name="Res Type", width=20, data="ResType", align="L", text_trim=True),
            pdt.ColumnParam(name="Res Name", width=30, data="ResName", align="L", text_trim=True),
            pdt.ColumnParam(
                name="Title",
                width=80,
                data="Title",
                align="L",
                text_trim=True,
                link="RemediationUrl",
            ),
        ]

        pdt.PandasTable(df=data.df_findings_top, columns=columns, pdf=self, font_size=6).generate()

    # *************************************************
    #
    # *************************************************
    def suppressed_section(self, data: ReportCompiledData):
        """Fill the Suppressed Findings Information Section"""

        self.section_title("**Suppressed Findings**")

        gb_controls = data.df_suppressed.sort_values(by=["ControlId", "AccountName"]).groupby(
            "ControlId"
        )

        for _control_id, df in gb_controls:
            control_title = df.iloc[0]["Title"]
            control_ressource_type = df.iloc[0]["ResType"]

            remediation = df.iloc[0]["Remediation"]
            remediation = (
                ast.literal_eval(remediation) if isinstance(remediation, str) else remediation
            )
            control_url = (
                remediation.get("Recommendation", {}).get("Url", "")
                if isinstance(remediation, dict)
                else ""
            )

            columns = [
                pdt.ColumnParam(name="Account Name", width=30, data="AccountName", align="L"),
                pdt.ColumnParam(name="Region", width=20, data="Region", align="L"),
                pdt.ColumnParam(
                    name=control_ressource_type,
                    width=70,
                    data="ResName",
                    align="L",
                    text_trim=True,
                ),
                pdt.ColumnParam(
                    name="Reason",
                    width=70,
                    data="WorkflowNote",
                    align="L",
                    text_trim=True,
                ),
            ]

            self.sub_title(f"**{control_title}**)", link=control_url)

            pdt.PandasTable(df=df, columns=columns, pdf=self, font_size=6).generate()
            self.ln(2)

    # *************************************************
    #
    # *************************************************
    def compile_data(self, dfs: dict[pd.DataFrame], standard_arn: str) -> ReportCompiledData:
        """Compile the data for the report"""

        df_standards = dfs["standards"]
        df_standards = df_standards[df_standards.index == standard_arn]

        if len(df_standards.index) == 0:
            print(f"No standard found for {standard_arn}")
            return
        s_standard = df_standards.iloc[0]

        # --------------------------------------
        # Compile Account level results
        # --------------------------------------

        df_standards_results = dfs["standards_results"]

        df_standards_results = df_standards_results[
            df_standards_results.index.get_level_values("Standards") == standard_arn
        ]
        print(f"Found {len(df_standards_results.index)} accounts results")

        df_standards_results = df_standards_results.reset_index().copy()
        df_standards_results["ScorePercent"] = df_standards_results["Score"] * 100
        df_standards_results["ScoreColor"] = df_standards_results["Score"].apply(
            self.get_score_color
        )

        # --------------------------------------
        # Compile controls at the organization level
        # --------------------------------------
        df_controls = dfs["controls"]
        df_controls = df_controls[df_controls["Standards"] == standard_arn]
        print(f"Found {len(df_controls.index)} controls")

        df_controls_results = dfs["controls_results"]
        df_controls_results = df_controls_results[
            df_controls_results.index.get_level_values("Standards") == standard_arn
        ]
        df_controls_results = df_controls_results.reset_index().copy()
        print(f"Found {len(df_controls_results.index)} controls results")

        gb_controls = df_controls_results.groupby("StandardsControl")
        df_controls_gb = gb_controls.agg(
            {
                "ControlId": "max",
                "CheckCount": "sum",
                "CheckPass": "sum",
                "CheckFail": "sum",
                "SeverityRating": "max",
            }
        ).reset_index()
        df_controls_gb["Pass"] = df_controls_gb["CheckPass"] == df_controls_gb["CheckCount"]
        df_controls_gb["Status"] = "Failed"
        df_controls_gb.loc[df_controls_gb["Pass"], "Status"] = "Passed"
        df_controls_gb["Failed_Check"] = df_controls_gb.apply(
            lambda x: f"{x['CheckFail']} of {x['CheckCount']}", axis=1
        )

        # Set severity color
        status_mapping = {"Passed": self.COLOR_PASSED, "Failed": self.COLOR_FAILED}
        df_controls_gb["StatusColor"] = df_controls_gb["Status"].map(status_mapping)

        # Set severity color
        severity_mapping = {
            "CRITICAL": self.COLOR_CRITICAL,
            "HIGH": self.COLOR_HIGH,
            "MEDIUM": self.COLOR_MEDIUM,
            "LOW": self.COLOR_LOW,
        }
        df_controls_gb["SeverityColor"] = df_controls_gb["SeverityRating"].map(severity_mapping)

        # Add control title
        df_controls_gb = df_controls_gb.merge(
            df_controls[["StandardsControl", "Title", "RemediationUrl"]],
            on="StandardsControl",
            how="left",
        )

        ctrl_total_pass = df_controls_gb["Pass"].sum()
        ctrl_total = len(df_controls_gb.index)
        ctrl_score = ctrl_total_pass / ctrl_total

        # print(df_controls_gb)

        print(f"Total Controls: {ctrl_total} - Total Pass: {ctrl_total_pass} - Score: {ctrl_score}")

        # --------------------------------------
        # Compile Findings
        # --------------------------------------
        df_findings = dfs["findings"]
        df_findings["Remediation"] = df_findings["Remediation"].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        df_findings = df_findings[df_findings["Standards"] == standard_arn]

        df_suppressed = df_findings[df_findings["WorkflowStatus"] == "SUPPRESSED"]

        print(f"Total Suppressed Findings: {len(df_suppressed.index)}")

        # list the top XX findings by severity
        df_top_findings = (
            df_findings[df_findings["SeverityN"] > 0]
            .sort_values(by=["SeverityN", "WorkflowStatus"], ascending=[False, True])
            .head(40)
            .copy()
        )
        df_top_findings["SeverityColor"] = df_top_findings["SeverityL"].map(severity_mapping)
        df_top_findings["Started"] = df_top_findings["FirstObservedAt"].str[:10]
        df_top_findings["RemediationUrl"] = df_top_findings["Remediation"].apply(
            lambda x: x.get("Recommendation", {}).get("Url", "")
        )

        # Summary of findings by severity
        df_findings_with_control = df_findings[
            [
                "StandardsControl",
                "WorkflowState",
                "RecordState",
                "WorkflowStatus",
                "passed",
            ]
        ]
        df_findings_with_control = df_findings_with_control.merge(
            df_controls[["StandardsControl", "SeverityRating"]],
            on="StandardsControl",
            how="left",
        )
        df_findings_with_control["suppressed"] = (
            df_findings_with_control["WorkflowStatus"] == "SUPPRESSED"
        )

        # -------------------------------------------
        # Summary of findings by severity
        # -------------------------------------------
        gb_summary = df_controls_gb.groupby("SeverityRating")
        df_findings_summary = gb_summary.agg(
            {"CheckCount": "sum", "CheckPass": "sum", "CheckFail": "sum"}
        ).reset_index()

        df_findings_summary["passed_percent"] = (
            df_findings_summary["CheckPass"] / df_findings_summary["CheckCount"]
        )

        df_findings_summary["SeverityColor"] = df_findings_summary["SeverityRating"].map(
            severity_mapping
        )
        df_findings_summary["TextColor"] = df_findings_summary["SeverityColor"].apply(
            lambda x: self.SECTION_TITLE_FG
        )
        df_findings_summary["SeverityOrder"] = df_findings_summary["SeverityRating"].apply(
            lambda x: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].index(x)
        )
        df_findings_summary = df_findings_summary.sort_values(by=["SeverityOrder"])

        print(df_findings_summary)

        # --------------------------------------
        # Historical data
        # --------------------------------------
        if "history" in dfs and (dfs["history"] is not None):
            df_history = dfs["history"]

            if "short" in df_history.columns:
                df_history = df_history[df_history["short"] == s_standard["Short"]]

            gb_history = df_history.groupby("date")
            df_history = gb_history.agg(
                {
                    "critical": "sum",
                    "high": "sum",
                    "medium": "sum",
                    "low": "sum",
                }
            )

            df_history["score_min"] = gb_history["score"].min() * 100
            df_history["score_max"] = gb_history["score"].max() * 100
            df_history["score_mean"] = gb_history["score"].mean() * 100

            date_count = len(df_history.index)
            print(f"Found {date_count} historical data")

            if date_count > 21:
                # Resampling to weekly
                df_history.index = pd.to_datetime(df_history.index)
                df_history = df_history.resample("W", label="left").mean()
                df_history.index = df_history.index.strftime("%Y-%m-%d")

                print(f"Resampled to {len(df_history.index)} weekly data")

        else:
            df_history = None

        return ReportCompiledData(
            standard_short=s_standard["Short"],
            standard_name=s_standard["Name"],
            standard_description=s_standard["Description"],
            standard_control_count=int(s_standard["ControlsCount"]),
            standard_score=ctrl_score,
            standard_total=ctrl_total,
            standard_pass=ctrl_total_pass,
            accounts_mean_score=df_standards_results["Score"].mean(),
            df_accounts=df_standards_results,
            df_controls=df_controls_gb,
            df_suppressed=df_suppressed,
            df_findings_top=df_top_findings,
            df_findings_summary=df_findings_summary,
            df_history=df_history,
        )

    # *************************************************
    #
    # *************************************************
    def generate(self, dfs: dict[pd.DataFrame], standard_arn: str):
        """Return Report from the notes in Pdf format"""

        print(f"Generate Report for standard {standard_arn}")

        # import o7util.pandas
        # o7util.pandas.dfs_to_excel(dfs=dfs, filename="tests/sechub-data-xx.xlsx")

        data = self.compile_data(dfs, standard_arn)

        self.title = f"{self.title} - {data.standard_short}"
        self.alias_nb_pages()
        self.add_page()

        self.report_head()

        start_y = self.get_y()
        self.standard_results(data=data)

        # print(f'L Marging: {self.l_margin} - R Margin: {self.r_margin}')
        # print(f'T Margin: {self.t_margin} - B Margin: {self.b_margin}')

        self.set_xy(100, start_y)
        self.standard_info(data=data)
        self.ln()
        self.checks_summary_table(data=data)
        self.ln(15)
        self.checks_historic_charts(data=data)

        self.add_page()
        self.accounts_section(data=data)
        self.ln()
        self.accounts_historic_chart(data=data)
        self.add_page(orientation="L")
        self.top_findings_section(data=data)
        self.add_page()
        self.controls_section(data=data)
        self.add_page(orientation="P")
        self.suppressed_section(data=data)

        return self
