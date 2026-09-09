import cv2
import numpy as np
from typing import Dict
from PIL import Image
import io
import pytesseract


def analyze_image(image_data: bytes) -> Dict:
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"valid": False, "reason": "Image invalide"}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        brightness = gray.mean()
        contrast = gray.std()
        h, w = img.shape[:2]

        is_sharp = variance > 50
        is_bright = 50 < brightness < 200
        is_contrast = contrast > 20
        is_high_res = h >= 300 and w >= 300

        if not is_sharp:
            reason = "Image floue"
        elif not is_bright:
            reason = "Luminosité incorrecte"
        elif not is_contrast:
            reason = "Contraste faible"
        elif not is_high_res:
            reason = f"Résolution trop faible ({w}x{h})"
        else:
            reason = ""

        return {
            "valid": is_sharp and is_bright and is_contrast and is_high_res,
            "variance": variance,
            "brightness": brightness,
            "contrast": contrast,
            "resolution": {"width": w, "height": h},
            "reason": reason,
        }
    except Exception as e:
        return {"valid": False, "reason": str(e)}


def extract_text(image_data: bytes) -> str:
    try:
        img = Image.open(io.BytesIO(image_data)).convert('L')
        return pytesseract.image_to_string(img, lang='fra+eng').strip()
    except Exception as e:
        return ""


def enhance_image(image_data: bytes) -> bytes:
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            cropped = img[y:y+h, x:x+w]
            if w < 300 or h < 300:
                cropped = cv2.resize(cropped, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            _, buffer = cv2.imencode('.jpg', cropped, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            return buffer.tobytes()
        _, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        return buffer.tobytes()
    except Exception:
        return image_data
