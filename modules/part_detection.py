import cv2
import numpy as np
from ultralytics import YOLO


class CarPartDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Initialize car part detector.
        
        Args:
            model_path: Path to YOLO model for car parts detection
        """
        # Try to load car parts model, fallback to general model
        try:
            self.model = YOLO(model_path)
        except:
            # Use general YOLO model if car parts model not available
            self.model = YOLO("yolov8n.pt")
        
        # Car parts we want to detect
        self.target_parts = [
            'wheel', 'headlight', 'taillight', 'door', 
            'mirror', 'grille', 'bumper', 'hood', 'logo', 'window'
        ]
        
        # Part confidence threshold
        self.confidence_threshold = 0.5
    
    def detect_parts(self, image):
        """
        Detect car parts in the image.
        
        Args:
            image: Input image
        
        Returns:
            parts: Dictionary of detected parts with bounding boxes
        """
        # Run YOLO detection
        results = self.model(image, conf=self.confidence_threshold)
        
        parts = {}
        
        # Process detection results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get class name and confidence
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = result.names[class_id]
                
                # Check if it's a car part we're interested in
                if class_name.lower() in self.target_parts:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Convert to integer coordinates
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Filter out very small detections
                    area = (x2 - x1) * (y2 - y1)
                    if area < 500:  # Minimum area threshold
                        continue
                    
                    # Store part information
                    part_info = {
                        'name': class_name,
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence,
                        'area': area
                    }
                    
                    # Use part name as key, append if multiple detections
                    if class_name not in parts:
                        parts[class_name] = []
                    parts[class_name].append(part_info)
        
        return parts
    
    def crop_parts(self, image, parts):
        """
        Crop detected parts from the image.
        
        Args:
            image: Input image
            parts: Dictionary of detected parts
        
        Returns:
            cropped_parts: Dictionary of cropped part images
        """
        cropped_parts = {}
        
        for part_name, part_list in parts.items():
            cropped_parts[part_name] = []
            
            for part_info in part_list:
                x1, y1, x2, y2 = part_info['bbox']
                
                # Crop the part region
                cropped = image[y1:y2, x1:x2]
                
                # Ensure minimum size
                if cropped.shape[0] > 10 and cropped.shape[1] > 10:
                    cropped_parts[part_name].append({
                        'image': cropped,
                        'bbox': (x1, y1, x2-x1, y2-y1),  # Convert to (x, y, w, h)
                        'confidence': part_info['confidence']
                    })
        
        return cropped_parts
    
    def match_parts_between_images(self, parts_oem, parts_asset):
        """
        Match parts between OEM and Asset images.
        
        Args:
            parts_oem: Detected parts in OEM image
            parts_asset: Detected parts in Asset image
        
        Returns:
            matched_parts: Dictionary of matched parts
        """
        matched_parts = {}
        
        for part_name in parts_oem:
            if part_name in parts_asset:
                # Get parts from both images
                oem_parts = parts_oem[part_name]
                asset_parts = parts_asset[part_name]
                
                # Match parts based on position and size
                matched_oem = []
                matched_asset = []
                
                for oem_part in oem_parts:
                    best_match = None
                    best_score = 0
                    
                    for asset_part in asset_parts:
                        # Calculate position similarity
                        oem_center = self._get_center(oem_part['bbox'])
                        asset_center = self._get_center(asset_part['bbox'])
                        
                        # Calculate distance between centers
                        distance = np.linalg.norm(np.array(oem_center) - np.array(asset_center))
                        
                        # Calculate size similarity
                        oem_area = oem_part['area']
                        asset_area = asset_part['area']
                        size_diff = abs(oem_area - asset_area) / max(oem_area, asset_area)
                        
                        # Combined similarity score
                        score = 1.0 / (1.0 + distance + size_diff * 100)
                        
                        if score > best_score and score > 0.5:
                            best_score = score
                            best_match = asset_part
                    
                    if best_match:
                        matched_oem.append(oem_part)
                        matched_asset.append(best_match)
                
                if matched_oem and matched_asset:
                    matched_parts[part_name] = {
                        'oem': matched_oem,
                        'asset': matched_asset
                    }
        
        return matched_parts
    
    def _get_center(self, bbox):
        """Get center coordinates of bounding box."""
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)