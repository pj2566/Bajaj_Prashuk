# Lab Report OCR API

This project provides a FastAPI-based web service to process lab reports in image format using Optical Character Recognition (OCR) to extract lab test results. It can detect test names, values, reference ranges, and flag out-of-range values.

## Features
- Extracts test names, values, units, and reference ranges from scanned lab reports.
- Flags test values that fall outside the reference range.
- Handles multiple test results from a single image.
  
## Prerequisites
Make sure you have the following installed:
- Python 3.7 or higher
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (make sure it's installed and accessible in your PATH)
- Required Python packages (see below)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/lab-report-ocr-api.git
   cd lab-report-ocr-api
