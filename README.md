Here’s the code you can directly paste into your `README.md` file:

```markdown
# Lab Report OCR API

This project is a FastAPI-based service designed to extract lab test data from medical reports using OCR (Optical Character Recognition). The API processes uploaded image files of lab reports and extracts structured data like test names, values, reference ranges, and whether the values are out of range.

## Requirements

- Python 3.7+
- FastAPI
- uvicorn
- pytesseract
- opencv-python
- numpy
- Pillow

### Install Dependencies
First, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

**Note**: Make sure you have `Tesseract` installed on your machine. Instructions to install it are provided below.

---

## API Endpoints

### 1. **POST `/get-lab-tests`**

- **Description**: This endpoint processes an uploaded lab report image and extracts lab test data, including test names, values, units, reference ranges, and whether the test value is out of range.
  
- **Method**: POST

- **Request**:
    - **File**: An image file (e.g., `.jpg`, `.png`) containing the lab report.

- **Request Body**:
    - `file`: The image file to be uploaded.

- **Response** (Success):
    ```json
    {
      "is_success": true,
      "data": [
        {
          "test_name": "Test Name",
          "test_value": "Value",
          "bio_reference_range": "Range",
          "test_unit": "Unit",
          "lab_test_out_of_range": true/false
        },
        ...
      ]
    }
    ```

- **Response** (Error):
    ```json
    {
      "is_success": false,
      "error": "Error message"
    }
    ```

---

## How to Run Locally

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/lab-report-ocr-api.git
   cd lab-report-ocr-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

The server will start at `http://localhost:8000`.

---
You can also access the interactive API documentation at http://localhost:8000/docs
## How to Test http://localhost:8000/docs


### 1. Using `curl`:
```bash
curl -X POST "http://localhost:8000/get-lab-tests" -F "file=@path_to_image.jpg"
```

### 2. Using Postman:
1. Set the HTTP method to `POST` and use the URL `http://localhost:8000/get-lab-tests`.
2. Under the "Body" tab, select `form-data`, then choose a file input for the image file (lab report) and upload the image.

---

## Example Response

### Success Response
```json
{
  "is_success": true,
  "data": [
    {
      "test_name": "ISO : 9001-2008",
      "test_value": "9001.0",
      "bio_reference_range": "2008-1",
      "test_unit": "",
      "lab_test_out_of_range": true
    },
    {
      "test_name": "101, 102, 107",
      "test_value": "101.0",
      "bio_reference_range": "102-107",
      "test_unit": "",
      "lab_test_out_of_range": true
    },
    {
      "test_name": "HA",
      "test_value": "223.0",
      "bio_reference_range": "391503-25",
      "test_unit": "",
      "lab_test_out_of_range": true
    },
    {
      "test_name": "_ PATIENT ID",
      "test_value": "16.0",
      "bio_reference_range": "13-21",
      "test_unit": "",
      "lab_test_out_of_range": false
    }
  ]
}
```

### Error Response
```json
{
  "is_success": false,
  "error": "Error message"
}
```

---

## Tesseract Installation

If you're encountering issues with Tesseract not being found in your PATH, ensure you have installed Tesseract and properly set up the PATH environment variable.

### On Windows:
1. Download the Tesseract installer from [here](https://github.com/UB-Mannheim/tesseract/wiki).
2. Run the installer and note the installation directory (e.g., `C:\Program Files\Tesseract-OCR`).
3. Add the directory to your PATH environment variable.

### On Linux (Ubuntu):
```bash
sudo apt install tesseract-ocr
```

### On macOS:
```bash
brew install tesseract
```

After installation, verify Tesseract is working by running:
```bash
tesseract --version
```

---

## License

This project is licensed under the MIT License.

---

Feel free to contribute, suggest features, or report bugs by opening an issue or a pull request!

---

### Notes

- Ensure that your lab reports are clear and readable for the OCR to work effectively.
- The system currently identifies test names, values, units, and ranges. However, in some cases, further fine-tuning may be necessary based on the format of your lab reports.

```
