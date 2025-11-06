"""
Examples of using the Low-Light Image Enhancer programmatically.
This script demonstrates various ways to use the enhancer module in your own code.
"""

from enhancer import LowLightEnhancer, enhance_image_file
import cv2
import numpy as np
from PIL import Image


# Example 1: Simple file enhancement with default parameters
def example_simple():
    """Simplest way to enhance an image file."""
    print("Example 1: Simple file enhancement")
    
    # Just provide input and output paths
    enhance_image_file('input.jpg', 'output_simple.jpg')
    
    print("✓ Enhanced image saved to output_simple.jpg\n")


# Example 2: Custom parameters
def example_custom_parameters():
    """Enhance with custom parameters for different effects."""
    print("Example 2: Custom parameters")
    
    # Subtle enhancement for slightly dark images
    enhance_image_file(
        'input.jpg',
        'output_subtle.jpg',
        clip_limit=1.5,    # Low contrast boost
        gamma=1.1,         # Slight brightness increase
        brightness=1.05    # Minimal brightness boost
    )
    print("✓ Subtle enhancement saved to output_subtle.jpg")
    
    # Strong enhancement for very dark images
    enhance_image_file(
        'input.jpg',
        'output_strong.jpg',
        clip_limit=3.5,    # High contrast boost
        gamma=1.8,         # Significant brightness increase
        brightness=1.3     # Strong brightness boost
    )
    print("✓ Strong enhancement saved to output_strong.jpg\n")


# Example 3: Working with numpy arrays
def example_numpy_arrays():
    """Enhance images loaded as numpy arrays."""
    print("Example 3: Working with numpy arrays")
    
    # Load image with OpenCV (returns BGR format)
    image_bgr = cv2.imread('input.jpg')
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    # Create enhancer and process
    enhancer = LowLightEnhancer()
    enhanced_rgb = enhancer.enhance_image(image_rgb)
    
    # Convert back to BGR for saving with OpenCV
    enhanced_bgr = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite('output_numpy.jpg', enhanced_bgr)
    
    print("✓ Enhanced from numpy array saved to output_numpy.jpg\n")


# Example 4: Working with PIL Images
def example_pil_images():
    """Enhance images using PIL/Pillow."""
    print("Example 4: Working with PIL Images")
    
    # Load with PIL
    image_pil = Image.open('input.jpg')
    
    # Convert to numpy array
    image_array = np.array(image_pil)
    
    # Enhance
    enhancer = LowLightEnhancer()
    enhanced_array = enhancer.enhance_image(image_array)
    
    # Convert back to PIL
    enhanced_pil = Image.fromarray(enhanced_array)
    enhanced_pil.save('output_pil.jpg')
    
    print("✓ Enhanced from PIL Image saved to output_pil.jpg\n")


# Example 5: Batch processing multiple images
def example_batch_processing():
    """Process multiple images at once."""
    print("Example 5: Batch processing")
    
    import glob
    from pathlib import Path
    
    # Get all jpg images in a directory
    input_dir = Path('input_images')
    output_dir = Path('output_images')
    output_dir.mkdir(exist_ok=True)
    
    # Process each image
    for image_path in input_dir.glob('*.jpg'):
        output_path = output_dir / f"enhanced_{image_path.name}"
        
        print(f"Processing {image_path.name}...", end=' ')
        enhance_image_file(str(image_path), str(output_path))
        print("✓")
    
    print(f"All images processed and saved to {output_dir}/\n")


# Example 6: Progressive enhancement levels
def example_progressive_enhancement():
    """Create multiple versions with different enhancement levels."""
    print("Example 6: Progressive enhancement levels")
    
    enhancer = LowLightEnhancer()
    
    # Load image
    image = cv2.imread('input.jpg')
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create different enhancement levels
    levels = {
        'light': (1.5, 1.1, 1.05),
        'medium': (2.0, 1.2, 1.1),
        'strong': (2.5, 1.4, 1.2),
        'ultra': (3.5, 1.8, 1.3),
    }
    
    for level_name, (clip, gamma, brightness) in levels.items():
        print(f"Creating {level_name} enhancement...", end=' ')
        
        enhanced = enhancer.enhance_image(
            image_rgb,
            clip_limit=clip,
            gamma=gamma,
            brightness_boost=brightness
        )
        
        # Save
        enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR)
        cv2.imwrite(f'output_{level_name}.jpg', enhanced_bgr)
        print("✓")
    
    print("All enhancement levels created\n")


# Example 7: Compare before and after
def example_comparison():
    """Create a side-by-side comparison image."""
    print("Example 7: Creating comparison image")
    
    import cv2
    
    # Load original
    original = cv2.imread('input.jpg')
    
    # Enhance
    enhancer = LowLightEnhancer()
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    enhanced_rgb = enhancer.enhance_image(original_rgb)
    enhanced = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
    
    # Resize to same height if needed
    if original.shape != enhanced.shape:
        enhanced = cv2.resize(enhanced, (original.shape[1], original.shape[0]))
    
    # Create side-by-side comparison
    comparison = np.hstack([original, enhanced])
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(comparison, 'Original', (20, 50), font, 1.5, (255, 255, 255), 3)
    cv2.putText(comparison, 'Enhanced', (original.shape[1] + 20, 50), font, 1.5, (255, 255, 255), 3)
    
    cv2.imwrite('comparison.jpg', comparison)
    print("✓ Comparison image saved to comparison.jpg\n")


# Example 8: Custom enhancement function
def example_custom_function():
    """Create your own enhancement function with specific settings."""
    print("Example 8: Custom enhancement function")
    
    def enhance_night_photo(input_path, output_path):
        """
        Specialized enhancement for night photography.
        Uses settings optimized for very dark images.
        """
        enhance_image_file(
            input_path,
            output_path,
            clip_limit=3.0,    # Strong contrast for dark scenes
            gamma=1.6,         # Significant brightening
            brightness=1.25    # Additional brightness boost
        )
    
    def enhance_indoor_photo(input_path, output_path):
        """
        Specialized enhancement for indoor low-light photos.
        Uses balanced settings.
        """
        enhance_image_file(
            input_path,
            output_path,
            clip_limit=2.2,    # Moderate contrast
            gamma=1.3,         # Moderate brightening
            brightness=1.15    # Slight brightness boost
        )
    
    # Use the custom functions
    enhance_night_photo('input.jpg', 'output_night.jpg')
    print("✓ Night photo enhancement saved")
    
    enhance_indoor_photo('input.jpg', 'output_indoor.jpg')
    print("✓ Indoor photo enhancement saved\n")


def main():
    """
    Main function to run examples.
    Comment out examples you don't want to run.
    """
    print("="*60)
    print("Low-Light Image Enhancer - Usage Examples")
    print("="*60 + "\n")
    
    # Note: Make sure you have an 'input.jpg' file in the same directory
    # or update the paths in the examples above
    
    try:
        # Uncomment the examples you want to run:
        
        # example_simple()
        # example_custom_parameters()
        # example_numpy_arrays()
        # example_pil_images()
        # example_batch_processing()
        # example_progressive_enhancement()
        # example_comparison()
        # example_custom_function()
        
        print("To run these examples, uncomment them in the main() function")
        print("and make sure you have 'input.jpg' in the same directory.\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure 'input.jpg' exists in the current directory.\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == '__main__':
    main()
