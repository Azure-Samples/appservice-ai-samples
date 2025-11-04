"""
Low-Light Image Enhancement Module
A standalone module for enhancing low-light images.
"""

import numpy as np
import cv2
from typing import Tuple


class LowLightEnhancer:
    """Enhances low-light images using CLAHE and adaptive techniques."""
    
    def __init__(self):
        """Initialize the enhancer with default parameters."""
        self.clip_limit = 2.0
        self.tile_grid_size = (8, 8)
        
    def enhance_image(
        self, 
        image: np.ndarray,
        clip_limit: float = 2.0,
        gamma: float = 1.2,
        brightness_boost: float = 1.1
    ) -> np.ndarray:
        """
        Enhance a low-light image using multiple techniques.
        
        Args:
            image: Input image as numpy array (RGB or BGR)
            clip_limit: CLAHE clip limit (higher = more contrast)
            gamma: Gamma correction value (>1 brightens)
            brightness_boost: Overall brightness multiplier
            
        Returns:
            Enhanced image as numpy array (same format as input)
        """
        # Detect if image is RGB or BGR
        is_bgr = self._detect_bgr(image)
        
        # Convert to RGB if BGR
        if is_bgr:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Convert RGB to LAB color space for better color preservation
        lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=self.tile_grid_size)
        l_enhanced = clahe.apply(l)
        
        # Apply gamma correction for brightness
        l_enhanced = self._apply_gamma_correction(l_enhanced, gamma)
        
        # Apply brightness boost
        l_enhanced = np.clip(l_enhanced * brightness_boost, 0, 255).astype(np.uint8)
        
        # Merge channels back
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        
        # Convert back to RGB
        enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # Apply slight saturation boost
        enhanced_rgb = self._boost_saturation(enhanced_rgb, factor=1.1)
        
        # Convert back to BGR if input was BGR
        if is_bgr:
            return cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
        else:
            return enhanced_rgb
    
    def _detect_bgr(self, image: np.ndarray) -> bool:
        """Detect if image is likely in BGR format (heuristic)."""
        # This is a simple heuristic - in practice, you should know your input format
        # For now, assume it's BGR if loaded with cv2.imread
        return False  # Default to RGB
    
    def _apply_gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """Apply gamma correction to brighten the image."""
        inv_gamma = 1.0 / gamma
        table = np.array([
            ((i / 255.0) ** inv_gamma) * 255 
            for i in range(256)
        ]).astype(np.uint8)
        return cv2.LUT(image, table)
    
    def _boost_saturation(self, image: np.ndarray, factor: float) -> np.ndarray:
        """Boost color saturation."""
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def enhance_image_file(
    input_path: str,
    output_path: str,
    clip_limit: float = 2.0,
    gamma: float = 1.2,
    brightness: float = 1.1
) -> None:
    """
    Enhance a low-light image from file.
    
    Args:
        input_path: Path to input image
        output_path: Path to save enhanced image
        clip_limit: CLAHE clip limit parameter
        gamma: Gamma correction parameter
        brightness: Brightness boost parameter
    """
    # Read image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Could not read image from {input_path}")
    
    # Enhance
    enhancer = LowLightEnhancer()
    # OpenCV reads as BGR, so we convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    enhanced = enhancer.enhance_image(image_rgb, clip_limit, gamma, brightness)
    
    # Convert back to BGR for saving
    enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR)
    
    # Save
    cv2.imwrite(output_path, enhanced_bgr)
    print(f"Enhanced image saved to: {output_path}")
