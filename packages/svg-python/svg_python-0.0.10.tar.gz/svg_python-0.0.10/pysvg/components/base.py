from abc import ABC, abstractmethod
from typing import Literal, Tuple

from pysvg.logger import get_logger
from pysvg.schema import AppearanceConfig, BBox, ComponentConfig, TransformConfig


class BaseSVGComponent(ABC):
    """
    Abstract base class for all SVG components.

    This class defines the common interface that all SVG components should implement,
    including common properties (appearance, transform) and abstract methods that
    must be implemented by each specific component type.
    """

    def __init__(
        self,
        config: ComponentConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        """
        Initialize the base SVG component.

        Args:
            appearance: External appearance configuration
            transform: Transform configuration
        """
        self.config = config
        self.appearance = appearance
        self.transform = transform

    @property
    @abstractmethod
    def central_point_relative(self) -> Tuple[float, float]:
        """
        Get the central point of the component.

        This property must be implemented by subclasses to return the central point
        of the specific component type. The return type may vary based on the
        component's coordinate system and representation.

        Returns:
            The central point of the component
        """
        raise NotImplementedError("Subclasses must implement this property")

    @abstractmethod
    def get_bounding_box(self) -> BBox:
        """
        Get the bounding box of the component using **absolute coordinates**.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "BaseSVGComponent":
        """
        Restrict the size of the component to a maximum width and height.

        Note: This method will **keep central point and aspect ratio unchanged**

        Args:
            width: Target width
            height: Target height
            mode: Mode to restrict the size. Available options:
                - "fit": Scale the component to fit within the specified dimensions.
                        If the component is already smaller, no scaling is applied.
                - "force": Scale the component to exactly match the specified dimensions,
                          regardless of its current size.

        Returns:
            Self for method chaining
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def to_svg_element(self) -> str:
        """
        Generate the complete SVG element string.

        Returns:
            Complete SVG element as XML string
        """
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def central_point(self) -> Tuple[float, float]:
        """
        Get the absolute central point of the component.

        If transform is not set, returns the relative central point with a warning.
        If transform is set, returns the central point with translation applied.

        Returns:
            Tuple[float, float]: The absolute (x, y) coordinates of the central point
        """
        relative_x, relative_y = self.central_point_relative

        _logger = get_logger(self.__class__.__name__)
        if not self.has_transform():
            _logger.warning(
                f"{self.__class__.__name__} has no transform, returning relative central point"
            )
            return relative_x, relative_y

        translate = self.transform.translate or (0, 0)
        return relative_x + translate[0], relative_y + translate[1]

    def get_attr_dict(self) -> dict[str, str]:
        """
        Get the attributes of the component as a dictionary.
        """
        attr = {}
        if self.has_config():
            attr.update(self.config.to_svg_dict())
        if self.has_appearance():
            attr.update(self.appearance.to_svg_dict())
        if self.has_transform():
            attr.update(self.transform.to_svg_dict())
        attr = {k: str(v) for k, v in attr.items()}
        return attr

    def get_attr_str(self) -> str:
        """Get the attributes of the component as a string."""
        attr = self.get_attr_dict()
        return " ".join([f'{k}="{v}"' for k, v in attr.items() if v is not None])

    def has_config(self) -> bool:
        """Check if the component has a config."""
        return hasattr(self, "config") and isinstance(self.config, ComponentConfig)

    def has_appearance(self) -> bool:
        """Check if the component has an appearance."""
        return hasattr(self, "appearance") and isinstance(self.appearance, AppearanceConfig)

    def has_transform(self) -> bool:
        """Check if the component has any transforms."""
        return (
            self.transform is not None
            and isinstance(self.transform, TransformConfig)
            and self.transform.have_set()
        )

    def move(self, cx: float, cy: float) -> "BaseSVGComponent":
        """
        Move the component to a specified position.

        Note:
            Coordinates are based on the central point of the component.

        Args:
            cx: central point x coordinate to move to
            cy: central point y coordinate to move to

        Returns:
            Self for method chaining
        """
        self.set_cpoint_to_lefttop()
        self.move_by(cx, cy)
        return self

    def move_by(self, dx: float, dy: float) -> "BaseSVGComponent":
        """
        Move the component by a specified offset.

        Args:
            dx: X offset to move by
            dy: Y offset to move by

        Returns:
            Self for method chaining
        """
        current_translate = self.transform.translate or (0, 0)
        new_x = current_translate[0] + dx
        new_y = current_translate[1] + dy
        self.transform.translate = (new_x, new_y)
        return self

    def set_cpoint_to_lefttop(self) -> "BaseSVGComponent":
        """
        Set the central point of the component to the left top corner
        """
        cp_x, cp_y = self.central_point
        self.move_by(-cp_x, -cp_y)
        return self

    def rotate(
        self, angle: float | Tuple[float, float, float], around_center_relative: bool = True
    ) -> "BaseSVGComponent":
        """
        Rotate the component by a specified angle.

        Args:
            angle: Rotation angle in degrees
            around_center_relative: If True, rotate around component center (relative); if False, rotate around origin

        Returns:
            Self for method chaining
        """
        if around_center_relative:
            cx, cy = self.central_point_relative
            self.transform.rotate = (angle, cx, cy)
        else:
            self.transform.rotate = angle
        return self

    def scale(self, scale_factor: float) -> "BaseSVGComponent":
        """
        Scale the component by a specified factor.

        Args:
            scale_factor: Scale factor.

        Note:
            This method is different from the standard SVG scale method.
                1. The standard SVG scale method scales the component from the left top corner,
                   while this method scales the component from the center.
                2. We strictly scale according to the size of the graphic bounding box area, which is different from standard SVG

        Returns:
            Self for method chaining
        """
        bbox = self.get_bounding_box()
        current_width = bbox.width
        current_height = bbox.height
        target_width = current_width * scale_factor
        target_height = current_height * scale_factor
        return self.restrict_size(target_width, target_height, mode="force")

    def skew(self, skew_x: float | None = None, skew_y: float | None = None) -> "BaseSVGComponent":
        """
        Apply skew transform to the component.

        Args:
            skew_x: X-axis skew angle in degrees (optional)
            skew_y: Y-axis skew angle in degrees (optional)

        Returns:
            Self for method chaining
        """
        if skew_x is not None:
            self.transform.skew_x = skew_x
        if skew_y is not None:
            self.transform.skew_y = skew_y
        return self

    def reset_transform(self) -> "BaseSVGComponent":
        """
        Reset all transforms to default values.

        Returns:
            Self for method chaining
        """
        self.transform.reset()
        return self

    def reset_appearance(self) -> "BaseSVGComponent":
        """
        Reset all appearance to default values.

        Returns:
            Self for method chaining
        """
        self.appearance.reset()
        return self
