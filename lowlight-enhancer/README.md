# 🌙 Low-Light Image Enhancer

A Python application that enhances low-light images using adaptive histogram equalization and contrast enhancement techniques. The app features a user-friendly web interface built with Gradio that allows users to upload images and view the enhanced results side-by-side with the original.

## Features

- 📤 **Easy Upload**: Upload images via drag-and-drop or file browser
- 🎨 **Side-by-Side Comparison**: View original and enhanced images together
- ⚙️ **Adjustable Parameters**: Fine-tune enhancement settings
- 💻 **CPU-Only**: No GPU required - runs on any machine
- 🐍 **Python 3.14 Compatible**: Works with the latest Python version
- 🚀 **Real-time Processing**: Fast image enhancement

## How It Works

The application uses several image processing techniques:

1. **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: Enhances local contrast without over-amplifying noise
2. **Gamma Correction**: Adjusts overall brightness while preserving details
3. **LAB Color Space Processing**: Maintains color accuracy during enhancement
4. **Saturation Boost**: Slightly enhances colors that may appear washed out

## Installation

### Prerequisites

- Python 3.9 or higher (tested up to Python 3.13)
- pip package manager

### Setup

1. Clone or download this repository

2. Navigate to the project directory:
   ```bash
   cd lowlight-enhancer
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application locally

Run the application with:

```bash
python app_flask.py
```

The application will start a local web server at `http://127.0.0.1:5000`

Open your web browser and navigate to that URL.

1. **Upload an Image**: 
   - Click the upload area or drag-and-drop a low-light image
   - Supports common formats: JPG, PNG, WEBP, etc.

2. **Automatic Enhancement**:
   - The image is automatically enhanced with default settings
   - View results side-by-side immediately

3. **Adjust Parameters** (Optional):
   - Open "Advanced Settings" to fine-tune:
     - **Contrast Limit** (1.0-4.0): Controls contrast enhancement strength
     - **Gamma Correction** (0.5-2.5): Adjusts brightness
     - **Brightness Boost** (1.0-1.5): Overall brightness multiplier
   - Click "Enhance Image" to apply new settings

4. **Compare Results**:
   - Original image on the left
   - Enhanced image on the right
   - Zoom in to see details

## Parameters Guide

### Contrast Limit (Default: 2.0)
- **Lower values (1.0-1.5)**: Subtle enhancement, good for slightly dark images
- **Medium values (2.0-2.5)**: Balanced enhancement for most low-light images
- **Higher values (3.0-4.0)**: Strong enhancement for very dark images

### Gamma Correction (Default: 1.2)
- **Lower values (<1.0)**: Darkens the image
- **Value of 1.0**: No change
- **Higher values (>1.0)**: Brightens the image

### Brightness Boost (Default: 1.1)
- **1.0**: No additional brightness
- **1.1-1.3**: Moderate brightening
- **1.4-1.5**: Strong brightening

## Technical Details

### Algorithm

The enhancement pipeline:

```
Input Image (RGB)
    ↓
Convert to LAB color space
    ↓
Apply CLAHE to L (lightness) channel
    ↓
Apply gamma correction
    ↓
Apply brightness boost
    ↓
Merge enhanced L with original A, B channels
    ↓
Convert back to RGB
    ↓
Boost saturation slightly
    ↓
Output Enhanced Image
```

### Libraries Used

- **Flask**: Web framework for the user interface
- **OpenCV**: Core image processing operations
- **Pillow**: Image I/O and format handling
- **NumPy**: Numerical operations and array manipulation

## Performance

- **Processing Time**: Typically <1 second for standard images (depending on resolution)
- **Memory Usage**: Minimal - processes one image at a time
- **CPU Usage**: Moderate during processing, idle otherwise
- **Resolution Support**: Works with any resolution (larger images take longer)

## Troubleshooting

### Common Issues

**Issue**: Application won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Enhancement too strong/weak
- **Solution**: Adjust the parameters in the Advanced Settings panel

**Issue**: Images look washed out
- **Solution**: Reduce the Contrast Limit and Brightness Boost values

## Limitations

- Not suitable for completely black/no-light images
- May introduce noise in extremely dark areas
- Color accuracy may vary with very unusual lighting conditions
- Best results with images that have some visible detail

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

Built using:
- OpenCV's CLAHE implementation
- Gradio for the web interface
- Python's image processing ecosystem
