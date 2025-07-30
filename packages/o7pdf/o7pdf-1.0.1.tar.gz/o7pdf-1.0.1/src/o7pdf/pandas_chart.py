"""Module to Reports in PDF Format"""

import dataclasses
import importlib.resources as pkg_resources
from enum import Enum

import pandas as pd

from o7pdf.pandas_basic import PandasBasic, Rectangle


@dataclasses.dataclass
class ChartParam:  # pylint: disable=too-many-instance-attributes
    """Parameters the chart"""

    spacing: float = 0.5  # Spacing between the elements in percentage (0 to 1)
    x_label_step = 1  # Steps for the X label


class SerieType(Enum):
    BAR = "bar"
    LINE = "line"
    ZONE = "zone"


@dataclasses.dataclass
class SerieParam:  # pylint: disable=too-many-instance-attributes
    """Parameters for a column"""

    name: str = ""  # TBD
    data: str = "no-data"  # data column
    data_min: str = "no-data"  # data column for zone type minimum
    data_max: str = "no-data"  # data column for zone type maximum

    color: dict = None  # Color of the background
    type: SerieType = SerieType.BAR
    stack_id: int = None
    is_stacked: bool = False
    y_axis: str = "left"

    def __post_init__(self):
        if isinstance(self.type, str):
            try:
                self.type = SerieType(self.type)
            except ValueError as error:
                raise ValueError(
                    f"Invalid type: {self.type}. Must be one of {list(SerieType)}"
                ) from error
        elif not isinstance(self.type, SerieType):
            raise ValueError(f"Invalid type: {self.type}. Must be one of {list(SerieType)}")


@dataclasses.dataclass
class Axis:  # pylint: disable=too-many-instance-attributes
    """Values for the Axis, used for internal calculations"""

    active: bool = False
    title: str = ""  # TBD
    width: float = 5
    height: float = None
    min: float = None
    max: float = None
    step: float = None
    format: str = "{:,.0f}"
    color: dict = None
    grid: bool = False  # TBD, alway on for now
    position: str = "left"
    visible: bool = True  # TBD, alway visible for now

    @property
    def value_to_height(self) -> float:
        """Calculate value to height ratio"""
        return self.height / (self.max - self.min)

    def value_to_offset(self, value) -> float:
        """Calculate value offset from top"""
        corrected = min(max(value, self.min), self.max)
        return self.height - ((corrected - self.min) * self.value_to_height)


@dataclasses.dataclass
class Stack:  # pylint: disable=too-many-instance-attributes
    """Representation of a stack (can be a sum of series)"""

    id: int
    datas: list[str] = dataclasses.field(default_factory=list)
    width: float = None
    type: SerieType = None
    y_axis: str = "left"
    totals: pd.Series = None


res_dir = pkg_resources.files("o7pdf").joinpath("res")


