"""
Low-Light Image Enhancement Web Application (Flask version)
A simple Flask application for enhancing low-light images with side-by-side comparison.
"""

import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import cv2
from enhancer import LowLightEnhancer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def pil_to_base64(img):
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def process_uploaded_image(file_storage, clip_limit=2.0, gamma=1.2, brightness=1.1):
    """
    Process uploaded image and return original and enhanced versions as base64.
    
    Args:
        file_storage: FileStorage object from Flask
        clip_limit: CLAHE clip limit
        gamma: Gamma correction value
        brightness: Brightness boost factor
        
    Returns:
        dict with 'original' and 'enhanced' base64 encoded images
    """
    # Read image from file storage
    img_pil = Image.open(file_storage)
    
    # Convert to RGB if necessary
    if img_pil.mode != 'RGB':
        img_pil = img_pil.convert('RGB')
    
    # Convert to numpy array
    img_array = np.array(img_pil)
    
    # Enhance the image
    enhancer = LowLightEnhancer()
    enhanced_array = enhancer.enhance_image(
        img_array,
        clip_limit=clip_limit,
        gamma=gamma,
        brightness_boost=brightness
    )
    
    # Convert back to PIL
    enhanced_pil = Image.fromarray(enhanced_array)
    
    # Convert to base64
    original_b64 = pil_to_base64(img_pil)
    enhanced_b64 = pil_to_base64(enhanced_pil)
    
    return {
        'original': f'data:image/png;base64,{original_b64}',
        'enhanced': f'data:image/png;base64,{enhanced_b64}'
    }


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/enhance', methods=['POST'])
def enhance():
    """Handle image enhancement requests."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Get parameters from form
    clip_limit = float(request.form.get('clip_limit', 2.0))
    gamma = float(request.form.get('gamma', 1.2))
    brightness = float(request.form.get('brightness', 1.1))
    
    try:
        # Process the image
        result = process_uploaded_image(file, clip_limit, gamma, brightness)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
   app.run()
