# README.md

# 🖼️ AI Image Caption Generator with Streamlit

This Streamlit app allows users to upload an image and receive an AI-generated caption using:

- **Azure Computer Vision API**: Extracts visual tags from the image.
- **Azure OpenAI (GPT-4o-mini)**: Generates a natural caption based on those tags.

---

## 📦 Requirements

- Python 3.8 or higher
- Azure OpenAI resource (with GPT-4o or GPT-4o-mini deployment)
- Azure Cognitive Services (Computer Vision API)

---

## 🚀 Running Locally

### 1. Clone this repo and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Set the following environment variables (use a `.env` file or export manually):
```bash
# .env (for local dev)
OPENAI_ENDPOINT=<your_openai_endpoint>
OPENAI_API_KEY=<your_openai_key>
OPENAI_DEPLOYMENT=<your_deployment_name>
OPENAI_API_VERSION=2024-12-01-preview

VISION_ENDPOINT=https://streamlit-cv.cognitiveservices.azure.com/
VISION_KEY=<your_vision_key>
```

Then run:
```bash
streamlit run app.py
```

---

## 🔐 Switching to Managed Identity (Optional)

For production deployments:
- Use `DefaultAzureCredential` from `azure.identity` instead of key-based auth
- Ensure your App Service or container has **System Assigned Identity** with roles:
  - **Cognitive Services User** for both resources

---

## 🧠 How It Works
1. User uploads an image.
2. Azure Vision API returns relevant tags like `dog`, `beach`, `sunset`.
3. A prompt is constructed and sent to Azure OpenAI.
4. GPT-4o generates a short caption (1–2 lines).
5. The app displays the image and its caption side-by-side.

---

## 📸 Example Output
> *"A playful golden retriever runs along the beach at sunset."*

---

## 🛠 Future Improvements
- Use GPT-4o image input directly (if supported)
- Add tone/style options for captions
- Support batch captioning for image folders

---

Built with ❤️ using Python, Streamlit, and Azure AI.
