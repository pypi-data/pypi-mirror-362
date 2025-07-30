"""Module to Reports in PDF Format"""

import datetime
import importlib.resources as pkg_resources
import logging
import os

import fpdf

import o7pdf
from o7pdf.colors import PdfColors

logger = logging.getLogger(__name__)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)

# https://py-pdf.github.io/fpdf2/fpdf/fpdf.html


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class Template(fpdf.FPDF):  # pylint: disable=too-many-instance-attributes
    """Class temaplate to generate PDF Report"""

    filename: str = "report.pdf"

    TEXT_FG = PdfColors.N800

    SECTION_TITLE_BG = PdfColors.ALT
    SECTION_TITLE_FG = PdfColors.N20

    SUB_TITLE_BG = PdfColors.N40
    SUB_TITLE_FG = PdfColors.MAIN

    # *************************************************
    #
    # *************************************************
    def __init__(  # pylint: disable=too-many-arguments
        self,
        filename: str = "report.pdf",
        title: str = "Template Report",
        username: str = None,
        updated: str = None,
        orientation: str = "portrait",
        logo: str = None,
    ):
        super().__init__(orientation=orientation, unit="mm", format="letter")

        self.res_dir = pkg_resources.files("o7pdf").joinpath("res")

        self.add_font(
            family="OpenSans",
            style="",
            fname=os.path.join(self.res_dir, "OpenSans-Regular.ttf"),
        )
        self.add_font(
            family="OpenSans",
            style="B",
            fname=os.path.join(self.res_dir, "OpenSans-Bold.ttf"),
        )
        self.add_font(
            family="OpenSans",
            style="I",
            fname=os.path.join(self.res_dir, "OpenSans-Italic.ttf"),
        )
        self.add_font(
            family="OpenSans",
            style="BI",
            fname=os.path.join(self.res_dir, "OpenSans-BoldItalic.ttf"),
        )
        self.set_font("OpenSans", size=10)

        self.filename = filename
        self.title = title
        self.username = username
        self.updated = (
            datetime.datetime.fromisoformat(str(updated)).strftime("%Y-%m-%d") if updated else ""
        )
        self.subtitle = None
        self.date: str = datetime.date.today().strftime("%Y-%m-%d")

        # Setting resurces
        self.logo = os.path.join(self.res_dir, logo) if logo else None

    # *************************************************
    #
    # *************************************************
    def save(self):
        """Save the PDF Report"""

        dir_name = os.path.dirname(self.filename)

        if len(dir_name) > 1 and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        self.output(self.filename)

        print(f"PDF Report saved to: {self.filename}")

    # *************************************************
    #
    # *************************************************
    def cell(self, text_trim: bool = False, **kwargs):  # pylint: disable=arguments-differ
        """Cell with support for text trim"""

        if "txt" in kwargs:
            # DeprecationWarning: The parameter "txt" has been renamed to "text" in fpdf2 2.7.6
            raise ValueError("txt is not supported, use text instead")

        if text_trim:
            text = kwargs.get("text", "")
            cell_width = kwargs.get("w", 0)
            text_width = self.get_string_width(text)
            if text_width > cell_width:
                kwargs["text"] = text[: int(cell_width / text_width * len(text))]

        try:
            super().cell(**kwargs)
        except Exception as exc:
            print("Error in cell method:", exc)
            print(kwargs)
            raise exc

    # *************************************************
    #
    # *************************************************
    def header(self):
        """Format Header"""

        # Logo
        with self.local_context():
            title = self.title if self.subtitle is None else f"{self.title} - {self.subtitle}"
            self.set_font("OpenSans", size=6)
            self.set_text_color(**self.TEXT_FG)
            self.set_draw_color(**self.SUB_TITLE_BG)
            self.set_line_width(0.1)
            self.cell(
                w=0,
                text=f"**{self.date}**",
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
                border="",
                markdown=True,
            )
            self.cell(
                w=0,
                text=title,
                new_x="LMARGIN",
                new_y="TOP",
                align="L",
                border="",
                markdown=True,
            )

            self.set_xy((-15.0) - self.r_margin, self.t_margin)
            self.set_font("OpenSans", size=6)
            self.cell(
                w=None,
                h=3,
                text="powered by",
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border="",
                markdown=True,
            )

            # self.set_y(self.get_y() - 0.1)
            self.image(
                os.path.join(self.res_dir, "o7-conseils-rect.svg"),
                w=13,
                link="https://o7conseils.com",
            )

            line_y = self.t_margin + 7
            self.line(x1=self.l_margin, y1=line_y, x2=self.epw + self.l_margin, y2=line_y)

        self.set_x(self.l_margin)
        self.set_y(self.t_margin + 8)

    # *************************************************
    #
    # *************************************************
    def footer(self):
        """Format Footer"""
        # Position at 1.5 cm from bottom

        with self.local_context():
            self.set_text_color(**self.TEXT_FG)
            self.set_font("OpenSans", size=6)
            # Page number
            self.set_y(-15)

            self.cell(
                w=0,
                h=10,
                text=f"v{o7pdf.__version__}",
                border=0,
                align="L",
                new_x="LEFT",
                new_y="NEXT",
                markdown=True,
            )

            if self.username:
                self.cell(
                    w=0,
                    h=10,
                    text=f"Generated by: **{self.username}**",
                    border=0,
                    align="L",
                    new_x="LEFT",
                    new_y="NEXT",
                    markdown=True,
                )

            if self.updated:
                self.set_y(-12)
                self.cell(
                    w=0,
                    h=10,
                    text=f"Updated: **{self.updated}**",
                    border=0,
                    align="L",
                    new_x="RIGHT",
                    new_y="NEXT",
                    markdown=True,
                )

            self.set_y(-15)
            self.cell(
                w=0,
                h=10,
                text="Page " + str(self.page_no()) + " / {nb}",
                border=0,
                align="R",
                new_x="RIGHT",
                new_y="TOP",
            )

    # *************************************************
    #
    # *************************************************
    def report_head(self):
        """Top of first page"""

        page_start = self.get_y()

        with self.local_context():
            self.set_text_color(**self.TEXT_FG)

            # self.image(
            #     os.path.join(self.res_dir, 'rbc-wm-logo-fr.png'),
            #     x = self.l_margin, y = page_start + 3.5, h=9.5,
            #     alt_text='TBD', link='https://www....')

            self.set_xy(self.l_margin + self.epw * 0.2, page_start)
            self.set_font("OpenSans", size=14)
            self.start_section(name=self.title, level=0)
            self.cell(
                w=self.epw * 0.7,
                h=16,
                text=f"**{self.title}** ",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="L",
                border=0,
                markdown=True,
            )

        self.set_xy(self.l_margin, page_start + 18)

    # *************************************************
    #
    # *************************************************
    def section_title(self, title: str):
        """Format Section Title"""

        with self.local_context():
            self.set_font("OpenSans", size=12)

            self.set_draw_color(**self.SECTION_TITLE_BG)
            self.set_fill_color(**self.SECTION_TITLE_BG)
            self.set_text_color(**self.SECTION_TITLE_FG)

            self.ln(3)
            self.set_x(self.l_margin)
            self.start_section(name=title, level=1)
            self.cell(
                w=self.epw,
                h=self.font_size * 1.75,
                text=title,
                fill=True,
                new_x="LMARGIN",
                new_y="NEXT",
                align="C",
                border="",
                markdown=True,
            )
            self.ln(5)

    # *************************************************
    #
    # *************************************************
    def sub_title(self, title: str, link: str = None):
        """Format Section Title"""

        with self.local_context():
            self.set_font("OpenSans", size=8)

            self.set_draw_color(**self.SUB_TITLE_BG)
            self.set_fill_color(**self.SUB_TITLE_BG)
            self.set_text_color(**self.SUB_TITLE_FG)

            self.set_x(self.l_margin)
            # https://py-pdf.github.io/fpdf2/fpdf/fpdf.html#fpdf.fpdf.FPDF.cell
            self.cell(
                w=self.epw,
                h=self.font_size * 1.5,
                text=f"  {title}",
                fill=True,
                new_x="LMARGIN",
                new_y="NEXT",
                align="L",
                border="",
                markdown=True,
                link=link,
            )
            self.ln(1)
