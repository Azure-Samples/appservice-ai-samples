
# App Service AI Samples

This repository contains sample projects, primarily written in Python, that demonstrate how to build and deploy AI applications on Azure App Service. Each sample is designed to showcase best practices for integrating AI capabilities and deploying scalable web apps to Azure.

## Quick start (any sample)

```bash
# 1) Clone the repo
git clone https://github.com/Azure-Samples/appservice-ai-samples.git
cd appservice-ai-samples

# 2) Pick a sample
cd <sample-folder>   # e.g., lowlight-enhancer

# 3) Initialize and deploy
azd init
azd up
```

> Prereqs: An Azure subscription and the Azure Developer CLI (`azd`) installed.


## Sample Projects

1. [**langchain-fastapi-chat**](https://github.com/Azure-Samples/appservice-ai-samples/tree/main/langchain-fastapi-chat): A FastAPI web app using LangChain and Azure OpenAI (gpt-4o) for conversational AI, featuring streaming responses and summaries. Includes Bicep templates for easy deployment to App Service.

    **Blog:** [https://techcommunity.microsoft.com/blog/appsonazureblog/deploy-langchain-applications-to-azure-app-service/4440640](https://techcommunity.microsoft.com/blog/appsonazureblog/deploy-langchain-applications-to-azure-app-service/4440640)

2. [**image-caption-app**](https://github.com/Azure-Samples/appservice-ai-samples/tree/main/image_caption_app): A **Streamlit** app that generates natural-language captions for uploaded images using an LLM + vision pipeline. Demonstrates a simple, user-friendly UI with drag-and-drop, promptable captioning, and an App Service–ready structure.

    **Blog:** [https://techcommunity.microsoft.com/blog/appsonazureblog/build-an-ai-image-caption-generator-on-azure-app-service-with-streamlit-and-gpt-/4450313](https://techcommunity.microsoft.com/blog/appsonazureblog/build-an-ai-image-caption-generator-on-azure-app-service-with-streamlit-and-gpt-/4450313)

3. [**gpt-oss-20b-sample**](https://github.com/Azure-Samples/appservice-ai-samples/tree/main/gpt-oss-20b-sample): A lightweight chat app that calls the **GPT-OSS-20B** model with a minimal web UI and clear, configurable prompts. Shows a clean scaffolding for inference calls, streaming responses, and environment-based configuration

    **Blog:** [https://techcommunity.microsoft.com/blog/appsonazureblog/build-lightweight-ai-apps-on-azure-app-service-with-gpt-oss-20b/4442885](https://techcommunity.microsoft.com/blog/appsonazureblog/build-lightweight-ai-apps-on-azure-app-service-with-gpt-oss-20b/4442885)

4. [**lowlight-enhancer**](https://github.com/Azure-Samples/appservice-ai-samples/tree/main/lowlight-enhancer): A tiny **Flask + OpenCV** web app that improves dim photos (CLAHE → gamma → brightness → subtle saturation). CPU-friendly, no heavyweight model required; instant before/after preview in the browser and a minimal code path that’s easy to extend.

    **Blog:** [https://techcommunity.microsoft.com/blog/appsonazureblog/low-light-image-enhancer-python--opencv-on-azure-app-service/4466837](https://techcommunity.microsoft.com/blog/appsonazureblog/low-light-image-enhancer-python--opencv-on-azure-app-service/4466837)

## Resources

Useful documentation and related resources:

- [Azure App Service Documentation](https://learn.microsoft.com/en-us/azure/app-service/)
- [Python Quickstart for Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [AI Integration with Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/overview-ai-integration)

