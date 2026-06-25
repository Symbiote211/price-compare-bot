import pytest
from unittest.mock import patch, MagicMock, mock_open
from image_recognizer import recognize_product


@patch('builtins.open', mock_open(read_data=b'fake image data'))
@patch('google.cloud.vision.ImageAnnotatorClient')
def test_recognize_product(mock_client):
    mock_response = MagicMock()
    mock_response.text_annotations = [MagicMock(description="Dove Men+Care")]
    mock_client.return_value.text_detection.return_value = mock_response

    result = recognize_product("test_product.jpg")
    assert "Dove" in result
