import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def compare_images(oem_img, asset_img):
    """
    Compare OEM and Asset images to detect visual differences.
    
    Args:
        oem_img: OEM image (numpy array)
        asset_img: Asset image (numpy array)
    
    Returns:
        similarity_score: SSIM similarity score (0-1)
        diff_map: Difference map
        boxes: List of bounding boxes for differences
    """
    # Resize images to same dimension
    h, w = oem_img.shape[:2]
    asset_img_resized = cv2.resize(asset_img, (w, h))
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(oem_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(asset_img_resized, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM
    score, diff = ssim(gray1, gray2, full=True)
    
    # Convert difference map to uint8
    diff_map = (diff * 255).astype("uint8")
    
    # Threshold the difference map
    thresh = cv2.threshold(
        diff_map, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]
    
    # Morphological operations to clean up noise
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    boxes = []
    
    for c in contours:
        # Only consider contours larger than threshold to avoid noise
        if cv2.contourArea(c) > 150:
            x, y, w, h = cv2.boundingRect(c)
            boxes.append((x, y, w, h))
    
    return score, diff_map, boxes
