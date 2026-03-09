import cv2
import numpy as np

def align_images(oem, asset):
    """
    Align the asset image to the OEM image using ORB feature matching and homography.
    
    Args:
        oem: OEM image (numpy array)
        asset: Asset image (numpy array)
    
    Returns:
        aligned_asset: Asset image aligned to OEM perspective
    """
    # Convert to grayscale
    gray1 = cv2.cvtColor(oem, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(asset, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create(4000)

    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    # Match features using brute force matcher
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Take top 200 matches
    matches = matches[:200]

    # Extract matched points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Find homography matrix
    H, _ = cv2.findHomography(pts2, pts1, cv2.RANSAC)

    # Apply perspective transformation
    aligned_asset = cv2.warpPerspective(asset, H, (oem.shape[1], oem.shape[0]))

    return aligned_asset