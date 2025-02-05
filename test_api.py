import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file. Did you create it and add your key?")
else:
    print("GOOGLE_API_KEY loaded successfully from .env file.")

    # Configure generativeai with your API key
    genai.configure(api_key=api_key)

    # Optional: List available models to verify API connection
    try:
        models = [m.name for m in genai.list_models()]
        print("\nAvailable models (API connection verified):")
        for model in models:
            print(f"- {model}")
    except Exception as e:
        print(f"\nError connecting to Google AI Studio API: {e}")
        print("Please check your API key and network connection.")