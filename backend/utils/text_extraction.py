"""
Text extraction utilities using Gemini API
Sends files directly to Gemini without local preprocessing
Supports PDF, DOCX, TXT, and images
"""
import base64
import os
from google import genai
from google.genai import types
from config import Config


def get_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    extension = filename.lower().split('.')[-1]
    mime_types = {
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'txt': 'text/plain',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'webp': 'image/webp',
    }
    return mime_types.get(extension, 'application/octet-stream')


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extract text from file bytes by sending directly to Gemini
    Supports PDF, DOCX, images, and text files
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Get file extension and MIME type
        extension = filename.lower().split('.')[-1]
        mime_type = get_mime_type(filename)
        
        # Handle plain text files directly
        if extension == 'txt':
            try:
                return file_bytes.decode('utf-8').strip()
            except UnicodeDecodeError:
                # If decoding fails, let Gemini handle it
                pass
        
        # Encode file to base64
        file_data = base64.standard_b64encode(file_bytes).decode('utf-8')
        
        # Create prompt for text extraction
        prompt = """Extract all text content from this document. 
        
Instructions:
- Extract ALL text, maintaining the original structure and formatting as much as possible
- Include headings, paragraphs, lists, tables, and any other text content
- For images with text, perform OCR to extract the text
- Preserve the logical flow and organization of the content
- Do NOT add any commentary or explanations
- Return ONLY the extracted text content

Extracted text:"""
        
        # Prepare content with file
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(
                        data=base64.standard_b64decode(file_data),
                        mime_type=mime_type
                    ),
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        
        # Configure generation
        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=0,
            ),
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE",
                ),
            ],
            response_mime_type="text/plain",
            temperature=0.1,  # Low temperature for accurate extraction
        )
        
        # Generate content
        model = "gemini-2.0-flash-exp"
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        
        # Return extracted text
        extracted_text = response.text.strip()
        
        if not extracted_text:
            return f"Warning: No text could be extracted from {filename}"
        
        return extracted_text
        
    except Exception as e:
        return f"Error extracting text from {filename}: {str(e)}"


def extract_text(file_path: str) -> str:
    """
    Extract text from a file path by reading and sending to Gemini
    """
    try:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        
        filename = os.path.basename(file_path)
        return extract_text_from_bytes(file_bytes, filename)
        
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"
