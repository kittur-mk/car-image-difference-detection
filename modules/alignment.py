import cv2
import numpy as np


def align_images(oem_image, asset_image):
    """
    Align Asset image to OEM image using ORB feature matching and homography.
    
    Args:
        oem_image: Reference OEM image
        asset_image: Image to be aligned
    
    Returns:
        aligned_asset: Aligned asset image
        homography_matrix: Transformation matrix
    """
    # Convert to grayscale
    gray_oem = cv2.cvtColor(oem_image, cv2.COLOR_BGR2GRAY)
    gray_asset = cv2.cvtColor(asset_image, cv2.COLOR_BGR2GRAY)
    
    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=500)
    
    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(gray_oem, None)
    kp2, des2 = orb.detectAndCompute(gray_asset, None)
    
    # Match features using BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Take top 10% matches
    num_matches = max(10, len(matches) // 10)
    good_matches = matches[:num_matches]
    
    if len(good_matches) < 4:
        # Not enough matches, return original asset image
        return asset_image, None
    
    # Extract matched points
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    # Find homography matrix
    homography_matrix, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    
    if homography_matrix is None:
        return asset_image, None
    
    # Warp asset image to align with OEM
    aligned_asset = cv2.warpPerspective(asset_image, homography_matrix, (oem_image.shape[1], oem_image.shape[0]))
    
    return aligned_asset, homography_matrix