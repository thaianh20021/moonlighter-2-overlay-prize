"""
Screen Reader Module for Moonlighter 2 Overlay
Captures screen region and performs OCR to detect item names
"""

import mss
import pytesseract
import numpy as np
from PIL import Image
import json
import os
import sys
from typing import Optional, Tuple, Dict


class ScreenReader:
    def __init__(self, config_file: str = "config.json"):
        """Initialize screen reader with OCR"""
        self.config = self._load_config(config_file)
        self.screen_info = self._get_screen_info()
        self.ocr_region = self._calculate_ocr_region()
        self._setup_tesseract()
        
        print(f"Screen size: {self.screen_info['width']}x{self.screen_info['height']}")
        print(f"OCR region: {self.ocr_region}")
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found, using defaults")
            return {
                "ocr_languages": ["en"],
                "ocr_region_offset": {"x": 0, "y": 0, "width": 0, "height": 0}
            }
    
    def _get_screen_info(self) -> Dict:
        """Get primary monitor information"""
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            return {
                'width': monitor['width'],
                'height': monitor['height'],
                'left': monitor['left'],
                'top': monitor['top']
            }
    
    def _calculate_ocr_region(self) -> Dict:
        """
        Calculate the OCR region based on screen size
        Checks for custom region first, then falls back to auto-calculated region
        """
        # Check if user has set a custom region (via F5)
        if self.config.get('use_custom_region', False):
            custom_region = self.config.get('custom_ocr_region')
            if custom_region:
                print("Using custom OCR region from config")
                return custom_region
        
        # Auto-calculate based on screen size
        # Based on test results with 1024x576 screenshot:
        # - Item name "Battery" found at (400, 350, 650, 420) with 99.99% confidence
        # - This translates to:
        #   X: 39-63% from left (center)
        #   Y: 60.7-72.9% from top (bottom half)
        screen_w = self.screen_info['width']
        screen_h = self.screen_info['height']
        
        # Calculate base region based on percentage of screen
        # Center horizontally around 40-65% width
        x_start_percent = 0.39
        x_end_percent = 0.635
        
        # Bottom half vertically around 60-73% height
        y_start_percent = 0.607
        y_end_percent = 0.729
        
        x_start = int(screen_w * x_start_percent)
        y_start = int(screen_h * y_start_percent)
        width = int(screen_w * (x_end_percent - x_start_percent))
        height = int(screen_h * (y_end_percent - y_start_percent))
        
        # Apply user-defined offsets from config
        offset = self.config.get('ocr_region_offset', {})
        x_start += offset.get('x', 0)
        y_start += offset.get('y', 0)
        width += offset.get('width', 0)
        height += offset.get('height', 0)
        
        return {
            'left': x_start,
            'top': y_start,
            'width': width,
            'height': height
        }
    
    def _setup_tesseract(self):
        """Setup Tesseract OCR path (for bundled executable or system installation)"""
        # Check if running as bundled executable
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
            tesseract_path = os.path.join(base_path, 'tesseract', 'tesseract.exe')
            tessdata_path = os.path.join(base_path, 'tesseract', 'tessdata')
            
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                os.environ['TESSDATA_PREFIX'] = tessdata_path
                print(f"✓ Using bundled Tesseract: {tesseract_path}")
            else:
                print("⚠️ Bundled Tesseract not found, using system installation")
        else:
            # Running as script - use system Tesseract
            # Try common installation paths on Windows
            possible_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"✓ Using system Tesseract: {path}")
                    return
            
            print("✓ Using Tesseract from PATH")
    
    def initialize_ocr(self):
        """Initialize OCR (kept for compatibility, but Tesseract is ready immediately)"""
        print("✓ Tesseract OCR ready")
    
    def capture_region(self) -> Optional[np.ndarray]:
        """Capture the OCR region of the screen"""
        try:
            with mss.mss() as sct:
                # Capture the specific region
                screenshot = sct.grab(self.ocr_region)
                # Convert to numpy array
                img = np.array(screenshot)
                # Convert BGRA to RGB
                img = img[:, :, :3]
                return img
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
    
    def preprocess_image(self, img: np.ndarray) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy for Tesseract
        - Convert to PIL Image
        - Convert to grayscale
        - Increase contrast
        """
        # Convert numpy array to PIL Image
        pil_img = Image.fromarray(img)
        
        # Convert to grayscale
        pil_img = pil_img.convert('L')
        
        # Increase contrast (helps with text detection)
        import PIL.ImageEnhance as ImageEnhance
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(2.0)
        
        return pil_img
    
    def read_text(self, img: np.ndarray) -> str:
        """
        Perform OCR on the image using Tesseract
        Returns the detected text
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(img)
            
            # Configure Tesseract for better accuracy
            # PSM 6 = Assume a single uniform block of text
            # OEM 3 = Default, based on what is available (LSTM + Legacy)
            custom_config = r'--oem 3 --psm 6'
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_img, config=custom_config, lang='eng')
            
            return text.strip()
        except Exception as e:
            print(f"Error during OCR: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def get_current_item_name(self) -> Optional[str]:
        """
        Capture screen and read item name
        Returns the detected item name or None
        """
        # Capture screen region
        img = self.capture_region()
        if img is None:
            return None
        
        # Read text from image
        text = self.read_text(img)
        
        # Clean up the text
        # Remove extra whitespace and newlines
        text = ' '.join(text.split())
        
        return text if text else None
    
    def save_debug_screenshot(self, filename: str = "debug_capture.png"):
        """Save the current OCR region for debugging"""
        img = self.capture_region()
        if img is not None:
            pil_img = Image.fromarray(img)
            pil_img.save(filename)
            print(f"Debug screenshot saved to {filename}")


if __name__ == "__main__":
    # Test the screen reader
    import time
    
    print("Testing Screen Reader...")
    reader = ScreenReader()
    
    print("\nSaving debug screenshot...")
    reader.save_debug_screenshot()
    
    print("\nInitializing OCR...")
    reader.initialize_ocr()
    
    print("\nReading text from screen in 3 seconds...")
    print("Please hover over an item in the game!")
    time.sleep(3)
    
    item_name = reader.get_current_item_name()
    print(f"\nDetected text: '{item_name}'")
