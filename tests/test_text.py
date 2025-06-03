"""
Tests for the text module
"""
import unittest
from LabelGenerator import LabelText

class TestLabelText(unittest.TestCase):
    """Test cases for the LabelText class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.text = LabelText()
    
    def test_init_default(self):
        """Test initialization with default parameters"""
        self.assertEqual(self.text.x, 0)
        self.assertEqual(self.text.y, 0)
        self.assertEqual(self.text.text, "")
        self.assertEqual(self.text.font_name, "Helvetica")
        self.assertEqual(self.text.font_size, 10)
        self.assertIsNone(self.text.font_style)
        self.assertEqual(self.text.color, (0, 0, 0))  # Black
        self.assertEqual(self.text.alignment, 'left')
    
    def test_set_location(self):
        """Test setting text position"""
        x, y = 50, 100
        self.text.set_location(x, y)
        self.assertEqual(self.text.x, x)
        self.assertEqual(self.text.y, y)
    
    def test_set_text(self):
        """Test setting text content"""
        text_content = "Hello, World!"
        self.text.set_text(text_content)
        self.assertEqual(self.text.text, text_content)
    
    def test_set_font(self):
        """Test setting font properties"""
        font_name = "Times-Roman"
        font_size = 12
        self.text.set_font(font_name, font_size)
        self.assertEqual(self.text.font_name, font_name)
        self.assertEqual(self.text.font_size, font_size)
    
    def test_set_color(self):
        """Test setting text color"""
        color = (255, 0, 0)  # Red
        self.text.set_color(color)
        self.assertEqual(self.text.color, color)
        
        # Test with RGB values
        self.text.set_color(0, 255, 0)  # Green
        self.assertEqual(self.text.color, (0, 255, 0))
    
    def test_set_alignment(self):
        """Test setting text alignment"""
        # Test left alignment
        self.text.set_alignment('left')
        self.assertEqual(self.text.alignment, 'left')
        
        # Test center alignment
        self.text.set_alignment('center')
        self.assertEqual(self.text.alignment, 'center')
        
        # Test right alignment
        self.text.set_alignment('right')
        self.assertEqual(self.text.alignment, 'right')
        
        # Test invalid alignment (should default to 'left')
        self.text.set_alignment('invalid')
        self.assertEqual(self.text.alignment, 'left')
        
    def test_set_style(self):
        """Test setting font style"""
        # Test normal style
        self.text.set_style('normal')
        self.assertEqual(self.text.font_style, None)
        
        # Test bold style
        self.text.set_style('bold')
        self.assertEqual(self.text.font_style, 'bold')
        
        # Test italic style
        self.text.set_style('italic')
        self.assertEqual(self.text.font_style, 'italic')
        
        # Test bold-italic style
        self.text.set_style('bold-italic')
        self.assertEqual(self.text.font_style, 'bold-italic')
        
        # Test invalid style (should default to None)
        self.text.set_style('invalid')
        self.assertEqual(self.text.font_style, None)

if __name__ == '__main__':
    unittest.main()
