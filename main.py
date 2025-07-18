from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = FastAPI()

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def read_root():
    return {"message": "AI Backend is running!"}

# 1️⃣ Article Generator
@app.post("/generate")
async def generate_article(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required."}

    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_token:
        return {"error": "Missing Replicate API token."}

    try:
        client = replicate.Client(api_token=replicate_token)
        output = client.run(
            "meta/llama-2-7b-chat",
            input={
                "prompt": prompt,
                "temperature": 0.7,
                "top_p": 1,
                "max_length": 1000,
                "repetition_penalty": 1.1
            }
        )
        article = "".join(output)
        return {"article": article}
    except Exception as e:
        return {"error": str(e)}

# 2️⃣ Text Humanizer
@app.post("/humanize")
async def humanize_text(request: Request):
    body = await request.json()
    raw_text = body.get("text", "")
    if not raw_text:
        return {"error": "Text is required."}

    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_token:
        return {"error": "Missing Replicate API token."}

    try:
        client = replicate.Client(api_token=replicate_token)
        output = client.run(
            "meta/llama-2-7b-chat",
            input={
                "prompt": f"Rewrite the following in a more human-like, natural tone:\n\n{raw_text}",
                "temperature": 0.75,
                "top_p": 1,
                "max_length": 1000,
                "repetition_penalty": 1.1
            }
        )
        humanized = "".join(output)
        return {"humanized": humanized}
    except Exception as e:
        return {"error": str(e)}

# 3️⃣ Text-to-Image Generator
@app.post("/generate-image")
async def generate_image(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required."}

    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_token:
        return {"error": "Missing Replicate API token."}

    try:
        client = replicate.Client(api_token=replicate_token)
        output = client.run(
            "stability-ai/sdxl",  # Or any other model you prefer
            input={"prompt": prompt}
        )
        return {"image_url": output[0]}  # Most models return image URL(s) in a list
    except Exception as e:
        return {"error": str(e)}
