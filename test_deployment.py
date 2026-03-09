#!/usr/bin/env python3
"""
Test script to verify the Car Image Difference Detection System dependencies
and basic functionality before deployment.
"""

import sys
import importlib

def test_imports():
    """Test all required imports."""
    required_modules = [
        'streamlit',
        'cv2',  # OpenCV
        'numpy',
        'skimage',  # scikit-image
        'ultralytics',
        'PIL',  # Pillow
        'torch',
        'matplotlib'
    ]
    
    print("Testing required imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"OK {module}")
        except ImportError as e:
            print(f"ERROR {module}: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_yolo_model():
    """Test YOLOv8 model loading."""
    try:
        from ultralytics import YOLO
        print("Testing YOLOv8 model loading...")
        model = YOLO("yolov8n.pt")
        print("✅ YOLOv8 model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ YOLOv8 model loading failed: {e}")
        return False

def test_opencv():
    """Test OpenCV functionality."""
    try:
        import cv2
        import numpy as np
        
        # Create a test image
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        test_img[:, :, 0] = 255  # Blue channel
        
        # Test basic operations
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(test_img, (50, 50))
        
        print("✅ OpenCV basic operations working")
        return True
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Car Image Difference Detection System - Deployment Test")
    print("=" * 50)
    
    # Test imports
    failed_imports = test_imports()
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        print("Please install missing dependencies:")
        for module in failed_imports:
            print(f"  pip install {module}")
        sys.exit(1)
    
    # Test OpenCV
    opencv_ok = test_opencv()
    
    # Test YOLO
    yolo_ok = test_yolo_model()
    
    print("\n" + "=" * 50)
    if failed_imports or not opencv_ok or not yolo_ok:
        print("❌ Deployment test FAILED")
        print("Please fix the issues above before deploying.")
        sys.exit(1)
    else:
        print("✅ Deployment test PASSED")
        print("Your application is ready for deployment!")
        print("\nNext steps:")
        print("1. Choose your deployment platform (Streamlit Cloud recommended)")
        print("2. Follow the deployment instructions in DEPLOYMENT.md")
        print("3. Test your deployed application")
    
    print("=" * 50)

if __name__ == "__main__":
    main()