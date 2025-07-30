"""Module to Reports in PDF Format"""

import dataclasses

import pandas as pd
import pandas.api.types as pdtypes

from o7pdf.pandas_basic import INFO_TO_SVG, PandasBasic, Rectangle


@dataclasses.dataclass
class ColumnParam:  # pylint: disable=too-many-instance-attributes
    """Parameters for a column"""

    name: str = ""
    data: str = "no-data"  # data column
    width: float = 10.0

    text_format: str = "{}"
    cell_format: str = ""
    outofgrid: bool = False
    text_trim: bool = False  # trim text if it does not fit in the cell
    align: str = "C"

    link: str = None  # data column for an cell link
    color_fg: str = None  # data column to set color of the text
    color_bg: str = None  # data column to set color of the cell

    group: str = ""  # group columns, the value will be displayed in the header
    footer: str = ""  # sum, mean
    merge: bool = False  # merge cells with the same values in the column


# *************************************************
#
# *************************************************
class PandasTable(PandasBasic):  # pylint: disable=too-many-instance-attributes
    """Class to generate a Pandas Dataframe in a PDF Report"""

    def __init__(self, columns: list[ColumnParam], orientation: str = "", **kwargs):
        super().__init__(**kwargs)

        self.columns: list[ColumnParam] = columns

        self.row_height: float = None
        self.col_width_max: float = None

        self.is_group_header: bool = False
        self.is_footer: bool = False

        self.table_rect: Rectangle = Rectangle()
        self.data_rect: Rectangle = Rectangle()
        self.foorter_rect: Rectangle = Rectangle()
        self.grid_rect: Rectangle = Rectangle()

        self.merge_borders: list[Rectangle] = []
        self.group_borders: list[Rectangle] = []

        self.row_oriented: bool = orientation == "row"

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size=self.font_size)
            self.row_height = self.pdf.font_size * 1.75

        self.is_group_header = any(len(column.group) > 0 for column in self.columns)
        self.is_footer = any(len(column.footer) > 0 for column in self.columns)

    # *************************************************
    #
    # *************************************************
    def reset_borders(self):
        """Reset the table borders"""

        self.foorter_rect: Rectangle = Rectangle()
        self.grid_rect: Rectangle = Rectangle()

        self.merge_borders: list[Rectangle] = []
        self.group_borders: list[Rectangle] = []

    # *************************************************
    #
    # *************************************************
    def prepare(self, count: int = None):
        """Generate the table inside the PDF Report"""

        self.reset_borders()

        self.col_width_max = max(column.width for column in self.columns)
        row_count = max(len(self.df.index) if count is None else count, 1)

        self.data_rect.x = self.original_x
        self.table_rect.x = self.data_rect.x

        if self.row_oriented:
            self.data_rect.x = self.data_rect.x + self.col_width_max
            self.data_rect.w = self.col_width_max * len(self.df.index)
            self.table_rect.w = self.data_rect.w + self.col_width_max
        else:
            self.data_rect.w = sum(
                column.width if not column.outofgrid else 0 for column in self.columns
            )
            self.table_rect.w = self.data_rect.w

        self.table_rect.y = self.pdf.get_y()
        if self.title:
            self.table_rect.y = self.table_rect.y + self.row_height

        if self.row_oriented:
            self.data_rect.y = self.table_rect.y
        else:
            self.data_rect.y = self.table_rect.y + self.row_height

        if self.is_group_header:
            self.data_rect.y += self.row_height

        if self.row_oriented:
            self.data_rect.h = len(self.columns) * self.row_height
        else:
            self.data_rect.h = row_count * self.row_height

        self.table_rect.h = self.data_rect.h + self.row_height
        if self.title:
            self.table_rect.h = self.table_rect.h + self.row_height
        if self.is_group_header:
            self.table_rect.h += self.row_height

        self.foorter_rect.x = self.data_rect.x
        self.foorter_rect.y = self.data_rect.y + self.data_rect.h
        self.foorter_rect.w = self.data_rect.w
        self.foorter_rect.h = 0
        if self.is_footer:
            self.foorter_rect.h = self.row_height
            self.table_rect.h += self.row_height

        self.grid_rect = Rectangle(
            x=self.data_rect.x,
            y=self.data_rect.y,
            w=self.data_rect.w,
            h=self.data_rect.h,
        )

        return self

    def get_height(self):
        """Get the table height"""
        return self.table_rect.h

    # *************************************************
    #
    # *************************************************
    def get_rows_on_page(self):
        """Get the number of rows that can fit rest of the page"""

        rows_left = (self.pdf.eph - (self.pdf.get_y() - self.pdf.t_margin + 10.0)) / self.row_height
        rows_left = int(rows_left) - 1
        rows_left = rows_left - 1 if self.is_group_header else rows_left
        rows_left = rows_left - 1 if self.is_footer else rows_left
        rows_left = max(0, rows_left)

        return rows_left

    # *************************************************
    #
    # *************************************************
    def generate(self):
        """Generate the table inside the PDF Report"""

        self.prepare()

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size=self.font_size)
            self.pdf.set_auto_page_break(False)

            self.draw_title()
            row_printed = 0
            first_loop = False
            total_rows = len(self.df.index) if not self.row_oriented else len(self.columns)

            while (row_printed < total_rows) | (not first_loop):
                first_loop = True

                row_on_page = self.get_rows_on_page()
                if row_on_page == 0:
                    self.pdf.add_page(orientation=self.pdf.cur_orientation)
                    continue

                row_on_page = min(row_on_page, total_rows - row_printed)

                self.prepare(count=row_on_page)
                self.draw_group_header()
                self.draw_header()

                self.draw_data(start=row_printed, count=row_on_page)

                self.draw_gridlines(count=row_on_page)

                self.draw_borders([self.data_rect], self.LINE_COLOR)
                self.draw_borders(self.group_borders, self.LINE_COLOR)
                self.draw_borders(self.merge_borders)

                row_printed = row_printed + row_on_page

            self.draw_footer()

        self.pdf.set_xy(self.table_rect.x, self.table_rect.y + self.table_rect.h)

        return self

    # *************************************************
    #
    # *************************************************
    def draw_title(self):
        """Draw the table title"""

        if not self.title:
            return

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.TITLE_BG)
            self.pdf.set_fill_color(**self.TITLE_BG)
            self.pdf.set_text_color(**self.TITLE_FG)
            self.pdf.set_line_width(0.2)

            self.pdf.set_xy(self.table_rect.x, self.table_rect.y - self.row_height)
            self.pdf.cell(
                w=self.table_rect.w,
                h=self.row_height,
                text=f"**{self.title}**",
                align="L",
                border=1,
                markdown=True,
                fill=True,
            )

    # *************************************************
    #
    # *************************************************
    def draw_group_header(self):
        """Draw the table header"""

        if self.row_oriented:
            return

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.HEADER_BG)
            self.pdf.set_fill_color(**self.HEADER_BG)
            self.pdf.set_text_color(**self.HEADER_FG)
            self.pdf.set_line_width(0.2)

            group_x = self.table_rect.x
            group_w = 0
            group_h = self.foorter_rect.y - self.table_rect.y

            for i, column in enumerate(self.columns):
                group = column.group
                width = column.width
                group_w = group_w + width

                if len(group) > 0:
                    if (i < len(self.columns) - 1) and (group == self.columns[i + 1].group):
                        continue

                    self.pdf.set_xy(group_x, self.table_rect.y)
                    self.pdf.cell(
                        w=group_w,
                        h=self.row_height,
                        text=group,
                        align="C",
                        border=1,
                        markdown=False,
                        fill=True,
                    )

                    self.group_borders.append(
                        Rectangle(x=group_x, y=self.table_rect.y, w=group_w, h=group_h)
                    )

                group_x = group_x + group_w
                group_w = 0

    # *************************************************
    #
    # *************************************************
    def draw_header(self):
        """Draw the table header"""

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.HEADER_BG)
            self.pdf.set_fill_color(**self.HEADER_BG)
            self.pdf.set_text_color(**self.HEADER_FG)
            self.pdf.set_line_width(0.2)

            header_y = self.table_rect.y
            if self.is_group_header:
                header_y += self.row_height

            self.pdf.set_xy(self.table_rect.x, header_y)

            new_x = "RIGHT"
            new_y = "TOP"
            if self.row_oriented:
                new_x = "LEFT"
                new_y = "NEXT"

            for column in self.columns:
                if column.outofgrid and len(column.name) == 0:
                    break

                self.pdf.cell(
                    w=column.width,
                    h=self.row_height,
                    new_x=new_x,
                    new_y=new_y,
                    text=column.name,
                    align="C",
                    border=1,
                    markdown=False,
                    fill=True,
                )

    # *************************************************
    #
    # *************************************************
    def draw_footer(self):
        """Draw the table header"""

        if self.row_oriented:
            return

        with self.pdf.local_context():
            self.pdf.set_fill_color(r=255, g=-1, b=-1)
            self.pdf.set_text_color(r=0)

            footer_x = self.data_rect.x
            footer_y = self.data_rect.y + self.data_rect.h

            for column in self.columns:
                footer = column.footer
                width = column.width

                if len(footer) > 0:
                    data = column.data
                    text_format = column.text_format

                    value = " "
                    if footer == "sum":
                        value = self.df[data].sum()
                    if footer == "mean":
                        value = self.df[data].mean()

                    txt = text_format.format(value)

                    self.pdf.set_xy(footer_x, footer_y)
                    self.pdf.cell(
                        w=width,
                        h=self.row_height,
                        text=f"**{txt}**",
                        align=column.align,
                        border=0,
                        markdown=True,
                        fill=False,
                    )

                footer_x = footer_x + width

    # *************************************************
    #
    # *************************************************
    def format_data_cell(
        self, column: ColumnParam, cell: Rectangle, value: any, maximum: float = 0, total: float = 0
    ) -> str:
        """Aplly cell background format and return the cell text"""

        if pd.isna(value):
            txt = "-"
        else:
            txt = column.text_format.format(value)

        if column.cell_format == "UNDER":
            self.draw_bar_under(value=value, cell=cell)

        elif column.cell_format == "OVER":
            self.draw_bar_over(value=value, cell=cell)

        elif column.cell_format == "WEIGHT":
            self.draw_progress(value=value, cell=cell, maximum=maximum)

        elif column.cell_format == "WEIGHT_SUM":
            self.draw_progress(value=value, cell=cell, maximum=total)

        elif column.cell_format == "DELTA":
            if value == 0:
                txt = ""

        elif column.cell_format == "DELTA_PLUS":
            if value > 0:
                txt = f"+{txt}"
            elif value == 0:
                txt = ""

        elif column.cell_format == "INFO":
            self.draw_info(infos=value, cell=cell)
            txt = ""

        return txt

    # *************************************************
    #
    # *************************************************
    def draw_data(self, start: int = None, count: int = None):  # disable=too-many-locals
        """Draw the table header"""

        row_count = len(self.df.index) if count is None else count
        first_row = 0 if start is None else start
        last_row = first_row + row_count

        with self.pdf.local_context():
            self.pdf.set_fill_color(**self.LINE_COLOR)
            self.pdf.set_text_color(r=0)

            date_cell = Rectangle(x=self.data_rect.x, y=self.data_rect.y, w=0, h=self.row_height)

            offset_col = 0
            for i, column in enumerate(self.columns):
                date_cell.w = column.width
                date_cell.h = self.row_height
                date_cell.y = self.data_rect.y

                col_max = (
                    self.df[column.data].max(skipna=True)
                    if pdtypes.is_numeric_dtype(self.df[column.data])
                    else 0
                )
                col_total = (
                    self.df[column.data].sum(skipna=True)
                    if pdtypes.is_numeric_dtype(self.df[column.data])
                    else 0
                )

                if self.row_oriented:
                    df_table = self.df
                else:
                    df_table = self.df[first_row:last_row]

                for j, row_index in enumerate(df_table.index):
                    if self.row_oriented:
                        date_cell.w = self.col_width_max
                        date_cell.x = self.data_rect.x + (j * self.col_width_max)
                        date_cell.y = self.data_rect.y + (i * self.row_height)
                    else:
                        date_cell.x = self.data_rect.x + offset_col

                    value = df_table.loc[row_index, column.data]

                    if column.merge:
                        if j == 0:
                            self.grid_rect.x = date_cell.x + column.width
                            self.grid_rect.w = self.data_rect.w - (
                                self.grid_rect.x - self.data_rect.x
                            )

                        if (j + 1) < row_count and value == df_table.iloc[j + 1][column.data]:
                            date_cell.h = date_cell.h + self.row_height
                            continue

                        x_offset = date_cell.x - self.data_rect.x

                        self.merge_borders.append(
                            Rectangle(
                                x=date_cell.x,
                                y=date_cell.y,
                                w=self.data_rect.w - x_offset,
                                h=date_cell.h,
                            )
                        )

                    txt = self.format_data_cell(
                        column=column, cell=date_cell, value=value, maximum=col_max, total=col_total
                    )

                    with self.pdf.local_context():
                        fill = False

                        if column.color_fg:
                            color_fg = df_table.loc[row_index, column.color_fg]
                            if isinstance(color_fg, dict):
                                self.pdf.set_text_color(**color_fg)

                        if column.color_bg:
                            color_bg = df_table.loc[row_index, column.color_bg]
                            if isinstance(color_bg, dict):
                                self.pdf.set_fill_color(**color_bg)
                                fill = True

                        link = df_table.loc[row_index, column.link] if column.link else None

                        if link and not isinstance(link, str):
                            link = None

                        self.pdf.set_xy(x=date_cell.x, y=date_cell.y)
                        self.pdf.cell(
                            w=date_cell.w,
                            h=date_cell.h,
                            text=txt,
                            text_trim=column.text_trim,
                            align=column.align,
                            border=0,
                            markdown=False,
                            fill=fill,
                            link=link,
                        )

                    date_cell.y = date_cell.y + date_cell.h
                    date_cell.h = self.row_height

                offset_col = offset_col + column.width

    # *************************************************
    #
    # *************************************************
    def draw_gridlines(self, count: int = None):
        """Draw the table gridlines"""

        row_count = len(self.df.index) if count is None else count

        line = Rectangle(x=self.grid_rect.x, y=self.grid_rect.y, w=self.grid_rect.w, h=0)

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.LINE_COLOR)
            self.pdf.set_line_width(0.1)
            self.pdf.set_dash_pattern(dash=0.3, gap=1, phase=0)
            for _i in range(row_count):
                self.pdf.line(x1=line.x, y1=line.y, x2=line.x + line.w, y2=line.y)
                line.y = line.y + self.row_height

    # *************************************************
    #
    # *************************************************
    def draw_bar_under(self, value: float, cell: Rectangle):
        """Insert a bar under the value"""

        if value < 1.0:
            bar_offset = max(cell.w * value, 0)

            rect = Rectangle(
                x=cell.x + bar_offset,
                y=cell.y,
                w=cell.w - bar_offset,
                h=self.row_height * 0.7,
            )
            rect.y = rect.y + ((self.row_height - rect.h) / 2)

            with self.pdf.local_context():
                self.pdf.set_fill_color(**self.UNDER_RED)
                self.pdf.rect(style="F", **rect.__dict__)

    # *************************************************
    #
    # *************************************************
    def draw_bar_over(self, value: float, cell: Rectangle):
        """Insert a bar over the value"""

        if value >= 1.0:
            value = min(value - 1, 1.0)

            rect = Rectangle(x=cell.x, y=cell.y, w=cell.w * value, h=self.row_height * 0.7)
            rect.y = rect.y + ((self.row_height - rect.h) / 2)

            with self.pdf.local_context():
                self.pdf.set_fill_color(**self.OVER_GREEN)
                self.pdf.rect(style="F", **rect.__dict__)

    # *************************************************
    #
    # *************************************************
    def draw_progress(self, value: float, cell: Rectangle, maximum: float):
        """Insert a bar over the value"""

        maximum = max(maximum, 1.0)
        value = min(value / maximum, 1.0)
        value = max(value, 0.0)

        rect = Rectangle(x=cell.x, y=cell.y, w=cell.w * value, h=self.row_height * 0.8)

        rect.y = rect.y + ((self.row_height - rect.h) / 2)

        with self.pdf.local_context():
            self.pdf.set_fill_color(**self.PROGRESS)
            self.pdf.rect(style="F", **rect.__dict__)

    # *************************************************
    #
    # *************************************************
    def draw_info(self, infos: str, cell: Rectangle):
        """Insert a bar over the value"""

        if not isinstance(infos, str):
            return

        x_pos = cell.x + (cell.w * 0.1)
        height = self.row_height * 0.8

        for info in infos:
            details = INFO_TO_SVG.get(info, None)
            if details:
                height = self.row_height * 0.8 * details["scale"]
                y_pos = (self.row_height - height) / 2 + cell.y

                self.pdf.image(
                    details["svg"],
                    x=x_pos,
                    y=y_pos,
                    h=height,
                    alt_text=details["hover"],
                )
                x_pos = height + x_pos
