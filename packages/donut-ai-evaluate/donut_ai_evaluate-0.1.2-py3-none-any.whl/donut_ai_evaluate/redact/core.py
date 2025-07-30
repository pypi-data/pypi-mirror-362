import numpy as np
import cv2
from typing import List
from donut_ai_evaluate._common.eval_logger import logger
from .models import Bbox ,BboxDataType
from .utils import calculate_iou

# --- Basic Logging Setup ---
# Configure logging to output info level messages by default

def _compare_bbox_lists_old(
    reference_raw_bboxes: List[BboxDataType],
    comparison_raw_bboxes: List[BboxDataType],
    iou_threshold: float = 0.7
) -> List[bool]:
    """
    Checks, for *each* bounding box in the reference list, if it has at least one
    sufficiently overlapping bounding box in the comparison list based on IoU.

    Accepts lists of [x, y, w, h] coordinates and returns a list of booleans.

    Args:
        reference_raw_bboxes: A list of lists, where each inner list contains
                              [x, y, w, h] for a reference bounding box.
        comparison_raw_bboxes: A list of lists, where each inner list contains
                               [x, y, w, h] for a comparison bounding box.
        iou_threshold: The minimum IoU score required to consider two bounding
                       boxes as overlapping sufficiently. Must be between 0.0
                       and 1.0. Defaults to 0.7.

    Returns:
        A list of booleans, with the same length as `reference_raw_bboxes`.
        Each boolean indicates whether the corresponding reference bounding box
        found at least one match in `comparison_raw_bboxes` meeting the
        `iou_threshold`.
        Returns an empty list if `reference_raw_bboxes` is empty.

    Raises:
        TypeError: If inputs are not lists, or if inner elements are not lists/tuples
                   of 4 numbers, or if numbers are invalid.
        ValueError: If `iou_threshold` is not between 0.0 and 1.0, or if bbox
                    dimensions derived are invalid (e.g., negative width/height).
    """
    # --- Input Validation ---
    if not isinstance(reference_raw_bboxes, list):
        raise TypeError(f"Expected 'reference_raw_bboxes' to be a list, but got {type(reference_raw_bboxes)}.")
    if not isinstance(comparison_raw_bboxes, list):
        raise TypeError(f"Expected 'comparison_raw_bboxes' to be a list, but got {type(comparison_raw_bboxes)}.")
    if not (0.0 <= iou_threshold <= 1.0):
        raise ValueError(f"iou_threshold must be between 0.0 and 1.0, but got {iou_threshold}.")

    # --- Convert Raw Data to Bbox Objects & Validate Inner Structure ---
    reference_bboxes: List[Bbox] = []
    comparison_bboxes: List[Bbox] = []

    try:
        for i, raw_box in enumerate(reference_raw_bboxes):
            # Bbox.from_xywh_list handles list/tuple check, length check, and numeric check
            reference_bboxes.append(Bbox.from_xywh_list(raw_box))
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid format in reference_raw_bboxes at index {i}: {raw_box}. Error: {e}", exc_info=True)
        raise TypeError(f"Invalid format in reference_raw_bboxes at index {i}: {raw_box}. Must be list/tuple of 4 numbers. Error: {e}") from e

    try:
        for i, raw_box in enumerate(comparison_raw_bboxes):
            comparison_bboxes.append(Bbox.from_xywh_list(raw_box))
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid format in comparison_raw_bboxes at index {i}: {raw_box}. Error: {e}", exc_info=True)
        raise TypeError(f"Invalid format in comparison_raw_bboxes at index {i}: {raw_box}. Must be list/tuple of 4 numbers. Error: {e}") from e

    # --- Core Logic ---
    logger.debug(f"Starting comparison: {len(reference_bboxes)} reference boxes vs "
                  f"{len(comparison_bboxes)} comparison boxes with IoU threshold {iou_threshold}.")

    match_results: List[bool] = []

    # If the reference list is empty, return an empty list
    if not reference_bboxes:
        logger.info("Reference Bbox list (derived) is empty. Returning empty list.")
        return []

    # Iterate through each (now converted) reference bounding box
    for ref_idx, ref_bbox in enumerate(reference_bboxes):
        found_match_for_current_ref = False
        highest_iou_for_ref = 0.0 # Optional: track highest IoU for debugging

        # If comparison list is empty, no matches are possible for any ref_box
        if not comparison_bboxes:
            found_match_for_current_ref = False
        else:
            # Compare it against every (converted) comparison bounding box
            for comp_idx, comp_bbox in enumerate(comparison_bboxes):
                try:
                    iou = calculate_iou(ref_bbox, comp_bbox)
                    highest_iou_for_ref = max(highest_iou_for_ref, iou) # Track max IoU found
                except Exception as e:
                    logger.error(f"Error calculating IoU between ref_bbox {ref_idx} ({ref_bbox}) "
                                 f"and comp_bbox {comp_idx} ({comp_bbox}): {e}", exc_info=True)
                    continue # Skip this comparison pair, treat as no match

                logger.debug(f"  IoU(Ref[{ref_idx}], Comp[{comp_idx}]) = {iou:.4f}")

                if iou >= iou_threshold:
                    logger.debug(f"    Match found for Ref[{ref_idx}] with Comp[{comp_idx}] (IoU={iou:.4f} >= {iou_threshold})")
                    found_match_for_current_ref = True
                    break # Found a match for this reference box, move to the next reference box

        # Log the outcome for the current reference box
        if not found_match_for_current_ref:
            logger.debug(f"No sufficient match found for reference Bbox {ref_idx}: {ref_bbox}. "
                         f"Max IoU found: {highest_iou_for_ref:.4f} (Threshold: {iou_threshold})")
        # Append the result for this reference box to the list
        match_results.append(found_match_for_current_ref)

    logger.info(f"Comparison finished. Results for {len(reference_bboxes)} reference boxes: {match_results}")
    return match_results


