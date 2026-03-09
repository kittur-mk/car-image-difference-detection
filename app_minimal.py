#!/usr/bin/env python3
"""
Minimal app for Streamlit Cloud deployment with dependency installation.
This app will install missing dependencies and then redirect to the main app.
"""

import streamlit as st
import sys
import subprocess
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'opencv-python',
        'numpy', 
        'pillow',
        'matplotlib',
        'requests',
        'scikit-image',
        'ultralytics',
        'torch',
        'torchvision'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    st.set_page_config(layout="wide")
    st.title("🔧 Car Image Difference Detection - Setup")
    
    st.write("Checking dependencies...")
    
    missing = check_dependencies()
    
    if missing:
        st.warning(f"Missing packages: {', '.join(missing)}")
        st.write("Installing missing dependencies...")
        
        for package in missing:
            with st.spinner(f"Installing {package}..."):
                if install_package(package):
                    st.success(f"✅ {package} installed successfully")
                else:
                    st.error(f"❌ Failed to install {package}")
        
        st.rerun()
    else:
        st.success("✅ All dependencies are installed!")
        
        # Try to import cv2 to verify it works
        try:
            import cv2
            st.success(f"✅ OpenCV version: {cv2.__version__}")
        except ImportError:
            st.error("❌ OpenCV import failed even after installation")
            return
        
        st.write("Redirecting to main application...")
        
        # Import and run the main app
        try:
            import app
            # The main app will run automatically since we imported it
        except Exception as e:
            st.error(f"Error loading main app: {e}")
            st.write("Please refresh the page or contact support.")

if __name__ == "__main__":
    main()