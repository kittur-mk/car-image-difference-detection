import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def align_images(oem, asset):

    gray1 = cv2.cvtColor(oem, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(asset, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(5000)

    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

    H, _ = cv2.findHomography(pts2, pts1, cv2.RANSAC,5.0)

    aligned_asset = cv2.warpPerspective(asset, H, (oem.shape[1], oem.shape[0]))

    return aligned_asset


def detect_differences(oem_img, asset_img):

    oem_img = cv2.resize(oem_img,(800,600))
    asset_img = cv2.resize(asset_img,(800,600))

    # Align images
    asset_img = align_images(oem_img, asset_img)

    gray_oem = cv2.cvtColor(oem_img, cv2.COLOR_BGR2GRAY)
    gray_asset = cv2.cvtColor(asset_img, cv2.COLOR_BGR2GRAY)

    score, diff = ssim(gray_oem, gray_asset, full=True)

    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(
        diff,
        0,
        255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]

    kernel = np.ones((5,5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    result = oem_img.copy()

    boxes = []

    for c in contours:

        area = cv2.contourArea(c)

        if area < 1500:
            continue

        x,y,w,h = cv2.boundingRect(c)

        boxes.append((x,y,w,h))

        cv2.rectangle(
            result,
            (x,y),
            (x+w,y+h),
            (0,0,255),
            3
        )

    similarity = round(score*100,2)

    return result, similarity, boxes