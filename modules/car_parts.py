def get_car_parts(image, view_type="front"):
    """
    Define logical car part regions for comparison based on view angle.
    
    Args:
        image: Input image (numpy array)
        view_type: Type of view ("front", "rear", "side")
    
    Returns:
        parts: Dictionary of car part regions
    """
    h, w = image.shape[:2]

    if view_type == "front":
        # Front view specific regions
        parts = {
            "Front Grille": image[int(h*0.35):int(h*0.55), int(w*0.25):int(w*0.55)],
            "Left Headlight": image[int(h*0.30):int(h*0.45), int(w*0.15):int(w*0.35)],
            "Right Headlight": image[int(h*0.30):int(h*0.45), int(w*0.60):int(w*0.80)],
            "Left Wheel": image[int(h*0.55):int(h*0.85), int(w*0.15):int(w*0.35)],
            "Right Wheel": image[int(h*0.55):int(h*0.85), int(w*0.60):int(w*0.80)],
            "Front Bumper": image[int(h*0.55):int(h*0.75), int(w*0.25):int(w*0.60)],
            "Hood": image[int(h*0.20):int(h*0.40), int(w*0.25):int(w*0.60)]
        }
    elif view_type == "rear":
        # Rear view specific regions
        parts = {
            "Rear Bumper": image[int(h*0.60):int(h*0.80), int(w*0.25):int(w*0.60)],
            "Left Tail Light": image[int(h*0.40):int(h*0.55), int(w*0.15):int(w*0.35)],
            "Right Tail Light": image[int(h*0.40):int(h*0.55), int(w*0.60):int(w*0.80)],
            "Left Rear Wheel": image[int(h*0.55):int(h*0.85), int(w*0.15):int(w*0.35)],
            "Right Rear Wheel": image[int(h*0.55):int(h*0.85), int(w*0.60):int(w*0.80)],
            "Trunk": image[int(h*0.25):int(h*0.45), int(w*0.25):int(w*0.60)],
            "Rear Window": image[int(h*0.15):int(h*0.35), int(w*0.20):int(w*0.70)]
        }
    elif view_type == "side":
        # Side view specific regions
        parts = {
            "Front Wheel": image[int(h*0.55):int(h*0.85), int(w*0.10):int(w*0.30)],
            "Rear Wheel": image[int(h*0.55):int(h*0.85), int(w*0.60):int(w*0.80)],
            "Door": image[int(h*0.40):int(h*0.70), int(w*0.30):int(w*0.60)],
            "Side Mirror": image[int(h*0.30):int(h*0.45), int(w*0.05):int(w*0.20)],
            "Fender": image[int(h*0.35):int(h*0.55), int(w*0.15):int(w*0.40)],
            "Rear Fender": image[int(h*0.35):int(h*0.55), int(w*0.55):int(w*0.80)],
            "Side Window": image[int(h*0.20):int(h*0.45), int(w*0.30):int(w*0.70)]
        }
    else:
        # Default front view
        parts = {
            "Front Grille": image[int(h*0.35):int(h*0.55), int(w*0.25):int(w*0.55)],
            "Left Headlight": image[int(h*0.30):int(h*0.45), int(w*0.15):int(w*0.35)],
            "Right Headlight": image[int(h*0.30):int(h*0.45), int(w*0.60):int(w*0.80)],
            "Left Wheel": image[int(h*0.55):int(h*0.85), int(w*0.15):int(w*0.35)],
            "Right Wheel": image[int(h*0.55):int(h*0.85), int(w*0.60):int(w*0.80)],
            "Front Bumper": image[int(h*0.55):int(h*0.75), int(w*0.25):int(w*0.60)],
            "Hood": image[int(h*0.20):int(h*0.40), int(w*0.25):int(w*0.60)]
        }

    return parts
