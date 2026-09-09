import cv2
import numpy as np
from typing import Dict, List
from PIL import Image
import io


def process_image(image_data: bytes) -> Dict:
    analysis = analyze_image(image_data)
    if not analysis["valid"]:
        return {"valid": False, "text": "", "image": image_data, "reason": analysis["reason"]}
    text = extract_text(image_data)
    enhanced = enhance_image(image_data)
    return {"valid": True, "text": text, "image": enhanced, "reason": ""}


def resize_image(image_data: bytes, max_size: int = 2000) -> bytes:
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        if max(h, w) > max_size:
            scale = max_size / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        _, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        return buffer.tobytes()
    except Exception:
        return image_data


def convert_pdf_to_images(pdf_data: bytes) -> List[bytes]:
    try:
        from pdf2image import convert_from_bytes
        return [io.BytesIO().getvalue() for img in convert_from_bytes(pdf_data)]
    except Exception:
        return []


# Import functions from vision module
from app.ai.vision import analyze_image, extract_text, enhance_image
