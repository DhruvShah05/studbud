"""
Deepgram Text-to-Speech utilities
Convert podcast scripts to audio
"""
import os
import time

try:
    from deepgram import DeepgramClient, SpeakOptions
    DEEPGRAM_AVAILABLE = True
except ImportError:
    DEEPGRAM_AVAILABLE = False
    print("Warning: Deepgram SDK not installed. Audio generation will not work.")

from config import Config

def clean_text_for_speech(text: str) -> str:
    """
    Clean text to remove markdown and special characters
    """
    import re
    
    # Remove markdown headers (# ## ###)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove asterisks used for emphasis (**, *, ****, etc.)
    text = re.sub(r'\*+', '', text)
    
    # Remove brackets and their content [Music], [Intro], etc.
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove stage directions in parentheses if at start of line
    text = re.sub(r'^\(.*?\)\s*', '', text, flags=re.MULTILINE)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def parse_podcast_script(script: str) -> list:
    """
    Parse podcast script into speaker segments
    Returns list of (speaker, text) tuples
    """
    segments = []
    lines = script.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip lines that are just formatting
        if line.startswith('#') or line.startswith('[') or line.startswith('**'):
            continue
            
        if line.startswith('Alex:'):
            text = line.replace('Alex:', '').strip()
            text = clean_text_for_speech(text)
            if text:
                segments.append(('alex', text))
        elif line.startswith('Sam:'):
            text = line.replace('Sam:', '').strip()
            text = clean_text_for_speech(text)
            if text:
                segments.append(('sam', text))
        elif line and not line.startswith('[') and not line.startswith('#'):
            # Narrator or description
            text = clean_text_for_speech(line)
            if text:
                segments.append(('narrator', text))
    
    return segments


def generate_podcast_audio(script: str, output_path: str = None) -> str:
    """
    Generate podcast audio from script using Deepgram TTS
    Returns path to generated audio file
    """
    if not DEEPGRAM_AVAILABLE:
        raise Exception("Deepgram SDK not installed. Run: pip install deepgram-sdk")
    
    if not Config.DEEPGRAM_API_KEY:
        raise Exception("Deepgram API key not configured in .env file")
    
    try:
        # Initialize Deepgram client
        deepgram = DeepgramClient(Config.DEEPGRAM_API_KEY)
        
        # Parse script into segments
        segments = parse_podcast_script(script)
        
        if not segments:
            raise Exception("No valid segments found in script")
        
        # Create output directory if needed
        if not output_path:
            os.makedirs('audio_outputs', exist_ok=True)
            output_path = f"audio_outputs/podcast_{int(time.time())}.mp3"
        
        # Combine all text
        full_text = "\n\n".join([text for _, text in segments if text])
        
        if not full_text:
            raise Exception("No text to convert to audio")
        
        # Deepgram has a 2000 character limit, so we need to chunk the text
        MAX_CHARS = 1800  # Leave some buffer
        
        # If text is short enough, generate directly
        if len(full_text) <= MAX_CHARS:
            options = SpeakOptions(
                model="aura-asteria-en",
            )
            
            response = deepgram.speak.v("1").save(
                output_path,
                {"text": full_text},
                options
            )
            
            return output_path
        
        # Otherwise, create a summary version
        # Take first 1800 characters and add a note
        truncated_text = full_text[:MAX_CHARS]
        # Find last complete sentence
        last_period = truncated_text.rfind('.')
        if last_period > 0:
            truncated_text = truncated_text[:last_period + 1]
        
        truncated_text += "\n\nNote: This is a preview. The full podcast script is too long for audio generation. Please download the script for the complete content."
        
        options = SpeakOptions(
            model="aura-asteria-en",
        )
        
        response = deepgram.speak.v("1").save(
            output_path,
            {"text": truncated_text},
            options
        )
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Deepgram TTS failed: {str(e)}")


def generate_simple_audio(text: str, output_path: str = None, voice: str = 'aura-asteria-en') -> str:
    """
    Generate simple audio from text
    Useful for single-speaker content
    """
    if not DEEPGRAM_AVAILABLE:
        raise Exception("Deepgram SDK not installed")
    
    if not Config.DEEPGRAM_API_KEY:
        raise Exception("Deepgram API key not configured")
    
    try:
        deepgram = DeepgramClient(Config.DEEPGRAM_API_KEY)
        
        if not output_path:
            os.makedirs('audio_outputs', exist_ok=True)
            output_path = f"audio_outputs/audio_{int(time.time())}.mp3"
        
        options = SpeakOptions(
            model=voice,
        )
        
        response = deepgram.speak.v("1").save(
            output_path,
            {"text": text},
            options
        )
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Deepgram TTS failed: {str(e)}")


# Available Deepgram voices
AVAILABLE_VOICES = {
    'aura-asteria-en': 'Female - Warm and engaging',
    'aura-luna-en': 'Female - Clear and professional',
    'aura-stella-en': 'Female - Friendly and conversational',
    'aura-athena-en': 'Female - Authoritative',
    'aura-hera-en': 'Female - Calm and soothing',
    'aura-orion-en': 'Male - Deep and resonant',
    'aura-arcas-en': 'Male - Professional and clear',
    'aura-perseus-en': 'Male - Energetic',
    'aura-angus-en': 'Male - Warm and friendly',
    'aura-orpheus-en': 'Male - Smooth and articulate',
    'aura-helios-en': 'Male - Confident',
    'aura-zeus-en': 'Male - Commanding'
}
