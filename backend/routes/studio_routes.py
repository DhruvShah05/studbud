"""
Studio tools routes - Chat, Mindmap, Flashcards, Quiz, Report
"""
import os
import time
from flask import Blueprint, request, jsonify, Response, stream_with_context
from utils.gemini_utils import (
    chat_with_sources_stream,
    generate_mindmap,
    generate_flashcards,
    generate_quiz,
    generate_report
)
from utils.db_client import (
    get_sources_text,
    save_chat_message,
    get_chat_history,
    clear_chat_history,
    save_studio_output,
    get_studio_outputs,
    delete_studio_output
)
import json

studio_bp = Blueprint('studio', __name__)


@studio_bp.route('/chat', methods=['POST'])
def chat():
    """
    Stream chat responses based on selected sources
    Real-time streaming like NotebookLM
    """
    data = request.json
    prompt = data.get('prompt')
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    
    if not prompt or not workspace_id:
        return jsonify({"error": "prompt and workspace_id are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids) if source_ids else ""
    
    if not sources_text and source_ids:
        return jsonify({"error": "No sources found"}), 404
    
    # Save user message
    save_chat_message(workspace_id, "user", prompt, source_ids)
    
    def generate():
        """Generator for streaming response"""
        full_response = ""
        try:
            for chunk in chat_with_sources_stream(prompt, sources_text):
                full_response += chunk
                # Send as SSE format
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Save assistant message
            save_chat_message(workspace_id, "assistant", full_response, source_ids)
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@studio_bp.route('/chat/history/<workspace_id>', methods=['GET'])
def get_history(workspace_id):
    """Get chat history for a workspace"""
    limit = request.args.get('limit', 50, type=int)
    history = get_chat_history(workspace_id, limit)
    return jsonify(history), 200


@studio_bp.route('/chat/clear/<workspace_id>', methods=['DELETE'])
def clear_history(workspace_id):
    """Clear chat history for a workspace"""
    success = clear_chat_history(workspace_id)
    
    if success:
        return jsonify({"message": "Chat history cleared"}), 200
    else:
        return jsonify({"error": "Failed to clear chat history"}), 500


@studio_bp.route('/mindmap', methods=['POST'])
def create_mindmap():
    """Generate a mindmap from selected sources"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Limit text length for processing
    max_length = 10000
    if len(sources_text) > max_length:
        sources_text = sources_text[:max_length] + "..."
    
    # Generate mindmap
    mindmap = generate_mindmap(sources_text)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="mindmap",
        content=mindmap,
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/flashcards', methods=['POST'])
def create_flashcards():
    """Generate flashcards from selected sources"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    count = data.get('count', 10)
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Limit text length
    max_length = 8000
    if len(sources_text) > max_length:
        sources_text = sources_text[:max_length] + "..."
    
    # Generate flashcards
    flashcards = generate_flashcards(sources_text, count)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="flashcards",
        content={"flashcards": flashcards},
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/quiz', methods=['POST'])
def create_quiz():
    """Generate a quiz from selected sources"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    count = data.get('count', 5)
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Limit text length
    max_length = 8000
    if len(sources_text) > max_length:
        sources_text = sources_text[:max_length] + "..."
    
    # Generate quiz
    quiz = generate_quiz(sources_text, count)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="quiz",
        content={"questions": quiz},
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/report', methods=['POST'])
def create_report():
    """Generate a report from selected sources"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    report_type = data.get('report_type', 'summary')
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Limit text length
    max_length = 15000
    if len(sources_text) > max_length:
        sources_text = sources_text[:max_length] + "..."
    
    # Generate report
    report = generate_report(sources_text, report_type)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="report",
        content={"report": report, "report_type": report_type},
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/outputs/<workspace_id>', methods=['GET'])
def get_outputs(workspace_id):
    """Get all studio outputs for a workspace"""
    output_type = request.args.get('type')
    outputs = get_studio_outputs(workspace_id, output_type)
    return jsonify(outputs), 200


@studio_bp.route('/outputs/<output_id>', methods=['DELETE'])
def delete_output(output_id):
    """Delete a studio output"""
    success = delete_studio_output(output_id)
    
    if success:
        return jsonify({"message": "Output deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete output"}), 500


@studio_bp.route('/audio-overview', methods=['POST'])
def create_audio_overview():
    """Generate a podcast-style audio overview script"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Generate audio overview
    from utils.gemini_utils import generate_audio_overview
    audio_script = generate_audio_overview(sources_text)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="audio_overview",
        content={"script": audio_script},
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/video-overview', methods=['POST'])
def create_video_overview():
    """Generate a video script overview"""
    data = request.json
    workspace_id = data.get('workspace_id')
    source_ids = data.get('source_ids', [])
    
    if not workspace_id or not source_ids:
        return jsonify({"error": "workspace_id and source_ids are required"}), 400
    
    # Get source texts
    sources_text = get_sources_text(source_ids)
    
    if not sources_text:
        return jsonify({"error": "No sources found"}), 404
    
    # Generate video overview
    from utils.gemini_utils import generate_video_overview
    video_script = generate_video_overview(sources_text)
    
    # Save output
    output = save_studio_output(
        workspace_id=workspace_id,
        output_type="video_overview",
        content={"script": video_script},
        source_ids=source_ids
    )
    
    return jsonify(output), 201


@studio_bp.route('/audio-overview/generate-audio', methods=['POST'])
def generate_audio_from_script():
    """Generate actual audio file from podcast script using Deepgram TTS"""
    data = request.json
    script = data.get('script')
    output_id = data.get('output_id')
    
    if not script:
        return jsonify({"error": "script is required"}), 400
    
    try:
        from utils.deepgram_utils import generate_podcast_audio
        import time
        
        # Generate unique filename
        audio_filename = f"podcast_{int(time.time())}.mp3"
        audio_path = os.path.join('audio_outputs', audio_filename)
        
        # Create directory if it doesn't exist
        os.makedirs('audio_outputs', exist_ok=True)
        
        # Generate audio
        output_path = generate_podcast_audio(script, audio_path)
        
        # Upload to S3 storage
        from utils.s3_client import upload_audio_file
        audio_url = upload_audio_file(output_path, audio_filename)
        
        return jsonify({
            "audio_url": audio_url,
            "filename": audio_filename,
            "message": "Audio generated successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