# --- Visual Comparison Function ---
def _compare_bbox_lists(
    reference_raw_bboxes: List[BboxDataType],
    comparison_raw_bboxes: List[BboxDataType],
    iou_threshold: float = 0.7,
    padding: int = 0# Add padding around the max coordinates for image size
) -> List[bool]:
    """
    Compares bounding boxes visually using pixel overlap via OpenCV.

    Checks, for *each* bounding box in the reference list, if its pixel area
    sufficiently overlaps with the pixel area of *any* bounding box in the
    comparison list. The overlap ratio is calculated as:
    (pixels in intersection) / (pixels in the reference bbox area).

    Args:
        reference_raw_bboxes: A list of lists, where each inner list contains
                              [x, y, w, h] for a reference bounding box.
                              Coordinates are expected to be usable as ints.
        comparison_raw_bboxes: A list of lists, where each inner list contains
                               [x, y, w, h] for a comparison bounding box.
                               Coordinates are expected to be usable as ints.
        iou_threshold: The minimum overlap ratio (intersection_pixels / reference_area_pixels)
                       required to consider a match. Must be between 0.0 and 1.0.
                       Defaults to 0.7.
        padding: Extra space added around the maximum coordinates to define
                 the image canvas size. Defaults to 10.

    Returns:
        A list of booleans, with the same length as `reference_raw_bboxes`.
        Each boolean indicates whether the corresponding reference bounding box
        found a sufficient pixel overlap match in `comparison_raw_bboxes`.
        Returns an empty list if `reference_raw_bboxes` is empty.

    Raises:
        TypeError: If inputs are not lists, or if inner elements are not lists/tuples
                   of 4 numbers.
        ValueError: If `iou_threshold` is not between 0.0 and 1.0, or if bbox
                    dimensions w or h are non-positive for a reference box.
                    Also raises if coordinates/dimensions are not valid numbers.
    """
    # --- Input Validation ---
    if not isinstance(reference_raw_bboxes, list):
        raise TypeError(f"Expected 'reference_raw_bboxes' to be a list, but got {type(reference_raw_bboxes)}.")
    if not isinstance(comparison_raw_bboxes, list):
        raise TypeError(f"Expected 'comparison_raw_bboxes' to be a list, but got {type(comparison_raw_bboxes)}.")
    if not (0.0 <= iou_threshold <= 1.0):
        raise ValueError(f"iou_threshold must be between 0.0 and 1.0, but got {iou_threshold}.")
    if not isinstance(padding, int) or padding < 0:
        raise ValueError(f"padding must be a non-negative integer, but got {padding}.")

    # --- Basic Inner Structure Validation & Calculate Image Dimensions ---
    max_x, max_y = 0, 0
    all_bboxes_raw = reference_raw_bboxes + comparison_raw_bboxes

    if not all_bboxes_raw:
        logger.info("Both reference and comparison lists are empty. Returning empty list.")
        # If reference is empty, result should be []; if only comparison is empty, proceed normally.
        return [] if not reference_raw_bboxes else [False] * len(reference_raw_bboxes)

    for i, raw_box in enumerate(all_bboxes_raw):
        if not isinstance(raw_box, (list, tuple)) or len(raw_box) != 4:
            raise TypeError(f"Invalid format at index {i} in combined list: {raw_box}. "
                            f"Must be list/tuple of 4 elements [x, y, w, h].")
        try:
            # Convert to float first for consistent type check, then int for coords
            fx, fy, fw, fh = map(float, raw_box)
            x, y, w, h = map(int, [fx, fy, fw, fh]) # Use int for pixel coords
            if fw < 0 or fh < 0:
                 # Check raw float width/height as int(negative) might become 0 misleadingly
                 raise ValueError(f"Negative dimensions found: w={fw}, h={fh} in box {raw_box}")

            current_max_x = x + w
            current_max_y = y + h
            max_x = max(max_x, current_max_x)
            max_y = max(max_y, current_max_y)
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid numeric data in bbox at index {i}: {raw_box}. Error: {e}", exc_info=True)
            raise TypeError(f"Invalid numeric data in bbox at index {i}: {raw_box}. Error: {e}") from e

    img_width = max_x # + padding
    img_height = max_y# + padding
    logger.debug(f"Calculated image dimensions: {img_width}x{img_height}")

    # --- Create Comparison Image (all comparison boxes drawn) ---
    comparison_image = np.zeros((img_height, img_width), dtype=np.uint8)
    for i, comp_raw_box in enumerate(comparison_raw_bboxes):
        try:
            # Re-extract and convert to int safely
            x, y, w, h = map(int, map(float, comp_raw_box))
            # Draw filled rectangle (white on black)
            # cv2.rectangle uses (pt1, pt2) -> (top-left, bottom-right)
            cv2.rectangle(comparison_image, (x, y), (x + w, y + h), 255, thickness=-1)
            logger.debug(f"Drew comparison box {i}: [{x},{y},{w},{h}]")
        except Exception as e:
             # Catch potential errors during drawing (e.g., huge coords) although unlikely after validation
             logger.error(f"Error drawing comparison box {i} ({comp_raw_box}): {e}", exc_info=True)
             # Depending on policy, you might skip or raise
             raise RuntimeError(f"Failed to draw comparison box {i}: {comp_raw_box}") from e

    # --- Iterate through Reference Boxes and Compare ---
    match_results: List[bool] = []

    if not reference_raw_bboxes:
        logger.info("Reference Bbox list is empty. Returning empty list.")
        return []

    for ref_idx, ref_raw_box in enumerate(reference_raw_bboxes):
        try:
            rx, ry, rw, rh = map(int, map(float, ref_raw_box))
        except (ValueError, TypeError) as e:
             # Should have been caught earlier, but for safety
             logger.error(f"Invalid data encountered again for ref box {ref_idx}: {ref_raw_box}. Error: {e}", exc_info=True)
             raise TypeError(f"Invalid data for ref box {ref_idx}: {ref_raw_box}") from e

        if rw <= 0 or rh <= 0:
            logger.warning(f"Reference box {ref_idx} ({ref_raw_box}) has non-positive dimensions (w={rw}, h={rh}). Treating as no match.")
            match_results.append(False)
            continue

        # Create a fresh image for the current reference box
        reference_image = np.zeros((img_height, img_width), dtype=np.uint8)

        # Draw the single reference box
        try:
            cv2.rectangle(reference_image, (rx, ry), (rx + rw, ry + rh), 255, thickness=-1)
        except Exception as e:
             logger.error(f"Error drawing reference box {ref_idx} ({ref_raw_box}): {e}", exc_info=True)
             raise RuntimeError(f"Failed to draw reference box {ref_idx}: {ref_raw_box}") from e


        # Calculate the pixel area of the reference box
        # For a simple rectangle, this is just w * h
        # ref_area_pixels = float(rw * rh) # Use float for division
        ref_area_pixels = float(cv2.countNonZero(reference_image))

        # Perform bitwise AND to find the intersection pixels
        intersection_image = cv2.bitwise_and(reference_image, comparison_image)

        # Count non-zero pixels in the intersection image
        overlap_pixels = float(cv2.countNonZero(intersection_image))

        # Calculate the overlap score (ratio)
        # ref_area_pixels check above ensures it's > 0 here
        if ref_area_pixels > 0:
            score = overlap_pixels / ref_area_pixels
            logger.debug(f"    Overlap Pixels={overlap_pixels}, Score={score:.4f}")
        else:
            # Avoid division by zero if reference area is 0 pixels
            score = 0.0
            logger.debug(f"    Reference area is 0 pixels, overlap score set to 0.0")

        # Compare score with threshold
        is_match = score >= iou_threshold
        match_results.append(is_match)
        logger.debug(f"    Match found: {is_match} (Threshold: {iou_threshold})")

        # --- Optional: Visualization for Debugging ---
        # if True: # Or set a debug flag
        #     # Create copies to draw outlines without modifying original masks
        #     vis_ref = cv2.cvtColor(reference_image, cv2.COLOR_GRAY2BGR)
        #     vis_comp = cv2.cvtColor(comparison_image, cv2.COLOR_GRAY2BGR)
        #     vis_intersect = cv2.cvtColor(intersection_image, cv2.COLOR_GRAY2BGR)
        #
        #     # Draw outlines for clarity (optional)
        #     cv2.rectangle(vis_ref, (rx, ry), (rx + rw, ry + rh), (0, 255, 0), 1) # Green outline on ref
        #     for cb in comparison_raw_bboxes:
        #         cx, cy, cw, ch = map(int, map(float, cb))
        #         cv2.rectangle(vis_comp, (cx, cy), (cx + cw, cy + ch), (0, 0, 255), 1) # Red outline on comp
        #
        #     # Combine for display
        #     white_line = np.ones((vis_ref.shape[0], 1, 3), dtype=np.uint8) * 255  # 255 for white
        #
        #     # Combine the images with a white line in between
        #     combined_vis = np.hstack((vis_ref, white_line, vis_comp, white_line, vis_intersect))
        #     # combined_vis = np.hstack((vis_ref, vis_comp, vis_intersect))
        #     win_name = f'Ref {ref_idx} vs All Comp (Score: {score:.2f})'
        #     cv2.imwrite(f"Data/{win_name}.png", combined_vis)
        # cv2.imshow(win_name, combined_vis)
        # cv2.waitKey(0) # Press any key to continue to next ref box
        # cv2.destroyWindow(win_name)
        # -------- End Optional Visualization --------

    logger.info(f"Visual comparison finished. Results for {len(reference_raw_bboxes)} reference boxes: {match_results}")
    return match_results










