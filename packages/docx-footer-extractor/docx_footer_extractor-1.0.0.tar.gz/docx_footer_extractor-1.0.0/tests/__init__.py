"""
Tests for DOCX Footer Extractor

Test suite for the docx_footer_extractor package.
"""

# Version info
__version__ = "1.0.0"

# Test configuration
TEST_DATA_DIR = "test_data"
SAMPLE_FILES = [
    "sample1.docx",
    "sample2.docx", 
    "sample3.docx"
]

# Expected test results for validation
EXPECTED_RESULTS = {
    "sample1.docx": {
        "Author": "John Doe",
        "Version": "1.0",
        "Date": "2025-01-15"
    },
    "sample2.docx": {
        "Title": "Test Document",
        "Department": "Engineering"
    }
}

# Test utilities
def get_test_file_path(filename):
    """Get the full path to a test file."""
    import os
    return os.path.join(os.path.dirname(__file__), TEST_DATA_DIR, filename)

def create_mock_docx_structure():
    """Create mock DOCX structure for testing."""
    return {
        "sections": [
            {
                "footer": {
                    "paragraphs": ["Author: Test User", "Version: 2.0"],
                    "tables": [[("Key", "Value"), ("Author", "Jane Doe")]]
                }
            }
        ]
    }

# Make test utilities available
__all__ = [
    "TEST_DATA_DIR",
    "SAMPLE_FILES", 
    "EXPECTED_RESULTS",
    "get_test_file_path",
    "create_mock_docx_structure"
]