# *************************************************
# https://pyfpdf.github.io/fpdf2/fpdf/
# *************************************************
class PandasChart(PandasBasic):  # pylint: disable=too-many-instance-attributes
    """Class to generate a chart from Pandas Dataframe in a PDF Report"""

    def __init__(self, series: list[SerieParam], width: float, height: float, **kwargs):
        super().__init__(**kwargs)

        self.param: ChartParam = ChartParam()
        self.series: list[SerieParam] = series
        self.width: float = width
        self.height: float = height

        self._chart_rect: Rectangle = Rectangle()
        self._data_rect: Rectangle = Rectangle()

        self._x_count: int = None
        self._x_width: float = None  # Width of each X elements
        self._x_spacing: float = None  # distance between each X element
        self._x_axis_height: float = 5

        self.axis: dict[Axis] = {"left": Axis(position="left"), "right": Axis(position="right")}
        self.stacks: dict[Stack] = {}

    # *************************************************
    #
    # *************************************************
    def prepare(self):
        """Prepare variables before the CHART generation"""

        # Determine the number of X elements & variables

        # Set the chart rectangle (Maximum area)
        self._chart_rect.x = self.original_x
        self._chart_rect.y = self.original_y
        self._chart_rect.w = self.width
        self._chart_rect.h = self.height

        # Set the data rectangle (Area for the data)
        self._data_rect.x = self.original_x + self.axis["left"].width
        self._data_rect.y = self.original_y
        self._data_rect.w = self.width - self.axis["left"].width
        self._data_rect.h = self.height - self._x_axis_height

        self._x_count = len(self.df.index)
        self._x_width = self._data_rect.w / self._x_count
        self._x_spacing = self._x_width * self.param.spacing

        # ---------------------------
        # Prepare Series values
        # ---------------------------
        for serie in self.series:
            if serie.color is None:
                serie.color = self.LINE_COLOR

            if not serie.is_stacked or len(self.stacks) == 0:
                current_stack = Stack(y_axis=serie.y_axis, id=len(self.stacks), type=serie.type)
                self.stacks[current_stack.id] = current_stack

            serie.stack_id = current_stack.id

            if serie.data in self.df.columns:
                current_stack.datas.append(serie.data)
            if serie.data_max in self.df.columns:
                current_stack.datas.append(serie.data_max)
            if serie.data_min in self.df.columns:
                current_stack.datas.append(serie.data_min)

        # ---------------------------
        # Prepare Stack values
        # ---------------------------
        for stack in self.stacks.values():
            stack.width = (self._x_width - self._x_spacing) / len(self.stacks)
            stack.totals = self.df[stack.datas].sum(axis=1)

            self.axis[stack.y_axis].active = True

            # print(f"---------------- Stack {stack.id} ----------------")
            # print(stack)

        # ---------------------------
        # Prepare the Axis values
        # ---------------------------
        for axis in self.axis.values():
            if not axis.active:
                continue

            if axis.color is None:
                axis.color = self.LINE_COLOR

            axis.height = self._data_rect.h

            if axis.max is None:
                axis.max = max(
                    stack.totals.max()
                    for stack in self.stacks.values()
                    if stack.y_axis == axis.position
                )

            if axis.min is None:
                axis.min = min(
                    stack.totals.min()
                    for stack in self.stacks.values()
                    if stack.y_axis == axis.position
                )
            if axis.step is None:
                axis.step = (axis.max - axis.min) / 5 if axis.step is None else axis.step

            # print(f'---------------- Axis {axis.position} ----------------')
            # print(axis)

        return self

    # *************************************************
    #
    # *************************************************
    def generate(self):
        """Generate the table inside the PDF Report"""

        self.prepare()

        self.draw_current_highlight()

        self.draw_x_label()

        for axis in self.axis.values():
            if axis.active:
                self.draw_axis(axis)

        self.draw_data()
        self.draw_title()
        # self.draw_borders([self._chart_rect], self.LINE_COLOR)

        self.pdf.set_xy(self._chart_rect.x, self._chart_rect.y2)

        return self

    # *************************************************
    #
    # *************************************************
    def draw_title(self):
        """Draw the chart title"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size=self.font_size)
            self.pdf.set_text_color(**self.LINE_COLOR)
            self.pdf.set_xy(self._data_rect.x, self._data_rect.y)
            self.pdf.cell(
                w=self._data_rect.w,
                h=self.font_size / 2,
                text=f"{self.title}",
                fill=False,
                new_x="LEFT",
                new_y="NEXT",
                align="C",
                border=0,
                markdown=True,
            )

    # *************************************************
    #
    # *************************************************
    def draw_data(self):
        """Draw the data in the chart"""

        for stack in self.stacks.values():
            self.draw_stack(stack)

    # *************************************************
    #
    # *************************************************
    def draw_stack(self, stack: Stack):
        """Draw stack in the chart"""

        axis = self.axis[stack.y_axis]
        series = [serie for serie in self.series if serie.stack_id == stack.id]

        top_values = stack.totals
        bottom_values = stack.totals

        for serie in series:
            top_values = bottom_values

            bottom_values = (
                top_values - self.df[serie.data] if serie.data in self.df.columns else top_values
            )

            with self.pdf.local_context():
                self.pdf.set_draw_color(**serie.color)
                self.pdf.set_fill_color(**serie.color)
                self.pdf.set_line_width(0.4)

                prev_top = None
                prev_bottom = None
                for count, index in enumerate(self.df.index):
                    top = axis.value_to_offset(top_values[index])
                    bottom = axis.value_to_offset(bottom_values[index])

                    if stack.type == SerieType.BAR:
                        self.draw_stack_bar(top, bottom, count, stack)
                    elif stack.type == SerieType.LINE:
                        self.draw_stack_line(current=top, prev=prev_top, count=count, stack=stack)
                    elif stack.type == SerieType.ZONE:
                        # print(f"Draw Zone {serie.data_min} {serie.data_max}")
                        top = axis.value_to_offset(self.df[serie.data_max][index])
                        bottom = axis.value_to_offset(self.df[serie.data_min][index])
                        self.draw_stack_zone(
                            top=top,
                            prev_top=prev_top,
                            bottom=bottom,
                            prev_bottom=prev_bottom,
                            count=count,
                            stack=stack,
                        )

                    prev_bottom = bottom
                    prev_top = top

    # *************************************************
    #
    # *************************************************
    def draw_stack_bar(self, top: float, bottom: float, count: int, stack: Stack):
        """Draw a bar stack in the chart"""

        x_pos = (
            self._data_rect.x
            + (count * self._x_width)
            + (stack.id * stack.width)
            + (self._x_spacing / 2)
        )
        y_pos = self._data_rect.y + top
        height = bottom - top

        self.pdf.rect(x_pos, y_pos, stack.width, height, style="F")

    # *************************************************
    #
    # *************************************************
    def draw_stack_line(self, current: float, prev: float, count: int, stack: Stack):
        """Draw a line stack in the chart"""
        # print(f"Draw Line Stack {stack.id} count={count} current={current} prev={prev}")

        x_pos = self._data_rect.x + ((count + 0.5) * self._x_width)
        y_pos = self._data_rect.y + current

        self.pdf.circle(x_pos, y_pos, 0.8, style="F")

        # self.pdf.free_text_annotation(
        #     x=x_pos - 0.4,
        #     y=y_pos - 0.4,
        #     text=f"{current}",
        #     w=0.8,
        #     h=0.8,
        # )

        if prev is not None:
            prev_x_pos = x_pos - self._x_width
            prev_y_pos = self._data_rect.y + prev

            self.pdf.line(prev_x_pos, prev_y_pos, x_pos, y_pos)

    # *************************************************
    #
    # *************************************************
    def draw_stack_zone(
        self,
        top: float,
        prev_top: float,
        bottom: float,
        prev_bottom: float,
        count: int,
        stack: Stack,
    ):
        """Draw a line stack in the chart"""
        # print(f"Draw Line Stack {stack.id} count={count} top={top} prev_top={prev_top}")

        if prev_top is None:
            return

        x_pos = self._data_rect.x + ((count + 0.5) * self._x_width)
        prev_x_pos = x_pos - self._x_width

        y_top_pos = self._data_rect.y + top
        prev_y_top_pos = self._data_rect.y + prev_top

        y_bottom_pos = self._data_rect.y + bottom
        prev_y_bottom_pos = self._data_rect.y + prev_bottom

        coords = (
            (x_pos, y_top_pos),
            (x_pos, y_bottom_pos),
            (prev_x_pos, prev_y_bottom_pos),
            (prev_x_pos, prev_y_top_pos),
        )
        self.pdf.polygon(coords, style="DF")

    # *************************************************
    #
    # *************************************************
    def draw_x_label(self):
        """Draw label for the x axis"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size=self.font_size)
            self.pdf.set_text_color(**self.LINE_COLOR)

            for index, title in enumerate(self.df.index):
                x_pos = self._data_rect.x + (index * self._x_width)
                y_pos = self._data_rect.y + self._data_rect.h

                if index % self.param.x_label_step == 0:
                    self.pdf.set_xy(x_pos, y_pos)
                    self.pdf.cell(
                        w=self._x_width,
                        h=self._x_axis_height,
                        text=f"{title}",
                        fill=False,
                        new_x="LEFT",
                        new_y="NEXT",
                        align="C",
                        border=0,
                        markdown=True,
                    )

                    x_pos_center = x_pos + (self._x_width / 2)

                    # set the vertical line
                    self.pdf.line(x_pos_center, y_pos, x_pos_center, y_pos + 0.75)

            # Draw the bottom line
            self.pdf.line(
                self._data_rect.x,
                self._data_rect.y2,
                self._data_rect.x2,
                self._data_rect.y2,
            )

    # *************************************************
    #
    # *************************************************
    def draw_axis(self, axis: Axis):
        """Draw label for the a Y axis"""

        with self.pdf.local_context():
            self.pdf.set_font("OpenSans", size=self.font_size)
            self.pdf.set_text_color(**axis.color)
            self.pdf.set_draw_color(**self.LINE_COLOR_BG)

            for value in range(int(axis.min), int(axis.max), int(axis.step)):
                height = (value - axis.min) * axis.value_to_height
                y_pos = self._data_rect.y + self._data_rect.h - height

                self.pdf.set_xy(self._chart_rect.x, y_pos - (self.font_size / 2))
                self.pdf.cell(
                    w=self.axis["left"].width,
                    h=self.font_size,
                    text=f"{axis.format.format(value)}",
                    fill=False,
                    new_x="LEFT",
                    new_y="NEXT",
                    align="C",
                    border=0,
                    markdown=True,
                )

                self.pdf.line(self._data_rect.x, y_pos, self._data_rect.x2, y_pos)

            self.pdf.set_draw_color(**axis.color)
            self.pdf.line(
                self._data_rect.x,
                self._data_rect.y,
                self._data_rect.x,
                self._data_rect.y2,
            )

    # *************************************************
    #
    # *************************************************
    def draw_current_highlight(self):
        """Draw box to show the current value"""

        if self.current is None:
            return

        with self.pdf.local_context():
            self.pdf.set_draw_color(**self.PROGRESS)
            self.pdf.set_fill_color(**self.PROGRESS)

            count = len(self.df.index) - 1
            x_pos = self._data_rect.x + (count * self._x_width)
            width = self._x_width
            y_pos = self._chart_rect.y
            height = self._chart_rect.h

            self.pdf.rect(x_pos, y_pos, width, height, style="F")
