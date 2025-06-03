"""
Tests for the document module
"""
import unittest
import os
import tempfile
from LabelGenerator import LabelDocument, LabelPage

class TestLabelDocument(unittest.TestCase):
    """Test cases for the LabelDocument class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.document = LabelDocument()
        self.test_page = LabelPage(width=100, height=150)
    
    def test_init_default(self):
        """Test initialization with default parameters"""
        self.assertEqual(self.document.pages, [])
        self.assertEqual(len(self.document.pages), 0)
    
    def test_add_page(self):
        """Test adding pages to document"""
        self.document.add_page(self.test_page)
        self.assertEqual(len(self.document.pages), 1)
        self.assertEqual(self.document.pages[0], self.test_page)
        
        # Add another page
        second_page = LabelPage(width=200, height=250)
        self.document.add_page(second_page)
        self.assertEqual(len(self.document.pages), 2)
        self.assertEqual(self.document.pages[1], second_page)
    
    def test_save_pdf(self):
        """Test saving document to PDF"""
        self.document.add_page(self.test_page)
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Save the document
            self.document.save_pdf(temp_filename)
            
            # Verify the file exists and has content
            self.assertTrue(os.path.exists(temp_filename))
            self.assertGreater(os.path.getsize(temp_filename), 0)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
    def test_clear_pages(self):
        """Test clearing all pages from document"""
        # Add a few pages
        self.document.add_page(LabelPage(width=100, height=150))
        self.document.add_page(LabelPage(width=200, height=250))
        self.assertEqual(len(self.document.pages), 2)
        
        # Clear pages
        self.document.clear_pages()
        self.assertEqual(len(self.document.pages), 0)

if __name__ == '__main__':
    unittest.main()