# --- Specific Wrapper Functions ---

def is_gt_field_redacted(
    gt_fields_raw: List[BboxDataType],
    ai_fields_raw: List[BboxDataType],
    iou_threshold: float = 0.7
) -> List[bool]:
    """
    Checks, for *each* ground truth (GT) bounding box, if it has at least one
    sufficiently overlapping AI bounding box. Accepts lists of [x, y, w, h].

    Args:
        gt_fields_raw: List of GT boxes, each as [x, y, w, h].
        ai_fields_raw: List of AI boxes, each as [x, y, w, h].
        iou_threshold: Minimum IoU for a match. Defaults to 0.7.

    Returns:
        A list of booleans, one for each GT box, indicating if it was matched
        by at least one AI box.

    Raises:
        TypeError: If inputs are not lists or contain invalid bbox data.
        ValueError: If `iou_threshold` is invalid or bbox dimensions are invalid.
    """
    logger.info("Checking coverage: GT fields vs AI fields...")
    try:
        # GT fields are the reference - check each one for a match in AI fields
        results = _compare_bbox_lists(
            reference_raw_bboxes=gt_fields_raw,
            comparison_raw_bboxes=ai_fields_raw,
            iou_threshold=iou_threshold
        )
        logger.info(f"Result of is_gt_field_redacted (per GT box): {results}")
        return results
    except (TypeError, ValueError) as e:
        logger.error(f"Error during is_gt_field_redacted: {e}", exc_info=False) # Log concise error
        raise # Re-raise the exception
    except Exception as e:
        logger.error(f"Unexpected error in is_gt_field_redacted: {e}", exc_info=True)
        raise

