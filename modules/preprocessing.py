import cv2


def preprocess_image(image):
    """
    Resize image and remove noise
    """

    # Resize for uniform comparison
    image = cv2.resize(image, (800, 600))

    # Apply Gaussian blur to remove noise
    image = cv2.GaussianBlur(image, (5, 5), 0)

    return image


def normalize_lighting(image):
    """
    Normalize brightness differences
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Histogram Equalization
    gray = cv2.equalizeHist(gray)

    return gray