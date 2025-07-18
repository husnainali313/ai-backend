from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow CORS (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def read_root():
    return {"message": "AI Backend is running!"}

# Article generation route
@app.post("/generate")
async def generate_article(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    # Check for empty prompt
    if not prompt:
        return {"error": "Prompt is required."}

    # Use your Replicate API token
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_token:
        return {"error": "Missing Replicate API token."}

    replicate_client = replicate.Client(api_token=replicate_token)

    try:
        output = replicate_client.run(
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
