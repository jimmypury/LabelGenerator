"""
Tests for the QR code module
"""
import unittest
from reportlab.lib.units import mm
from LabelGenerator import LabelQRCode

class TestLabelQRCode(unittest.TestCase):
    """Test cases for the LabelQRCode class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.qrcode = LabelQRCode()
    
    def test_init_default(self):
        """Test initialization with default parameters"""
        self.assertEqual(self.qrcode.x, 0)
        self.assertEqual(self.qrcode.y, 0)
        self.assertEqual(self.qrcode.width, 20 * mm)
        self.assertEqual(self.qrcode.height, 20 * mm)
        self.assertEqual(self.qrcode.data, "")
        self.assertEqual(self.qrcode.color, (0, 0, 0))  # Black
        self.assertEqual(self.qrcode.error_correction, LabelQRCode.ERROR_LEVEL.MEDIUM)
        self.assertIsNone(self.qrcode._qr_image)
        self.assertIsNone(self.qrcode._last_data)
    
    def test_set_location(self):
        """Test setting QR code position"""
        x, y = 50, 100
        self.qrcode.set_location(x, y)
        self.assertEqual(self.qrcode.x, x)
        self.assertEqual(self.qrcode.y, y)
    
    def test_set_size(self):
        """Test setting QR code size"""
        size = 30
        self.qrcode.set_size(size)
        self.assertEqual(self.qrcode.width, size * mm)
        self.assertEqual(self.qrcode.height, size * mm)
        
        # Test with different width and height
        width, height = 25, 35
        self.qrcode.set_size(width, height)
        self.assertEqual(self.qrcode.width, width * mm)
        self.assertEqual(self.qrcode.height, height * mm)
    
    def test_set_data(self):
        """Test setting QR code data"""
        data = "https://example.com"
        self.qrcode.set_data(data)
        self.assertEqual(self.qrcode.data, data)
        
        # Verify that setting data clears cached image
        self.qrcode._qr_image = "dummy_image"
        self.qrcode._last_data = "old_data"
        self.qrcode.set_data("new_data")
        self.assertIsNone(self.qrcode._qr_image)
    
    def test_set_color(self):
        """Test setting QR code color"""
        color = (255, 0, 0)  # Red
        self.qrcode.set_color(color)
        self.assertEqual(self.qrcode.color, color)
        
        # Test with RGB values
        self.qrcode.set_color(0, 255, 0)  # Green
        self.assertEqual(self.qrcode.color, (0, 255, 0))
        
        # Verify that setting color clears cached image
        self.qrcode._qr_image = "dummy_image"
        self.qrcode._last_data = "old_data"
        self.qrcode.set_color(0, 0, 255)  # Blue
        self.assertIsNone(self.qrcode._qr_image)
    
    def test_set_error_correction(self):
        """Test setting error correction level"""
        # Test all error correction levels
        levels = [
            LabelQRCode.ERROR_LEVEL.LOW,
            LabelQRCode.ERROR_LEVEL.MEDIUM,
            LabelQRCode.ERROR_LEVEL.QUARTILE,
            LabelQRCode.ERROR_LEVEL.HIGH
        ]
        
        for level in levels:
            self.qrcode.set_error_correction(level)
            self.assertEqual(self.qrcode.error_correction, level)
            
            # Verify that setting error correction clears cached image
            self.qrcode._qr_image = "dummy_image"
            self.qrcode._last_data = "old_data"
            self.qrcode.set_error_correction(level)
            self.assertIsNone(self.qrcode._qr_image)
    
    def test_generate_qr(self):
        """Test QR code generation"""
        # Set meaningful data to generate QR code
        self.qrcode.set_data("Test QR code data")
        
        # Generate QR code image
        image = self.qrcode._generate_qr()
        
        # Verify that image was generated and cached
        self.assertIsNotNone(image)
        self.assertIsNotNone(self.qrcode._qr_image)
        self.assertEqual(self.qrcode._last_data, self.qrcode.data)
        
        # Subsequent call should return cached image
        cached_image = self.qrcode._generate_qr()
        self.assertEqual(cached_image, image)

if __name__ == '__main__':
    unittest.main()
