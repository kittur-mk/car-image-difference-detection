import cv2
import numpy as np
from modules.part_mapper import identify_part


def draw_differences(image, comparison_results):
    """
    Draw red bounding boxes around detected differences on the image.
    
    Args:
        image: The image to draw on
        comparison_results: Dictionary of comparison results with bounding boxes
    
    Returns:
        result: Image with red bounding boxes drawn
        changed_parts: List of changed part names and descriptions
    """
    # Ensure image is a numpy array
    if isinstance(image, cv2.UMat):
        image = image.get()
    
    # Ensure image is not a tuple (debugging the persistent issue)
    if isinstance(image, tuple):
        print(f"ERROR: draw_differences received a tuple instead of image: {image}")
        return None, []
    
    result = image.copy()
    changed_parts = []
    
    # Draw bounding boxes for changed parts
    for part_name, results in comparison_results.items():
        for result_data in results:
            if result_data['status'] != 'Same':
                # Get bounding box
                x, y, w, h = result_data['oem_bbox']
                
                # Draw red bounding box
                cv2.rectangle(
                    result,
                    (x, y),
                    (x + w, y + h),
                    (0, 0, 255),  # Red color
                    2
                )
                
                # Label the part with status
                label = f"{part_name} {result_data['status']}"
                cv2.putText(
                    result,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),  # Red color
                    2
                )
                
                # Add to changed parts list
                changed_parts.append({
                    'part': part_name,
                    'status': result_data['status'],
                    'similarity': result_data['combined_similarity']
                })

    return result, changed_parts


def generate_visual_report(oem_image, asset_image, result_image, changed_parts, overall_similarity):
    """
    Generate a comprehensive visual report.
    
    Args:
        oem_image: OEM image
        asset_image: Asset image
        result_image: Image with differences highlighted
        changed_parts: List of changed parts
        overall_similarity: Overall similarity score
    
    Returns:
        report_image: Combined report image
    """
    # Create a blank canvas for the report
    h, w = oem_image.shape[:2]
    
    # Create report layout: 2 rows, 2 columns
    report_h = h * 2
    report_w = w * 2
    report_image = np.zeros((report_h, report_w, 3), dtype=np.uint8)
    
    # Add white background
    report_image.fill(255)
    
    # Place OEM image (top-left)
    report_image[0:h, 0:w] = oem_image
    
    # Place Asset image (top-right)
    report_image[0:h, w:w*2] = asset_image
    
    # Place result image (bottom-left)
    report_image[h:h*2, 0:w] = result_image
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (0, 0, 0)  # Black text
    
    cv2.putText(report_image, "OEM Image", (10, 30), font, font_scale, color, thickness)
    cv2.putText(report_image, "Asset Image", (w + 10, 30), font, font_scale, color, thickness)
    cv2.putText(report_image, "Detected Differences", (10, h + 30), font, font_scale, color, thickness)
    
    # Add similarity score (bottom-right)
    similarity_text = f"Overall Similarity: {overall_similarity:.1%}"
    cv2.putText(report_image, similarity_text, (w + 10, h + 30), font, font_scale, color, thickness)
    
    # Add changed parts list (bottom section)
    y_offset = h + 80
    if changed_parts:
        cv2.putText(report_image, "Changed Parts:", (w + 10, y_offset), font, font_scale, color, thickness)
        y_offset += 40
        
        for i, part in enumerate(changed_parts[:10]):  # Show max 10 parts
            part_text = f"• {part['part']}: {part['status']} ({part['similarity']:.1%})"
            cv2.putText(report_image, part_text, (w + 30, y_offset + i * 30), font, 0.7, color, 1)
    else:
        cv2.putText(report_image, "No design differences detected", (w + 10, y_offset), font, font_scale, color, thickness)
    
    return report_image


def detect_differences(original, diff):
    """
    Detect differences between two images.
    
    Args:
        original: The original image
        diff: The difference image
    
    Returns:
        result: Image with differences highlighted
        differences: List of bounding boxes for differences
    """
    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    result = original.copy()

    differences = []

    for c in contours:

        if cv2.contourArea(c) > 100:

            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            differences.append((x, y, w, h))

    return result, differences
