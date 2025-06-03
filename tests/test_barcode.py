"""
Tests for the barcode module
"""
import unittest
from reportlab.lib.units import mm
from LabelGenerator import LabelBarcode

class TestLabelBarcode(unittest.TestCase):
    """Test cases for the LabelBarcode class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.barcode = LabelBarcode()
    
    def test_init_default(self):
        """Test initialization with default parameters"""
        self.assertEqual(self.barcode.x, 0)
        self.assertEqual(self.barcode.y, 0)
        self.assertEqual(self.barcode.width, 50 * mm)
        self.assertEqual(self.barcode.height, 10 * mm)
        self.assertEqual(self.barcode.data, "1234567890")
        self.assertEqual(self.barcode.barcode_type, "code128")
        self.assertEqual(self.barcode.color, (0, 0, 0))  # Black
        self.assertFalse(self.barcode.show_text)
        self.assertEqual(self.barcode.text_location, LabelBarcode.TEXT.BOTTOM)
        self.assertEqual(self.barcode.text_color, (0, 0, 0))
        self.assertEqual(self.barcode.text_size, 8)
    
    def test_set_location(self):
        """Test setting barcode position"""
        x, y = 50, 100
        self.barcode.set_location(x, y)
        self.assertEqual(self.barcode.x, x)
        self.assertEqual(self.barcode.y, y)
    
    def test_set_size(self):
        """Test setting barcode size"""
        width, height = 60, 15
        self.barcode.set_size(width, height)
        self.assertEqual(self.barcode.width, width * mm)
        self.assertEqual(self.barcode.height, height * mm)
    
    def test_set_data(self):
        """Test setting barcode data"""
        data = "9876543210"
        self.barcode.set_data(data)
        self.assertEqual(self.barcode.data, data)
    
    def test_set_barcode_type(self):
        """Test setting barcode type"""
        # Test valid barcode types
        valid_types = ["code39", "code128", "ean13", "ean8", "upca", "usps_4state"]
        
        for bc_type in valid_types:
            self.barcode.set_barcode_type(bc_type)
            self.assertEqual(self.barcode.barcode_type, bc_type)
    
    def test_set_color(self):
        """Test setting barcode color"""
        color = (255, 0, 0)  # Red
        self.barcode.set_color(color)
        self.assertEqual(self.barcode.color, color)
        
        # Test with RGB values
        self.barcode.set_color(0, 255, 0)  # Green
        self.assertEqual(self.barcode.color, (0, 255, 0))
    
    def test_show_text_options(self):
        """Test barcode text display options"""
        # Test hiding text
        self.barcode.hide_text()
        self.assertFalse(self.barcode.show_text)
        
        # Test showing text at bottom
        self.barcode.show_text_bottom()
        self.assertTrue(self.barcode.show_text)
        self.assertEqual(self.barcode.text_location, LabelBarcode.TEXT.BOTTOM)
        
        # Test showing text at top
        self.barcode.show_text_top()
        self.assertTrue(self.barcode.show_text)
        self.assertEqual(self.barcode.text_location, LabelBarcode.TEXT.TOP)
    
    def test_set_text_properties(self):
        """Test setting barcode text properties"""
        # Test text color
        color = (0, 0, 255)  # Blue
        self.barcode.set_text_color(color)
        self.assertEqual(self.barcode.text_color, color)
        
        # Test text size
        size = 12
        self.barcode.set_text_size(size)
        self.assertEqual(self.barcode.text_size, size)

if __name__ == '__main__':
    unittest.main()
