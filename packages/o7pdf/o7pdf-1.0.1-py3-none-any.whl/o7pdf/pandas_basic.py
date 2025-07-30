"""Module to Reports in PDF Format"""

import dataclasses
import importlib.resources as pkg_resources
import os

import fpdf
import pandas as pd

from o7pdf.colors import PdfColors


@dataclasses.dataclass
class Rectangle:  # pylint: disable=invalid-name
    """Represents rectangle"""

    x: float = 0.0
    y: float = 0.0
    w: float = 0.0
    h: float = 0.0

    @property
    def x2(self):
        """Calculate x2"""
        return self.x + self.w

    @property
    def y2(self):
        """Calculate x2"""
        return self.y + self.h


res_dir = pkg_resources.files("o7pdf").joinpath("res")

INFO_TO_SVG = {
    "L": {"svg": os.path.join(res_dir, "lock.svg"), "scale": 1.0, "hover": "Vérouillé"},
    "N": {
        "svg": os.path.join(res_dir, "lock.svg"),
        "scale": 1.0,
        "hover": "Vérouillé sur achat",
    },
    "E": {
        "svg": os.path.join(res_dir, "file-diff.svg"),
        "scale": 0.8,
        "hover": "Équivalence de modèle",
    },
    "U": {
        "svg": os.path.join(res_dir, "clipboard2-x-fill.svg"),
        "scale": 0.8,
        "hover": "Hors modèle",
    },
    "X": {
        "svg": os.path.join(res_dir, "x-octagon.svg"),
        "scale": 0.8,
        "hover": "Sans modélisation",
    },
    "Z": {
        "svg": os.path.join(res_dir, "remove-emoji.svg"),
        "scale": 0.8,
        "hover": "Transaction non-permise",
    },
    "P": {
        "svg": os.path.join(res_dir, "question.svg"),
        "scale": 1.0,
        "hover": "Sans référence",
    },
    "O": {
        "svg": os.path.join(res_dir, "edit.svg"),
        "scale": 1.0,
        "hover": "Quantité modifiée manuellement",
    },
}


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class PandasBasic:  # pylint: disable=too-many-instance-attributes
    """Basic to draw Chart of Table from a Pandas Dataframe in a PDF Report"""

    TITLE_BG = PdfColors.N40
    TITLE_FG = PdfColors.N800
    HEADER_BG = PdfColors.N40
    HEADER_FG = PdfColors.N700
    GROUP_BORDER_COLOR = PdfColors.BM100
    LINE_COLOR = PdfColors.N700
    LINE_COLOR_BG = PdfColors.N40
    PROGRESS = PdfColors.B100

    UNDER_RED = PdfColors.R500  # Previous -> #A50021
    OVER_GREEN = PdfColors.G500  # Previous -> #33CC33

    def __init__(
        self,
        df: pd.DataFrame,
        pdf: fpdf.FPDF,
        current: pd.Series = None,
        font_size: int = 6,
        title: str = None,
    ):  # pylint: disable=too-many-arguments, too-many-positional-arguments
        self.df: pd.DataFrame = df.copy()
        self.current: pd.Series = current
        self.pdf: fpdf.FPDF = pdf
        self.title: str = title
        self.font_size: float = font_size

        self.original_x = self.pdf.get_x()
        self.original_y = self.pdf.get_y()

        if self.current is not None:
            # copy the df and append the current as the last row
            self.df.loc[self.current.name] = self.current

    # *************************************************
    #
    # *************************************************
    def prepare(self):
        """Prepare variables before the generation"""
        return self

    # *************************************************
    #
    # *************************************************
    def generate(self):
        """Generate the element in the PDF Report"""
        self.prepare()
        return self

    # *************************************************
    #
    # *************************************************
    def draw_borders(self, borders: list[Rectangle], color: dict = None):
        """Draw a list of borders"""

        if color is None:
            color = self.LINE_COLOR

        with self.pdf.local_context():
            self.pdf.set_draw_color(**color)
            self.pdf.set_line_width(0.2)
            self.pdf.set_dash_pattern(dash=0, gap=0, phase=0)
            for border in borders:
                self.pdf.rect(border.x, border.y, border.w, border.h, style="D")