def is_redacted_field_gt(
    ai_fields_raw: List[BboxDataType],
    gt_fields_raw: List[BboxDataType],
    iou_threshold: float = 0.7
) -> List[bool]:
    """
    Checks, for *each* AI-detected bounding box, if it corresponds to
    (sufficiently overlaps with) at least one ground truth (GT) bounding box.
    Accepts lists of [x, y, w, h].

    Args:
        ai_fields_raw: List of AI boxes, each as [x, y, w, h].
        gt_fields_raw: List of GT boxes, each as [x, y, w, h].
        iou_threshold: Minimum IoU for a match. Defaults to 0.7.

    Returns:
        A list of booleans, one for each AI box, indicating if it matched
        at least one GT box (helps identify potential false positives).

    Raises:
        TypeError: If inputs are not lists or contain invalid bbox data.
        ValueError: If `iou_threshold` is invalid or bbox dimensions are invalid.
    """
    logger.info("Checking correspondence: AI fields vs GT fields...")
    try:
        # AI fields are the reference - check each one for a match in GT fields
        results = _compare_bbox_lists(
            reference_raw_bboxes=ai_fields_raw,
            comparison_raw_bboxes=gt_fields_raw,
            iou_threshold=iou_threshold
        )
        logger.info(f"Result of is_redacted_field_gt (per AI box): {results}")
        return results
    except (TypeError, ValueError) as e:
        logger.error(f"Error during is_redacted_field_gt: {e}", exc_info=False) # Log concise error
        raise # Re-raise the exception
    except Exception as e:
        logger.error(f"Unexpected error in is_redacted_field_gt: {e}", exc_info=True)
        raise

