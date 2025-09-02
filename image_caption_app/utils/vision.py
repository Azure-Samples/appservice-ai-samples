# utils/vision.py
import os
import requests
from azure.identity import DefaultAzureCredential

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT").rstrip("/")
VISION_API_URL = f"{VISION_ENDPOINT}/vision/v3.2/analyze"

PARAMS = {
    "visualFeatures": "Tags,Description",
    "language": "en"
}

def get_vision_headers():
    # Prefer key if provided (useful locally or while MI is being fixed in Azure)
    vision_key = os.getenv("VISION_KEY")
    if vision_key:
        return {
            "Ocp-Apim-Subscription-Key": vision_key,
            "Content-Type": "application/octet-stream",
        }

    # Otherwise, use Managed Identity / AAD
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default").token
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }

def extract_tags(image_bytes):
    try:
        headers = get_vision_headers()
        response = requests.post(
            VISION_API_URL,
            headers=headers,
            params=PARAMS,
            data=image_bytes,
            timeout=30,
        )
        response.raise_for_status()
        analysis = response.json()

        tags = [
            t.get('name')
            for t in analysis.get('tags', [])
            if t.get('name') and t.get('confidence', 0) > 0.6
        ]
        if not tags:
            tags = analysis.get('description', {}).get('tags', [])

        return tags[:6] if tags else ["image"]

    except Exception as e:
        # Log enough context to diagnose in App Service logs
        print(f"Azure Vision API error: {e}")
        return ["image"]
