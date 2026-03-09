def identify_part(x, y, w, h, image_shape):

    height, width = image_shape[:2]

    # Center of bounding box
    cx = x + w / 2
    cy = y + h / 2

    # ----------------------
    # FRONT AREA
    # ----------------------
    if cy < height * 0.35:

        if cx < width * 0.3:
            return "Left Headlight"

        elif cx > width * 0.7:
            return "Right Headlight"

        else:
            return "Front Grille"

    # ----------------------
    # MIDDLE AREA
    # ----------------------
    elif cy < height * 0.65:

        if cx < width * 0.3:
            return "Left Wheel"

        elif cx > width * 0.7:
            return "Right Wheel"

        else:
            return "Door / Side Panel"

    # ----------------------
    # REAR AREA
    # ----------------------
    else:

        if cx < width * 0.3:
            return "Left Tail Lamp"

        elif cx > width * 0.7:
            return "Right Tail Lamp"

        else:
            return "Rear Bumper"