# pdf-document-reconstructor

A Python utility for reconstructing PDF documents from JSON-formatted text block data and CSV layout specifications.

## Overview

This tool processes JSON data containing text block information (likely from services like AWS Textract or similar document analysis tools) along with CSV layout specifications to generate properly formatted PDF documents. It maintains the original text positioning and formatting while cleaning and normalizing the content.

## Features

- Processes multi-page documents
- Preserves original text positioning and layout
- Handles HTML entities and special characters
- Supports custom page margins and line heights
- Progress tracking for large documents
- Error handling and reporting

## Requirements

- Python 3.x
- pandas
- reportlab
- json
- html

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-document-reconstructor.git

# Install dependencies
pip install pandas reportlab
```

## Usage

1. Prepare your input files:
   - JSON file containing the analyzed document data
   - CSV file with layout specifications

2. Use the DocumentProcessor class:

```python
from document_processor import DocumentProcessor

# Initialize the processor
processor = DocumentProcessor('analyzeDocResponse.json', 'layout.csv')

# Generate the PDF
processor.process_document('output.pdf')
```

## Input File Formats

### JSON Structure
The JSON file should contain text blocks with the following information:
- Page number
- Block type
- Text content
- Geometry information (bounding box coordinates)

### CSV Layout
The CSV file should contain layout specifications for the document. Columns should be properly formatted without quotes.

## Configuration

The following parameters can be adjusted in the DocumentProcessor class:
- Page size (default: A4)
- Margins (default: 1 inch)
- Line height (default: 14 points)
- Font settings (default: Helvetica 12pt)

## Error Handling

The processor includes comprehensive error handling:
- Invalid text content handling
- Geometry validation
- Processing status updates
- Detailed error reporting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Author

[Your Name]

## Acknowledgments

- ReportLab team for the PDF generation library
- Pandas developers for the data processing capabilities
