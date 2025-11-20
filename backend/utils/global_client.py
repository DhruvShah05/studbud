"""
Global Gemini Client using the new google-genai SDK
"""
from google import genai
import os
from config import Config

# Initialize the Gemini client
client = genai.Client(
    api_key=Config.GEMINI_API_KEY
)

def get_client():
    """Get the global Gemini client instance"""
    return client
