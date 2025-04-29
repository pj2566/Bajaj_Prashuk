from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
import cv2
import numpy as np
import re
import io
from PIL import Image
import uvicorn
app = FastAPI()

# Preprocess image for better OCR results
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    open_cv_image = np.array(image)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Extract structured OCR data
def extract_structured_text(image_np):
    return pytesseract.image_to_data(image_np, output_type=pytesseract.Output.DICT)

# Identify lab tests from structured data
def parse_lab_tests_from_data(ocr_data):
    rows = {}
    n = len(ocr_data['level'])

    # Group words by line number
    for i in range(n):
        text = ocr_data['text'][i].strip()
        line_num = ocr_data['line_num'][i]
        if text:
            rows.setdefault(line_num, []).append(text)

    result = []

    for words in rows.values():
        line = ' '.join(words)

        # Look for patterns dynamically
        value = None
        ref_range = None
        test_name = ''
        unit = ''

        # Extract numbers for test value and reference range
        numbers = re.findall(r"\d+\.?\d*", line)

        if len(numbers) >= 1:
            try:
                value = float(numbers[0])
            except:
                continue

        if len(numbers) >= 2:
            ref_range = f"{numbers[1]}-{numbers[2]}" if len(numbers) > 2 else numbers[1]

        # Extract test name heuristically (before value)
        value_pos = line.find(numbers[0]) if numbers else -1
        if value_pos != -1:
            test_name = line[:value_pos].strip(':- ').upper()

        # Extract unit if mentioned after value
        parts = line[value_pos:].split()
        unit_match = re.search(r"(g/dL|mg/dL|%|mmol/L|10\^\d+/L)", line)
        if unit_match:
            unit = unit_match.group()

        # Check range violation
        out_of_range = False
        if ref_range:
            try:
                low, high = map(float, ref_range.split('-'))
                out_of_range = not (low <= value <= high)
            except:
                pass

        if test_name and value is not None:
            result.append({
                "test_name": test_name,
                "test_value": str(value),
                "bio_reference_range": ref_range or "",
                "test_unit": unit,
                "lab_test_out_of_range": out_of_range
            })

    return result


@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        processed_image = preprocess_image(image_bytes)
        ocr_data = extract_structured_text(processed_image)
        data = parse_lab_tests_from_data(ocr_data)
        return JSONResponse(content={"is_success": True, "data": data})
    except Exception as e:
        return JSONResponse(content={"is_success": False, "error": str(e)})

# To run locally: uncomment below
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
