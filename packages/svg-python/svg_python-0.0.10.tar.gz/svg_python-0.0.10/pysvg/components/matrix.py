from typing import Literal, Tuple
from typing_extensions import override

from pydantic import Field

from pysvg.constants import INDENT
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pysvg.components.cell import (
    CellConfig,
    Cell,
    CellCenterLocate,
    CellLeftTopLocate,
    CellLeftBottomLocate,
    CellRightTopLocate,
    CellRightBottomLocate,
)
from pysvg.components.content import TextConfig, TextContent
from pysvg.schema import AppearanceConfig, Color, TransformConfig, BBox
from pysvg.utils import MatrixIterator, MatrixBoardIterator, add_matrix_border
from pysvg.logger import get_logger

# Define matrix element data type
MatElemType = str | int | float

# Define border position type
CoordPosition = Literal["upperleft", "upperright", "lowerleft", "lowerright"]


class MatrixConfig(ComponentConfig):
    """Matrix component configuration"""

    x: float = Field(default=0, description="Matrix x position")
    y: float = Field(default=0, description="Matrix y position")
    cell_size: float = Field(default=50, ge=1, description="Size of each cell")
    cell_padding: float = Field(default=5, ge=0, description="Padding inside each cell")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        return {}


class Matrix(BaseSVGComponent):
    """
    Matrix Component - Matrix visualization component, implemented based on Cell component
    """

    def __init__(
        self,
        data: list[list[MatElemType]],
        config: MatrixConfig | None = None,
        transform: TransformConfig | None = None,
        element_map: dict[MatElemType, BaseSVGComponent] = {},
        background_map: dict[MatElemType, AppearanceConfig] = {},
        caption: str | None = None,
        caption_location: Literal["top", "bottom", "left", "right"] | None = None,
        caption_margin: float = 20,
        caption_font_size: float = 16,
        caption_font_family: str = "Arial",
        caption_font_color: Color = Color("black"),
        border_as_coord: CoordPosition | None = None,
        coord_font_size: float = 16,
        coord_font_family: str = "Arial",
        coord_font_color: Color = Color("black"),
        elem_locate_on_line: bool = False,
    ):
        """Creates a Matrix component for visualizing 2D data in SVG format.

        This component allows you to create a matrix visualization where each element can be
        customized with different content and appearance. It supports features like captions
        and border numbering for better data representation.

        Args:
            data (list[list[MatElemType]]): 2D list containing the matrix data. Must be rectangular
                (all rows must have the same length). Elements can be strings, integers, or floats.
            config (MatrixConfig | None, optional): Configuration for the matrix component.
                Defaults to MatrixConfig().
            transform (TransformConfig | None, optional): Transform configuration for the matrix.
                Defaults to TransformConfig().
            element_map (dict[MatElemType, BaseSVGComponent] | None, optional): Maps matrix elements
                to their visual representations. If None, elements are displayed as text.
            background_map (dict[MatElemType, AppearanceConfig] | None, optional): Maps matrix elements
                to their cell background appearances. If None, cells have transparent background.
            caption (str | None, optional): Caption text for the matrix. Must be provided if
                caption_location is set.
            caption_location (Literal["top", "bottom", "left", "right"] | None, optional): Position of
                the caption relative to the matrix. Must be provided if caption is set.
            caption_margin (float, optional): Space between caption and matrix. Defaults to 20.
            caption_font_size (float, optional): Font size for caption text. Defaults to 16.
            caption_font_family (str, optional): Font family for caption text. Defaults to "Arial".
            caption_font_color (Color, optional): Color for caption text. Defaults to black.
            border_as_coord (BorderPosition | None, optional): Position for displaying row/column
                numbers. Can be "upperleft", "upperright", "lowerleft", or "lowerright".
            coord_font_size (float, optional): Font size for border numbers. Defaults to 16.
            coord_font_family (str, optional): Font family for border numbers. Defaults to "Arial".
            coord_font_color (Color, optional): Color for border numbers. Defaults to black.
            elem_locate_on_line (bool, optional): Whether to locate the element on the line.

        Raises:
            ValueError: If the matrix data is not rectangular, or if caption and caption_location
                are not properly paired (both must be either set or None).
        """
        _logger = get_logger(self.__class__.__name__)
        super().__init__(
            config=config or MatrixConfig(),
            transform=transform or TransformConfig(),
        )
        self._original_border_as_coord = border_as_coord

        if caption_location is not None and caption_location not in [
            "top",
            "bottom",
            "left",
            "right",
        ]:
            raise ValueError(f"Invalid caption location: {caption_location}")

        if elem_locate_on_line and border_as_coord is None:
            _logger.info(
                "`elem_locate_on_line` is True, but `border_as_coord` set as None. "
                "We will pad empty elements to the left and top border of the matrix data."
            )
            border_as_coord = "upperleft"
            data = add_matrix_border(data, pad_elem="", mode="tl")

        itmode = "Rl2rCt2b"
        cell_cls = CellCenterLocate
        if elem_locate_on_line:
            match border_as_coord:
                case "upperleft":
                    cell_cls = CellLeftTopLocate
                case "upperright":
                    cell_cls = CellRightTopLocate
                    itmode = "Rr2lCt2b"
                case "lowerleft":
                    cell_cls = CellLeftBottomLocate
                    itmode = "Cb2tRl2r"
                case "lowerright":
                    cell_cls = CellRightBottomLocate
                    itmode = "Cb2tRr2l"
                case _:
                    raise ValueError(f"Invalid border position: {border_as_coord}")

        # Verify matrix is rectangular
        rows = len(data)
        cols = len(data[0])
        if not all(len(row) == cols for row in data):
            raise ValueError("Matrix data must be rectangular")

        self._cell_cls = cell_cls

        # Matrix properties
        self._data = data
        self._rows = rows
        self._cols = cols

        # Matrix iterator
        self._it = list(MatrixIterator(rows, cols, itmode))
        self._board_it = list(MatrixBoardIterator(rows, cols))

        # Validate caption and caption_location pairing
        if caption is not None and caption_location is None:
            raise ValueError("caption_location must be provided when caption is specified")
        if caption_location is not None and caption is None:
            raise ValueError("caption must be provided when caption_location is specified")

        # Store element and background maps
        self._element_map = element_map
        self._background_map = background_map

        self._elem_locate_on_line = elem_locate_on_line

        # Caption related settings
        self._caption = (
            TextContent(
                text=caption,
                config=TextConfig(
                    font_size=caption_font_size,
                    font_family=caption_font_family,
                    color=caption_font_color,
                    text_anchor="middle",
                    dominant_baseline="central",
                ),
            )
            if caption
            else None
        )
        self._caption_location = caption_location
        self._caption_margin = caption_margin

        # Coordinate related settings
        self._coord_position: CoordPosition | None = border_as_coord
        self._coord_font_size: float = coord_font_size
        self._coord_font_family: str = coord_font_family
        self._coord_color: Color = coord_font_color

    @property
    def width(self) -> float:
        return self._cols * self.config.cell_size

    @property
    def height(self) -> float:
        return self._rows * self.config.cell_size

    @property
    def cell_size(self) -> float:
        return self.config.cell_size

    @property
    def half_cell_size(self) -> float:
        return self.config.cell_size / 2

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        if self._coord_position is None:
            # No border labeling, use center of entire matrix
            center_x = self.config.x + (self._cols * self.config.cell_size) / 2
            center_y = self.config.y + (self._rows * self.config.cell_size) / 2
        else:
            # With border labeling, need to calculate center of actual content area
            content_cols = self._cols - 1
            content_rows = self._rows - 1
            if self._coord_position == "upperleft":
                # Actual content area: excluding row 0 and column 0
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
                if self._elem_locate_on_line:
                    content_start_x -= self.half_cell_size
                    content_start_y -= self.half_cell_size
            elif self._coord_position == "upperright":
                # Actual content area: excluding row 0 and last column
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
                if self._elem_locate_on_line:
                    content_start_x += self.half_cell_size
                    content_start_y -= self.half_cell_size
            elif self._coord_position == "lowerleft":
                # Actual content area: excluding last row and column 0
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y  # Start from row 0
                if self._elem_locate_on_line:
                    content_start_x -= self.half_cell_size
                    content_start_y += self.half_cell_size
            elif self._coord_position == "lowerright":
                # Actual content area: excluding last row and last column
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y  # Start from row 0
                if self._elem_locate_on_line:
                    content_start_x += self.half_cell_size
                    content_start_y += self.half_cell_size
            else:
                raise ValueError(f"Invalid border position: {self._coord_position}")
            center_x = content_start_x + (content_cols * self.config.cell_size) / 2
            center_y = content_start_y + (content_rows * self.config.cell_size) / 2

        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        min_x = self.config.x
        min_y = self.config.y
        max_x = self.config.x + self.width
        max_y = self.config.y + self.height

        # Consider caption position
        if self._caption is not None:
            max_y += self.config.caption_margin
            max_x += self.config.caption_margin

        return BBox(
            x=self.transform.translate[0] + min_x,
            y=self.transform.translate[1] + min_y,
            width=max_x - min_x,
            height=max_y - min_y,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Matrix":
        cp_origin = self.central_point_relative
        ratio = min(width / self.width, height / self.height)
        if mode == "fit" and ratio >= 1.0:
            return self
        self.config.cell_size = self.config.cell_size * ratio
        self.move(cp_origin[0], cp_origin[1])
        return self

    @override
    def to_svg_element(self) -> str:
        elements = []

        self._create_cells()

        # Collect all SVGContent components for symbol definitions
        svg_symbols = self._collect_svg_symbols()

        # Add symbol definitions if any
        if svg_symbols:
            defs_content = "\n".join(svg_symbols)
            elements.append(f"<defs>\n{defs_content}".replace("\n", "\n" + INDENT) + "\n</defs>")

        # Add all cells in the order specified by the iterator.
        for i, j in self._it:
            elements.append(self._cells[i][j].to_svg_element())

        # Add caption
        if self._caption is not None:
            elements.append(self._render_caption())

        attr = self.get_attr_str()
        svg_code = "\n".join(elements)
        return f"<g {attr}>\n{svg_code}".replace("\n", "\n" + INDENT) + "\n</g>"

    def _collect_svg_symbols(self) -> list[str]:
        """Collect all SVGContent components and generate symbol definitions"""
        from pysvg.components.content import SVGContent

        svg_symbols = []
        seen_symbols = set()

        # Iterate through all elements in the matrix to find SVGContent components
        for original_elem in self._element_map.values():
            if isinstance(original_elem, SVGContent):
                symbol_id = original_elem.symbol_id
                if symbol_id not in seen_symbols:
                    svg_symbols.append(original_elem.get_symbol_definition())
                    seen_symbols.add(symbol_id)

        return svg_symbols

    def _create_cells(self):
        """Create all Cell components"""
        self._cells: list[list[Cell]] = []
        none_appearance = AppearanceConfig(fill=Color("none"), stroke=Color("none"), stroke_width=0)

        for i in range(self._rows):
            row_cells = []
            for j in range(self._cols):
                # Get actual element (considering mapping)
                original_elem = self._data[i][j]
                actual_elem: BaseSVGComponent = self._element_map.get(
                    original_elem, TextContent(str(original_elem))
                )
                bg_appearance = self._background_map.get(
                    original_elem, AppearanceConfig(fill=Color("none"), stroke=Color("black"))
                )

                # Set coordinate cell appearance as none
                if self._is_coord_cell(i, j):
                    bg_appearance = none_appearance
                    if isinstance(actual_elem, TextContent):
                        actual_elem.config.color = self._coord_color
                        actual_elem.config.font_size = self._coord_font_size
                        actual_elem.config.font_family = self._coord_font_family

                # In case of elem_locate_on_line, we need to set the background of the border (from the four corners) to none.
                if self._elem_locate_on_line:
                    if (i, j) in self._board_it:
                        bg_appearance = none_appearance

                cell = self._cell_cls(
                    config=CellConfig(
                        embed_component=actual_elem,
                        padding=self.config.cell_padding,
                        width=self.config.cell_size,
                        height=self.config.cell_size,
                    ),
                    appearance=bg_appearance,
                )
                cell.move(
                    self.config.x + j * self.config.cell_size + self.half_cell_size,
                    self.config.y + i * self.config.cell_size + self.half_cell_size,
                )

                row_cells.append(cell)

            self._cells.append(row_cells)

    def _render_caption(self) -> str:
        """Convert caption to svg code"""
        if self._caption is None or self._caption_location is None:
            raise ValueError(
                "Caption is not set or caption_location is not set, but using _render_caption()"
            )

        self._caption.set_cpoint_to_lefttop()

        # Get matrix center point (considering border labeling effect)
        center_x_relative, center_y_relative = self.central_point_relative

        # Adjust coordinates based on position, using center point as reference
        if self._caption_location == "top":
            self._caption.move(center_x_relative, self.config.y - self._caption_margin)
        elif self._caption_location == "bottom":
            self._caption.move(
                center_x_relative, self.config.y + self.height + self._caption_margin
            )
        elif self._caption_location == "left":
            self._caption.config.text_anchor = "end"
            self._caption.move(self.config.x - self._caption_margin, center_y_relative)
        elif self._caption_location == "right":
            self._caption.config.text_anchor = "start"
            self._caption.move(self.config.x + self.width + self._caption_margin, center_y_relative)

        if self._original_border_as_coord and self._elem_locate_on_line:
            if "upper" in self._coord_position and self._caption_location == "top":
                self._caption.move_by(0, -self.half_cell_size)
            elif "lower" in self._coord_position and self._caption_location == "bottom":
                self._caption.move_by(0, self.half_cell_size)
            elif "left" in self._coord_position and self._caption_location == "left":
                self._caption.move_by(-self.half_cell_size, 0)
            elif "right" in self._coord_position and self._caption_location == "right":
                self._caption.move_by(self.half_cell_size, 0)

        # # WARNING: This is a hack to fix the caption position when border is not set as coordinate and elem_locate_on_line is True
        if self._original_border_as_coord is None and self._elem_locate_on_line:
            assert self._coord_position == "upperleft"
            if self._caption_location == "top":
                self._caption.move_by(0, self.half_cell_size)
            elif self._caption_location == "bottom":
                self._caption.move_by(0, -self.half_cell_size)
            elif self._caption_location == "left":
                self._caption.move_by(self.half_cell_size, 0)
            elif self._caption_location == "right":
                self._caption.move_by(-self.half_cell_size, 0)

        return self._caption.to_svg_element()

    def _is_coord_cell(self, row: int, col: int) -> bool:
        """Check if the cell at specified position is a border label cell"""
        if self._coord_position is None:
            return False

        if self._coord_position == "upperleft":
            return row == 0 or col == 0
        elif self._coord_position == "upperright":
            return row == 0 or col == self._cols - 1
        elif self._coord_position == "lowerleft":
            return row == self._rows - 1 or col == 0
        elif self._coord_position == "lowerright":
            return row == self._rows - 1 or col == self._cols - 1

        return False
