import streamlit as st
import numpy as np

# Handle OpenCV import with fallback
try:
    import cv2
except ImportError:
    st.error("OpenCV (cv2) is not installed. Please install it with: pip install opencv-python")
    st.stop()

# Import other modules
try:
    from modules.preprocessing import preprocess_image
    from modules.detection import crop_car
    from modules.alignment import align_images
    from modules.part_detection import CarPartDetector
    from modules.part_comparison import PartComparator, compare_parts, draw_part_bounding_boxes
    from modules.report import draw_differences, generate_visual_report
    from modules.part_mapper import identify_part
    from modules.difference_detector import detect_differences
    from modules.image_alignment import align_images as align_images_orb
    from modules.car_parts import get_car_parts
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()


st.set_page_config(layout="wide")
st.title("🚗 AI Car Design Difference Detection (High Accuracy)")


# ==========================
# IMAGE LOADING FUNCTION
# ==========================

def load_image(uploaded_file):
    """Load uploaded image file."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


# ==========================
# HIGH ACCURACY PART-LEVEL DIFFERENCE DETECTION
# ==========================

def process_oem_asset_comparison(oem_file, asset_file, view_name):
    """
    Compare OEM and Asset images using SSIM-based difference detection.
    
    Args:
        oem_file: Uploaded OEM image file
        asset_file: Uploaded Asset image file
        view_name: Name of the view (e.g., "Front View Comparison")
    """
    if oem_file is None or asset_file is None:
        st.warning(f"Please upload both OEM and Asset images for {view_name}")
        return

    st.subheader(view_name)

    # Load images
    oem_img = load_image(oem_file)
    asset_img = load_image(asset_file)

    # Preprocess images
    oem_img = preprocess_image(oem_img)
    asset_img = preprocess_image(asset_img)

    # Detect car and crop
    car_oem, conf_oem = crop_car(oem_img)
    car_asset, conf_asset = crop_car(asset_img)

    st.write("OEM Car Detection Confidence:", round(conf_oem, 3))
    st.write("Asset Car Detection Confidence:", round(conf_asset, 3))

    # Align images for better accuracy
    st.write("Aligning images for optimal comparison...")
    aligned_asset, homography = align_images(car_oem, car_asset)
    
    if homography is None:
        st.warning("Image alignment failed, using original images")
        aligned_asset = car_asset

    # Compare images using SSIM and detect differences
    st.write("Comparing images using SSIM...")
    ssim_result_image, similarity_score, detected_changes = detect_differences(car_oem, aligned_asset)

    # Display results in the requested format
    
    # Section 1 – Input Images
    st.write("### Section 1 – Input Images")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(car_oem, caption="OEM Image", channels="BGR")
    
    with col2:
        st.image(aligned_asset, caption="Asset Image", channels="BGR")

    # Section 2 – Difference Result
    st.write("### Section 2 – Difference Result")
    st.image(ssim_result_image, caption="OEM Image with Red Bounding Boxes", channels="BGR")

    # Section 3 – Detected Changes
    st.write("### Section 3 – Detected Changes")
    if detected_changes:
        for change in detected_changes:
            st.write(f"• {change}")
    else:
        st.write("• No significant changes detected")

    # Section 4 – Similarity Score
    st.write("### Section 4 – Similarity Score")
    st.write(f"{similarity_score:.1f}%")


# ==========================
# FILE UPLOAD SECTION
# ==========================

st.header("Upload OEM Images")
oem_front = st.file_uploader("OEM Angular Front", key="oem_front")
oem_rear = st.file_uploader("OEM Angular Rear", key="oem_rear")
oem_side = st.file_uploader("OEM Side View", key="oem_side")

st.header("Upload Asset Images")
asset_front = st.file_uploader("Asset Angular Front", key="asset_front")
asset_rear = st.file_uploader("Asset Angular Rear", key="asset_rear")
asset_side = st.file_uploader("Asset Side View", key="asset_side")




# ==========================
# NEW ENHANCED COMPARISON WITH IMAGE ALIGNMENT AND HUMAN-READABLE EXPLANATIONS
# ==========================

def load_image(file):
    """Load uploaded image file."""
    bytes_data = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)
    return img

def enhanced_process_oem_asset_comparison(oem_file, asset_file, view_name):
    """
    Enhanced comparison with image alignment and human-readable explanations.
    """
    if oem_file is None or asset_file is None:
        st.warning(f"Please upload both OEM and Asset images for {view_name}")
        return

    st.subheader(view_name)

    # Load images
    oem = load_image(oem_file)
    asset = load_image(asset_file)

    # Determine view type based on view_name
    if "Front" in view_name or "front" in view_name:
        view_type = "front"
    elif "Rear" in view_name or "rear" in view_name:
        view_type = "rear"
    elif "Side" in view_name or "side" in view_name:
        view_type = "side"
    else:
        view_type = "front"

    # Align images using ORB feature matching (Very Important)
    st.write("Aligning images using ORB feature matching...")
    asset_aligned = align_images_orb(oem, asset)

    # Display aligned images
    st.subheader("Aligned Images")
    col1, col2 = st.columns(2)
    col1.image(oem, caption="OEM Image", channels="BGR")
    col2.image(asset_aligned, caption="Aligned Asset Image", channels="BGR")

    # Get car parts for comparison based on view type
    oem_parts = get_car_parts(oem, view_type)
    asset_parts = get_car_parts(asset_aligned, view_type)

    # Compare parts and generate explanations
    changes = compare_parts(oem_parts, asset_parts)

    # Draw red bounding boxes around detected differences
    bounding_box_image = draw_part_bounding_boxes(oem, oem_parts, asset_parts)

    # Display detected changes with human-readable explanations
    st.subheader("Detected Changes")

    if changes:
        for change in changes:
            st.write(f"• {change}")
    else:
        st.write("No major design differences detected")

    # Display OEM image with red bounding boxes
    st.subheader("Visual Difference Detection (Part-based)")
    st.image(bounding_box_image, caption="OEM Image with Red Bounding Boxes", channels="BGR")

    # Also run the original SSIM-based comparison for additional visual detection
    st.write("### Visual Difference Detection (SSIM-based)")
    ssim_result_image, similarity_score, detected_changes = detect_differences(oem, asset_aligned)
    st.image(ssim_result_image, caption="OEM Image with Red Bounding Boxes (SSIM)", channels="BGR")
    st.write(f"Similarity Score: {similarity_score:.1f}%")


# ==========================
# RUN COMPARISON
# ==========================

if st.button("Compare Cars"):
    st.write("### Front View Comparison")
    enhanced_process_oem_asset_comparison(oem_front, asset_front, "Angular Front")
    
    st.write("### Rear View Comparison")
    enhanced_process_oem_asset_comparison(oem_rear, asset_rear, "Angular Rear")
    
    st.write("### Side View Comparison")
    enhanced_process_oem_asset_comparison(oem_side, asset_side, "Side View")
