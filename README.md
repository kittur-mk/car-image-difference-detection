# Car Image Difference Detection System

An AI-powered web application that detects and visualizes differences between OEM and Asset car images using computer vision and deep learning techniques.

## Features

- **Multi-View Support**: Compare Front, Rear, and Side view images
- **AI-Powered Detection**: Uses YOLOv8 for car detection and cropping
- **SSIM-Based Comparison**: Structural Similarity Index for accurate difference detection
- **Part-Level Analysis**: Component-wise comparison with bounding box visualization
- **Human-Readable Reports**: Clear explanations of detected changes
- **Streamlit Interface**: User-friendly web application

## Demo

The application provides a comprehensive comparison interface with:
- Input image display
- Difference visualization with red bounding boxes
- Detected changes list
- Similarity scoring (0-100%)

## Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/car-image-difference-detection.git
cd car-image-difference-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Upload OEM images (Angular Front, Angular Rear, Side View)
2. Upload corresponding Asset images
3. Click "Compare Cars" to process
4. View results with visualizations and similarity scores

## Project Structure

```
car-image-difference-detection/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── modules/                 # Core modules
    ├── preprocessing.py     # Image preprocessing
    ├── detection.py         # Car detection with YOLOv8
    ├── alignment.py         # Image alignment
    ├── part_detection.py    # Car part detection
    ├── part_comparison.py   # Part-level comparison
    ├── difference_detector.py # SSIM-based difference detection
    ├── image_alignment.py   # ORB feature matching alignment
    ├── car_parts.py         # Car part definitions
    ├── part_mapper.py       # Part identification
    ├── report.py           # Report generation
    └── __init__.py
```

## Deployment Options

### 1. Streamlit Cloud (Recommended)

1. Create a free account at [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Configure the app (Python version, requirements.txt)
4. Deploy automatically

### 2. Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```
3. Create `runtime.txt`:
```
python-3.10.12
```
4. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### 3. Docker

1. Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

2. Build and run:
```bash
docker build -t car-difference-detector .
docker run -p 8501:8501 car-difference-detector
```

## Dependencies

- **Streamlit**: Web framework for the UI
- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical computations
- **scikit-image**: SSIM calculation and image analysis
- **ultralytics**: YOLOv8 model for object detection

## Technical Details

### Image Processing Pipeline

1. **Preprocessing**: Resize, normalize, and enhance images
2. **Detection**: Use YOLOv8 to detect and crop cars
3. **Alignment**: Align images using feature matching
4. **Comparison**: Calculate SSIM and detect differences
5. **Visualization**: Draw bounding boxes around differences

### Accuracy Features

- **Multi-algorithm approach**: Combines SSIM and part-level analysis
- **Image alignment**: Ensures accurate comparison
- **Confidence scoring**: Provides similarity percentages
- **Visual feedback**: Clear bounding box visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create a GitHub issue
- Check the documentation
- Review the code comments

## Future Enhancements

- [ ] Mobile app version
- [ ] Batch processing support
- [ ] PDF report generation
- [ ] API endpoints for integration
- [ ] Advanced ML models for better accuracy
- [ ] Real-time video processing