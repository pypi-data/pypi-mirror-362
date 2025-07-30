# DOCX Footer Extractor

A Python library for extracting metadata from DOCX file footers using parallel processing.

## Features

- Extract key-value pairs from DOCX file footers
- Process multiple files in parallel for better performance
- Support for both folder processing and specific file lists
- Extract metadata from footer text and tables
- Python 3.9+ compatibility
- Thread-safe processing with error handling

## Installation

```bash
pip install docx_footer_extractor
```

## Quick Start

```python
from docx_footer_extractor import DocxFooterExtractor

# Create extractor instance
extractor = DocxFooterExtractor(max_workers=4)

# Process all DOCX files in a folder
results = extractor.extract("./documents")

# Process specific files
file_list = ["doc1.docx", "doc2.docx", "folder/doc3.docx"]
results = extractor.extract(file_list)

# Results format
for result in results:
    filename = result['filename']
    metadata = result['metadata']
    print(f"{filename}: {metadata}")
```

## Usage

### Using the Class

```python
from docx_footer_extractor import DocxFooterExtractor

extractor = DocxFooterExtractor(max_workers=4)

# Process folder
results = extractor.extract("./my_documents")

# Process specific files
results = extractor.extract([
    "document1.docx",
    "path/to/document2.docx"
])

# Save results to file
extractor.save_results_to_file(results, "output.txt")
```

## Output Format

The library returns a list of dictionaries with the following structure:

```bash
python[
    {
        "filename": "document1.docx",
        "metadata": {
            "Author": "John Doe",
            "Version": "1.0",
            "Date": "2025-01-15"
        }
    },
    {
        "filename": "document2.docx",
        "metadata": {
            "Title": "Report",
            "Department": "Sales"
        }
    }
]
```

## Requirements

```bash
Python 3.9+
python-docx>=0.8.11
```
