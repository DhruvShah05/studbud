"""
Gemini AI utilities using the new google-genai SDK
Supports streaming, JSON mode, and function calling
"""
from google import genai
from google.genai import types
from utils.global_client import get_client
import json

client = get_client()

# Safety settings for all requests (EXACT format from your example)
SAFETY_SETTINGS = [
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
]


def chat_with_sources_stream(prompt: str, sources_text: str):
    """
    Stream chat responses based on source documents
    Yields text chunks in real-time
    """
    full_prompt = f"""You are an AI research assistant with access to specific source documents.

IMPORTANT INSTRUCTIONS:
- Use ONLY the information from the sources provided below
- Cite sources when making claims
- If the answer is not in the sources, say so clearly
- Be comprehensive but concise

SOURCES:
{sources_text}

USER QUESTION:
{prompt}

Please provide a detailed answer based on the sources above."""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=full_prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="text/plain",
        temperature=0.7,
    )

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error: {str(e)}"


def generate_mindmap(text: str) -> dict:
    """
    Generate a hierarchical mindmap from text
    Returns JSON structure
    """
    prompt = f"""Convert the following text into a hierarchical mindmap structure.

Analyze the content and create a logical hierarchy with a main topic and subtopics.

Return ONLY valid JSON in this exact format:
{{
  "topic": "Main Topic",
  "children": [
    {{
      "topic": "Subtopic 1",
      "children": [
        {{"topic": "Detail 1"}},
        {{"topic": "Detail 2"}}
      ]
    }},
    {{
      "topic": "Subtopic 2",
      "children": [
        {{"topic": "Detail 3"}}
      ]
    }}
  ]
}}

TEXT TO ANALYZE:
{text}

Return only the JSON structure, no additional text."""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="application/json",
        temperature=0.5,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e), "topic": "Error generating mindmap"}


def generate_flashcards(text: str, count: int = 10) -> list:
    """
    Generate flashcards from text
    Returns list of question-answer pairs
    """
    prompt = f"""Create {count} educational flashcards from the following text.

Each flashcard should have a clear question and a concise answer.
Focus on key concepts, definitions, and important facts.

Return ONLY valid JSON in this exact format:
[
  {{
    "question": "What is...",
    "answer": "..."
  }},
  {{
    "question": "How does...",
    "answer": "..."
  }}
]

TEXT TO ANALYZE:
{text}

Return only the JSON array, no additional text."""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="application/json",
        temperature=0.6,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return json.loads(response.text)
    except Exception as e:
        return [{"error": str(e), "question": "Error", "answer": "Failed to generate flashcards"}]


def generate_quiz(text: str, count: int = 5) -> list:
    """
    Generate multiple choice quiz from text
    Returns list of questions with options and correct answer
    """
    prompt = f"""Create {count} multiple choice quiz questions from the following text.

Each question should have:
- A clear question
- 4 options (A, B, C, D)
- The correct answer indicated

Return ONLY valid JSON in this exact format:
[
  {{
    "question": "What is...",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": "Option A",
    "explanation": "Brief explanation of why this is correct"
  }}
]

TEXT TO ANALYZE:
{text}

Return only the JSON array, no additional text."""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="application/json",
        temperature=0.6,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return json.loads(response.text)
    except Exception as e:
        return [{"error": str(e), "question": "Error", "options": [], "correct": "", "explanation": "Failed to generate quiz"}]


def generate_report(text: str, report_type: str = "summary") -> str:
    """
    Generate a comprehensive report from text
    Returns markdown formatted report
    """
    report_prompts = {
        "summary": "Create a comprehensive summary report with key points, main ideas, and conclusions.",
        "analysis": "Create an analytical report examining themes, patterns, and insights from the content.",
        "study_guide": "Create a study guide with sections for overview, key concepts, important details, and review questions.",
        "brief": "Create a brief executive summary highlighting the most critical information.",
    }

    prompt_instruction = report_prompts.get(report_type, report_prompts["summary"])

    prompt = f"""{prompt_instruction}

Structure the report with clear sections using markdown formatting:
- Use ## for main sections
- Use ### for subsections
- Use bullet points for lists
- Use **bold** for emphasis
- Include 5-7 well-organized sections

TEXT TO ANALYZE:
{text}

Generate a professional, well-structured report in markdown format."""

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="text/plain",
        temperature=0.7,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except Exception as e:
        return f"# Error Generating Report\n\n{str(e)}"


def generate_audio_overview(sources_text: str) -> str:
    """
    Generate a podcast-style audio overview script
    Like NotebookLM's Audio Overview feature
    """
    model = "gemini-2.5-flash"
    
    prompt = f"""You are creating a podcast-style audio overview script based on the following content.

Create an engaging, conversational dialogue between two hosts discussing the key concepts:
- Host 1 (Alex): The curious learner who asks questions
- Host 2 (Sam): The knowledgeable expert who explains concepts

IMPORTANT FORMATTING RULES FOR AUDIO:
- Use ONLY plain text - NO markdown, NO asterisks, NO hashtags, NO special characters
- Use simple speaker labels: "Alex:" and "Sam:" at the start of each line
- Do NOT use headers, titles, or section markers
- Do NOT use asterisks (****) or any emphasis markers
- Do NOT include stage directions in brackets like [Music] or [Intro]
- Write ONLY the actual spoken dialogue
- Keep it conversational and natural
- 5-7 minute conversation length

Example format:
Alex: Hey Sam, can you explain what data structures are?
Sam: Sure! Data structures are ways to organize and store data efficiently.
Alex: That makes sense. Can you give me an example?
Sam: Of course! Think of an array like a row of mailboxes...

Content to discuss:
{sources_text[:15000]}

Generate the podcast script with ONLY plain text dialogue:"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="text/plain",
        temperature=0.8,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Audio overview generation failed: {str(e)}")


def generate_video_overview(sources_text: str) -> str:
    """
    Generate a video script overview
    """
    model = "gemini-2.5-flash"
    
    prompt = f"""Create a video script for an educational video based on the following content.

Include:
- Opening hook (10 seconds)
- Main content sections with visual cues
- Key points with timestamps
- Closing summary
- Suggested visuals/animations

Format:
[00:00-00:10] OPENING
[Visual: Animated title]
Script: "..."

Content:
{sources_text[:15000]}

Generate the video script:"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="text/plain",
        temperature=0.7,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Video overview generation failed: {str(e)}")


def simple_chat(prompt: str, system_instruction: str = None) -> str:
    """
    Simple non-streaming chat for general queries
    """
    if system_instruction:
        full_prompt = f"{system_instruction}\n\n{prompt}"
    else:
        full_prompt = prompt

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=full_prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        safety_settings=SAFETY_SETTINGS,
        response_mime_type="text/plain",
        temperature=0.8,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
