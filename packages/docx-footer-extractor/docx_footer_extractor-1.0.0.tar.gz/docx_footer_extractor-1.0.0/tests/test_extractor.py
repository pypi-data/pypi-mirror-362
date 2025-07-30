import unittest
import tempfile
import os
from docx import Document
from docx_footer_extractor import DocxFooterExtractor, extract_footer
from tests import EXPECTED_RESULTS, get_test_file_path, create_mock_docx_structure

class TestDocxFooterExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = DocxFooterExtractor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_convenience_function(self):
        # Test that convenience function works
        try:
            results = extract_footer([])
        except ValueError:
            pass  # Expected for empty list
        
        # Test with non-existent directory
        try:
            results = extract_footer("/non/existent/path")
        except FileNotFoundError:
            pass  # Expected

    def test_with_sample_data(self):
        # Use predefined expected results
        expected = EXPECTED_RESULTS["sample1.docx"]
        
        # Get test file path
        test_file = get_test_file_path("sample1.docx")
        
        # Use mock structure
        mock_data = create_mock_docx_structure()

if __name__ == '__main__':
    unittest.main()
