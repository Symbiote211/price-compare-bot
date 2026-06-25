from google.cloud import vision
from typing import Optional
from config import GOOGLE_CREDENTIALS
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        if GOOGLE_CREDENTIALS:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS
        _client = vision.ImageAnnotatorClient()
    return _client

def recognize_product(image_path: str) -> str:
    try:
        client = _get_client()

        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        if response.text_annotations:
            return response.text_annotations[0].description
        return ""
    except Exception as e:
        print(f"Vision API error: {e}")
        return ""
