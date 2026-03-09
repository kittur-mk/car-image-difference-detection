import cv2
from skimage.metrics import structural_similarity as ssim

class PartComparator:
    def __init__(self):
        """Initialize part comparator with advanced comparison methods."""
        self.similarity_threshold_same = 0.92
        self.similarity_threshold_minor = 0.75
    
    def compare_parts(self, matched_parts):
        """
        Compare matched parts between OEM and Asset images.
        
        Args:
            matched_parts: Dictionary of matched parts from both images
        
        Returns:
            comparison_results: Dictionary of comparison results
        """
        comparison_results = {}
        
        for part_name, part_data in matched_parts.items():
            oem_parts = part_data['oem']
            asset_parts = part_data['asset']
            
            comparison_results[part_name] = []
            
            # Compare each matched pair
            for i, (oem_part, asset_part) in enumerate(zip(oem_parts, asset_parts)):
                result = self._compare_single_part(oem_part, asset_part, part_name)
                comparison_results[part_name].append(result)
        
        return comparison_results
    
    def _compare_single_part(self, oem_part, asset_part, part_name):
        """
        Compare a single part between OEM and Asset images.
        
        Args:
            oem_part: OEM part data
            asset_part: Asset part data
            part_name: Name of the part
        
        Returns:
            result: Comparison result dictionary
        """
        oem_image = oem_part['image']
        asset_image = asset_part['image']
        
        # Resize to same dimensions
        h, w = oem_image.shape[:2]
        asset_image_resized = cv2.resize(asset_image, (w, h))
        
        # Convert to grayscale
        gray_oem = cv2.cvtColor(oem_image, cv2.COLOR_BGR2GRAY)
        gray_asset = cv2.cvtColor(asset_image_resized, cv2.COLOR_BGR2GRAY)
        
        # Compute SSIM
        ssim_score, _ = ssim(gray_oem, gray_asset, full=True)
        
        # Compute feature-based similarity using ORB
        feature_similarity = self._compute_feature_similarity(gray_oem, gray_asset)
        
        # Compute color histogram similarity
        color_similarity = self._compute_color_similarity(oem_image, asset_image_resized)
        
        # Combine similarities (weighted average)
        combined_similarity = (ssim_score * 0.5 + feature_similarity * 0.3 + color_similarity * 0.2)
        
        # Determine status
        if combined_similarity > self.similarity_threshold_same:
            status = "Same"
        elif combined_similarity > self.similarity_threshold_minor:
            status = "Minor Change"
        else:
            status = "Major Change"
        
        result = {
            'part_name': part_name,
            'ssim_score': ssim_score,
            'feature_similarity': feature_similarity,
            'color_similarity': color_similarity,
            'combined_similarity': combined_similarity,
            'status': status,
            'oem_bbox': oem_part['bbox'],
            'asset_bbox': asset_part['bbox'],
            'oem_confidence': oem_part['confidence'],
            'asset_confidence': asset_part['confidence']
        }
        
        return result
    
    def _compute_feature_similarity(self, img1, img2):
        """
        Compute feature-based similarity using ORB descriptors.
        
        Args:
            img1, img2: Grayscale images
        
        Returns:
            similarity: Feature similarity score (0-1)
        """
        # Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=200)
        
        # Detect keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        
        if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
            return 0.0
        
        # Match features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        
        if len(matches) == 0:
            return 0.0
        
        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Calculate similarity based on number of good matches
        # Normalize by the number of keypoints
        num_keypoints = min(len(kp1), len(kp2))
        if num_keypoints == 0:
            return 0.0
        
        good_matches_ratio = len(matches) / num_keypoints
        
        # Additional weighting based on average distance
        avg_distance = np.mean([m.distance for m in matches]) if matches else 1000
        distance_score = max(0, 1 - (avg_distance / 1000))
        
        similarity = min(1.0, good_matches_ratio * 0.7 + distance_score * 0.3)
        
        return similarity
    
    def _compute_color_similarity(self, img1, img2):
        """
        Compute color histogram similarity.
        
        Args:
            img1, img2: Color images
        
        Returns:
            similarity: Color similarity score (0-1)
        """
        # Convert to HSV for better color comparison
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        # Calculate histograms
        hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
        hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])
        
        # Normalize histograms
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        # Calculate correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        return correlation
    
    def get_overall_similarity(self, comparison_results):
        """
        Calculate overall similarity across all parts.
        
        Args:
            comparison_results: Dictionary of comparison results
        
        Returns:
            overall_similarity: Overall similarity score (0-1)
        """
        all_similarities = []
        
        for part_name, results in comparison_results.items():
            for result in results:
                all_similarities.append(result['combined_similarity'])
        
        if not all_similarities:
            return 0.0
        
        # Calculate weighted average based on part importance
        part_weights = {
            'headlight': 1.2,
            'grille': 1.2,
            'wheel': 1.1,
            'bumper': 1.1,
            'door': 1.0,
            'hood': 1.0,
            'window': 0.8,
            'mirror': 0.8,
            'taillight': 1.0,
            'logo': 1.3
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for part_name, results in comparison_results.items():
            weight = part_weights.get(part_name.lower(), 1.0)
            for result in results:
                weighted_sum += result['combined_similarity'] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    def get_changed_parts(self, comparison_results):
        """
        Get list of changed parts.
        
        Args:
            comparison_results: Dictionary of comparison results
        
        Returns:
            changed_parts: List of changed part names and descriptions
        """
        changed_parts = []
        
        for part_name, results in comparison_results.items():
            for result in results:
                if result['status'] != 'Same':
                    changed_parts.append({
                        'part': part_name,
                        'status': result['status'],
                        'similarity': result['combined_similarity']
                    })
        
        return changed_parts


def compare_parts(oem_parts, asset_parts):
    """
    Compare car parts between OEM and Asset images and generate human-readable explanations.
    
    Args:
        oem_parts: Dictionary of OEM car part regions
        asset_parts: Dictionary of Asset car part regions
    
    Returns:
        results: List of human-readable change descriptions
    """
    results = []

    for part in oem_parts:
        if part not in asset_parts:
            continue

        oem = oem_parts[part]
        asset = asset_parts[part]

        # Resize parts to same size for comparison
        oem = cv2.resize(oem, (200, 200))
        asset = cv2.resize(asset, (200, 200))

        # Convert to grayscale
        gray1 = cv2.cvtColor(oem, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(asset, cv2.COLOR_BGR2GRAY)

        # Compute SSIM
        score, _ = ssim(gray1, gray2, full=True)

        # If similarity is below threshold, consider it different
        if score < 0.80:
            # Front view parts
            if "Grille" in part:
                results.append("Front grille design is different")
            elif "Headlight" in part:
                results.append("Headlight shape changed")
            elif "Wheel" in part and "Rear" not in part:
                results.append(f"{part} design is different")
            elif "Bumper" in part and "Rear" not in part:
                results.append("Front bumper design changed")
            elif "Hood" in part:
                results.append("Hood design changed")
            
            # Rear view parts
            elif "Tail Light" in part:
                results.append("Tail light design is different")
            elif "Rear Wheel" in part:
                results.append(f"{part} design is different")
            elif "Rear Bumper" in part:
                results.append("Rear bumper design changed")
            elif "Trunk" in part:
                results.append("Trunk design changed")
            elif "Rear Window" in part:
                results.append("Rear window design changed")
            
            # Side view parts
            elif "Front Wheel" in part:
                results.append("Front wheel design is different")
            elif "Rear Wheel" in part:
                results.append("Rear wheel design is different")
            elif "Door" in part:
                results.append("Door design changed")
            elif "Mirror" in part:
                results.append("Side mirror design changed")
            elif "Fender" in part:
                results.append("Fender design changed")
            elif "Rear Fender" in part:
                results.append("Rear fender design changed")
            elif "Side Window" in part:
                results.append("Side window design changed")
            
            # Generic fallback
            else:
                results.append(f"{part} design is different")

    return results


def draw_part_bounding_boxes(oem_image, oem_parts, asset_parts):
    """
    Draw red bounding boxes around detected differences on the OEM image.
    
    Args:
        oem_image: Original OEM image
        oem_parts: Dictionary of OEM car part regions with coordinates
        asset_parts: Dictionary of Asset car part regions
    
    Returns:
        result_image: OEM image with red bounding boxes around differences
    """
    result_image = oem_image.copy()
    h, w = oem_image.shape[:2]
    
    # Define part coordinates for each view type
    part_coordinates = {
        # Front view coordinates
        "Front Grille": (int(h*0.35), int(h*0.55), int(w*0.25), int(w*0.55)),
        "Left Headlight": (int(h*0.30), int(h*0.45), int(w*0.15), int(w*0.35)),
        "Right Headlight": (int(h*0.30), int(h*0.45), int(w*0.60), int(w*0.80)),
        "Left Wheel": (int(h*0.55), int(h*0.85), int(w*0.15), int(w*0.35)),
        "Right Wheel": (int(h*0.55), int(h*0.85), int(w*0.60), int(w*0.80)),
        "Front Bumper": (int(h*0.55), int(h*0.75), int(w*0.25), int(w*0.60)),
        "Hood": (int(h*0.20), int(h*0.40), int(w*0.25), int(w*0.60)),
        
        # Rear view coordinates
        "Rear Bumper": (int(h*0.60), int(h*0.80), int(w*0.25), int(w*0.60)),
        "Left Tail Light": (int(h*0.40), int(h*0.55), int(w*0.15), int(w*0.35)),
        "Right Tail Light": (int(h*0.40), int(h*0.55), int(w*0.60), int(w*0.80)),
        "Left Rear Wheel": (int(h*0.55), int(h*0.85), int(w*0.15), int(w*0.35)),
        "Right Rear Wheel": (int(h*0.55), int(h*0.85), int(w*0.60), int(w*0.80)),
        "Trunk": (int(h*0.25), int(h*0.45), int(w*0.25), int(w*0.60)),
        "Rear Window": (int(h*0.15), int(h*0.35), int(w*0.20), int(w*0.70)),
        
        # Side view coordinates
        "Front Wheel": (int(h*0.55), int(h*0.85), int(w*0.10), int(w*0.30)),
        "Rear Wheel": (int(h*0.55), int(h*0.85), int(w*0.60), int(w*0.80)),
        "Door": (int(h*0.40), int(h*0.70), int(w*0.30), int(w*0.60)),
        "Side Mirror": (int(h*0.30), int(h*0.45), int(w*0.05), int(w*0.20)),
        "Fender": (int(h*0.35), int(h*0.55), int(w*0.15), int(w*0.40)),
        "Rear Fender": (int(h*0.35), int(h*0.55), int(w*0.55), int(w*0.80)),
        "Side Window": (int(h*0.20), int(h*0.45), int(w*0.30), int(w*0.70))
    }
    
    for part in oem_parts:
        if part not in asset_parts:
            continue

        oem = oem_parts[part]
        asset = asset_parts[part]

        # Resize parts to same size for comparison
        oem = cv2.resize(oem, (200, 200))
        asset = cv2.resize(asset, (200, 200))

        # Convert to grayscale
        gray1 = cv2.cvtColor(oem, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(asset, cv2.COLOR_BGR2GRAY)

        # Compute SSIM
        score, _ = ssim(gray1, gray2, full=True)

        # If similarity is below threshold, draw bounding box
        if score < 0.80 and part in part_coordinates:
            y1, y2, x1, x2 = part_coordinates[part]
            
            # Draw red bounding box (BGR format: 0, 0, 255)
            cv2.rectangle(result_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            
            # Add label text
            cv2.putText(result_image, part, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return result_image
