"""
Source document management routes
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.db_client import (
    create_source,
    get_sources,
    get_source,
    delete_source
)
from utils.s3_client import upload_file_to_storage
from utils.text_extraction import extract_text_from_bytes
import os

source_bp = Blueprint('source', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@source_bp.route('/upload', methods=['POST'])
def upload_source():
    """Upload and process a source document"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    workspace_id = request.form.get('workspace_id')
    
    if not workspace_id:
        return jsonify({"error": "workspace_id is required"}), 400
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    try:
        # Read file bytes
        file_bytes = file.read()
        filename = secure_filename(file.filename)
        file_type = filename.rsplit('.', 1)[1].lower()
        
        # Extract text
        extracted_text = extract_text_from_bytes(file_bytes, filename)
        
        if extracted_text.startswith("Error"):
            return jsonify({"error": extracted_text}), 500
        
        # Upload to S3 storage
        file_url = upload_file_to_storage(file_bytes, filename, workspace_id)
        
        if not file_url:
            return jsonify({"error": "Failed to upload file to storage"}), 500
        
        # Create source record
        source = create_source(
            workspace_id=workspace_id,
            filename=filename,
            file_type=file_type,
            file_url=file_url,
            extracted_text=extracted_text
        )
        
        if source:
            return jsonify(source), 201
        else:
            return jsonify({"error": "Failed to create source record"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@source_bp.route('/list/<workspace_id>', methods=['GET'])
def list_sources(workspace_id):
    """Get all sources for a workspace"""
    sources = get_sources(workspace_id)
    return jsonify(sources), 200


@source_bp.route('/<source_id>', methods=['GET'])
def get_source_route(source_id):
    """Get a specific source"""
    source = get_source(source_id)
    
    if source:
        return jsonify(source), 200
    else:
        return jsonify({"error": "Source not found"}), 404


@source_bp.route('/<source_id>', methods=['DELETE'])
def delete_source_route(source_id):
    """Delete a source"""
    try:
        # Get source to retrieve file URL
        source = get_source(source_id)
        if not source:
            return jsonify({"error": "Source not found"}), 404
        
        # Delete file from S3
        from utils.s3_client import delete_file_from_storage
        delete_file_from_storage(source['file_url'])
        
        # Delete from database
        success = delete_source(source_id)
        
        if success:
            return jsonify({"message": "Source deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete source from database"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
