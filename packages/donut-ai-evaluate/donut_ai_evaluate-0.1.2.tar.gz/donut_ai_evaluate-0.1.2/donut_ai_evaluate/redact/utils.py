from .models import Bbox

# --- IoU Calculation Helper ---
def calculate_iou(box1: Bbox, box2: Bbox) -> float:
    """
    Calculates the Intersection over Union (IoU) score for two bounding boxes.

    Args:
        box1: The first bounding box (Bbox object).
        box2: The second bounding box (Bbox object).

    Returns:
        The IoU score (float between 0.0 and 1.0).
        Returns 0.0 if there is no overlap or if the union area is zero.

    Raises:
        TypeError: If inputs are not Bbox instances.
    """
    if not isinstance(box1, Bbox) or not isinstance(box2, Bbox):
        raise TypeError("Both inputs must be Bbox instances.")

    # Get coordinates (x1, y1, x2, y2)
    x1_1, y1_1, x2_1, y2_1 = box1.get_coords()
    x1_2, y1_2, x2_2, y2_2 = box2.get_coords()

    # Calculate coordinates of the intersection rectangle
    inter_x1 = max(x1_1, x1_2)
    inter_y1 = max(y1_1, y1_2)
    inter_x2 = min(x2_1, x2_2)
    inter_y2 = min(y2_1, y2_2)

    # Calculate intersection area
    inter_width = max(0, inter_x2 - inter_x1)
    inter_height = max(0, inter_y2 - inter_y1)
    intersection_area = inter_width * inter_height

    # Calculate individual box areas
    box1_area = box1.area()
    box2_area = box2.area()

    # Calculate union area
    union_area = box1_area + box2_area - intersection_area

    # Calculate IoU
    if union_area <= 0:
        # Avoid division by zero; no union means no overlap or zero-area boxes
        iou = 0.0
    else:
        iou = intersection_area / union_area
        # Clamp IoU to [0, 1] due to potential floating point inaccuracies
        iou = max(0.0, min(iou, 1.0))


    return iou
