"""
Tests for the page module
"""
import unittest
from LabelGenerator import LabelPage, LabelText, LabelBarcode, LabelQRCode

class TestLabelPage(unittest.TestCase):
    """Test cases for the LabelPage class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.page = LabelPage(width=100, height=150)
    
    def test_init_default(self):
        """Test initialization with default parameters"""
        page = LabelPage()
        self.assertIsNotNone(page)
        self.assertEqual(page.elements, [])
        self.assertIsNone(page.background_color)
        
    def test_init_custom_size(self):
        """Test initialization with custom page size"""
        width_mm = 100
        height_mm = 150
        mm_to_point = 72 / 25.4
        
        page = LabelPage(width=width_mm, height=height_mm)
        self.assertAlmostEqual(page.width, width_mm * mm_to_point, places=2)
        self.assertAlmostEqual(page.height, height_mm * mm_to_point, places=2)
    
    def test_set_background_color(self):
        """Test setting page background color"""
        color = (255, 0, 0)  # Red
        self.page.set_background_color(color)
        self.assertEqual(self.page.background_color, color)
        
    def test_add_element(self):
        """Test adding elements to page"""
        # Add a text element
        text = LabelText()
        text.text = "Test Text"
        self.page.add_element(text)
        self.assertEqual(len(self.page.elements), 1)
        self.assertEqual(self.page.elements[0], text)
        
        # Add a barcode element
        barcode = LabelBarcode()
        self.page.add_element(barcode)
        self.assertEqual(len(self.page.elements), 2)
        self.assertEqual(self.page.elements[1], barcode)
        
        # Add a QR code element
        qrcode = LabelQRCode()
        self.page.add_element(qrcode)
        self.assertEqual(len(self.page.elements), 3)
        self.assertEqual(self.page.elements[2], qrcode)
    
    def test_clear_elements(self):
        """Test clearing all elements from page"""
        # Add elements
        self.page.add_element(LabelText())
        self.page.add_element(LabelBarcode())
        self.assertEqual(len(self.page.elements), 2)
        
        # Clear elements
        self.page.clear_elements()
        self.assertEqual(len(self.page.elements), 0)

if __name__ == '__main__':
    unittest.main()
