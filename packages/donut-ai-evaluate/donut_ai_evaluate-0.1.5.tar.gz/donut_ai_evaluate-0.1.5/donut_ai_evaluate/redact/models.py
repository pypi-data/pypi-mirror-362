# --- Bbox Dataclass ---
from dataclasses import dataclass
from donut_ai_evaluate._common.eval_logger import  logger
from typing import List,Tuple,Union

@dataclass
class Bbox:
    """
    Represents a bounding box with coordinates and dimensions.

    Can be instantiated directly with x, y, w, h or via class methods:
    - Bbox.from_xywh_list([x, y, w, h])
    - Bbox.from_coords_list([x1, y1, x2, y2])

    Attributes:
        x (float): The x-coordinate of the top-left corner.
        y (float): The y-coordinate of the top-left corner.
        w (float): The width of the bounding box. Must be non-negative.
        h (float): The height of the bounding box. Must be non-negative.
    """
    x: float
    y: float
    w: float
    h: float

    def __post_init__(self):
        """Validate width and height after initialization."""
        if self.w < 0:
            logger.warning(f"Attempted to create Bbox with negative width: {self.w}. Raising ValueError.")
            raise ValueError(f"Width cannot be negative: {self.w}")
        if self.h < 0:
            logger.warning(f"Attempted to create Bbox with negative height: {self.h}. Raising ValueError.")
            raise ValueError(f"Height cannot be negative: {self.h}")
        logger.debug(f"Bbox created successfully: {self}")


    def area(self) -> float:
        """Calculates the area of the bounding box."""
        return self.w * self.h

    def get_coords(self) -> Tuple[float, float, float, float]:
        """Returns the top-left (x1, y1) and bottom-right (x2, y2) coordinates."""
        return self.x, self.y, self.x + self.w, self.y + self.h

    @classmethod
    def from_xywh_list(cls: "Bbox", xywh_list: List[Union[int, float]]) -> "Bbox":
        """
        Creates a Bbox instance from a list containing [x, y, w, h].

        Args:
            xywh_list: A list or tuple containing four numbers representing
                       the x-coordinate, y-coordinate, width, and height,
                       in that order.

        Returns:
            A Bbox instance.

        Raises:
            TypeError: If `xywh_list` is not a list or tuple, or if elements
                       are not numbers (int or float).
            ValueError: If `xywh_list` does not contain exactly four elements,
                        or if width or height calculated are negative (checked
                        during Bbox initialization).
        """
        logger.debug(f"Attempting to create Bbox from xywh_list: {xywh_list}")
        if not isinstance(xywh_list, (list, tuple)):
            raise TypeError(f"Input must be a list or tuple, got {type(xywh_list)}")
        if len(xywh_list) != 4:
            raise ValueError(f"Input list must contain exactly 4 elements (x, y, w, h), got {len(xywh_list)}")

        try:
            # Attempt conversion to float for consistency, handle potential errors
            x, y, w, h = map(float, xywh_list)
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting elements of xywh_list to float: {xywh_list} - {e}", exc_info=True)
            raise TypeError(f"All elements in xywh_list must be numbers (int or float). Error: {e}") from e

        # The __post_init__ of Bbox will handle w < 0 and h < 0 checks
        try:
             instance = cls(x=x, y=y, w=w, h=h)
             logger.debug(f"Successfully created Bbox from xywh_list: {instance}")
             return instance
        except ValueError as e: # Catch potential errors from __post_init__
            logger.error(f"Validation failed during Bbox creation from xywh_list {xywh_list}: {e}")
            raise # Re-raise the original ValueError from __post_init__


    @classmethod
    def from_coords_list(cls: "Bbox", coords_list: List[Union[int, float]]) -> "Bbox":
        """
        Creates a Bbox instance from a list containing [x1, y1, x2, y2].

        Args:
            coords_list: A list or tuple containing four numbers representing
                         the top-left x, top-left y, bottom-right x, and
                         bottom-right y coordinates, in that order.

        Returns:
            A Bbox instance.

        Raises:
            TypeError: If `coords_list` is not a list or tuple, or if elements
                       are not numbers (int or float).
            ValueError: If `coords_list` does not contain exactly four elements,
                        or if x2 < x1 or y2 < y1 (implying negative width/height).
        """
        logger.debug(f"Attempting to create Bbox from coords_list: {coords_list}")
        if not isinstance(coords_list, (list, tuple)):
             raise TypeError(f"Input must be a list or tuple, got {type(coords_list)}")
        if len(coords_list) != 4:
            raise ValueError(f"Input list must contain exactly 4 elements (x1, y1, x2, y2), got {len(coords_list)}")

        try:
            # Attempt conversion to float for consistency
            x1, y1, x2, y2 = map(float, coords_list)
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting elements of coords_list to float: {coords_list} - {e}", exc_info=True)
            raise TypeError(f"All elements in coords_list must be numbers (int or float). Error: {e}") from e

        # Pre-validation before calculating w, h
        if x2 < x1:
            msg = f"Invalid coordinates: x2 ({x2}) cannot be less than x1 ({x1})."
            logger.error(msg)
            raise ValueError(msg)
        if y2 < y1:
            msg = f"Invalid coordinates: y2 ({y2}) cannot be less than y1 ({y1})."
            logger.error(msg)
            raise ValueError(msg)

        # Calculate x, y, w, h
        x = x1
        y = y1
        w = x2 - x1
        h = y2 - y1

        # Standard Bbox constructor will call __post_init__ for final checks (e.g., if somehow w/h are still negative, though the checks above should prevent it)
        try:
            instance = cls(x=x, y=y, w=w, h=h)
            logger.debug(f"Successfully created Bbox from coords_list: {instance}")
            return instance
        except ValueError as e: # Catch potential errors from __post_init__
            logger.error(f"Validation failed during Bbox creation from coords_list {coords_list}: {e}")
            raise # Re-raise the original ValueError


BboxDataType = List[Union[int, float]] # Represents [x, y, w, h]
