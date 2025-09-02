# utils/openai_caption.py
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

def _build_client():
    endpoint = os.getenv("ENDPOINT_URL").rstrip("/")
    api_version = os.getenv("OPENAI_API_VERSION")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    # If a key is present, use it (good for local dev).
    if api_key:
        return AzureOpenAI(
            azure_endpoint=endpoint,
            api_version=api_version,
            api_key=api_key,
        )

    # Otherwise use Managed Identity via Azure AD token provider.
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_version=api_version,
        azure_ad_token_provider=token_provider,
    )

client = _build_client()

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")

def generate_caption(tags):
    tag_text = ", ".join(tags)
    prompt = f"""
    You are an assistant that generates vivid, natural-sounding captions for images.
    Create a one-line caption for an image that contains the following: {tag_text}.
    """

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Azure OpenAI error: {e}")
        return "A beautiful scene, captured perfectly."