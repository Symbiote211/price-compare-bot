import pytest
from unittest.mock import patch, MagicMock
from ocr import extract_text_from_image

@patch('ocr.Image.open')
@patch('pytesseract.image_to_string')
def test_extract_text(mock_tesseract, mock_open):
    mock_tesseract.return_value = "Dove Men+Care гель для душа 250мл"
    result = extract_text_from_image("test_image.jpg")
    assert "Dove" in result
    assert "гель" in result

@patch('ocr.Image.open')
@patch('pytesseract.image_to_string')
def test_extract_text_empty(mock_tesseract, mock_open):
    mock_tesseract.return_value = ""
    result = extract_text_from_image("empty_image.jpg")
    assert result == ""
