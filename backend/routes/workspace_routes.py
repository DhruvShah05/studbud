"""
Workspace management routes
"""
from flask import Blueprint, request, jsonify
from utils.db_client import (
    create_workspace,
    get_workspaces,
    get_workspace,
    update_workspace,
    delete_workspace,
    get_user_by_clerk_id
)

workspace_bp = Blueprint('workspace', __name__)


def get_db_user_id(clerk_user_id: str) -> str:
    """Convert Clerk user ID to database user UUID"""
    try:
        user = get_user_by_clerk_id(clerk_user_id)
        if user:
            return user['id']
        return None
    except Exception as e:
        print(f"Error getting database user ID: {e}")
        return None


@workspace_bp.route('/create', methods=['POST'])
def create_workspace_route():
    """Create a new workspace"""
    data = request.json
    clerk_user_id = data.get('user_id', 'default_user')
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({"error": "Workspace name is required"}), 400
    
    # Convert Clerk user ID to database UUID
    user_id = get_db_user_id(clerk_user_id)
    if not user_id:
        return jsonify({"error": "User not found. Please sign in again."}), 404
    
    workspace = create_workspace(user_id, name, description)
    
    if workspace:
        return jsonify(workspace), 201
    else:
        return jsonify({"error": "Failed to create workspace"}), 500


@workspace_bp.route('/list', methods=['GET'])
def list_workspaces_route():
    """Get all workspaces for a user"""
    clerk_user_id = request.args.get('user_id', 'default_user')
    
    # Convert Clerk user ID to database UUID
    user_id = get_db_user_id(clerk_user_id)
    if not user_id:
        return jsonify({"error": "User not found. Please sign in again."}), 404
    
    workspaces = get_workspaces(user_id)
    return jsonify(workspaces), 200


@workspace_bp.route('/<workspace_id>', methods=['GET'])
def get_workspace_route(workspace_id):
    """Get a specific workspace"""
    workspace = get_workspace(workspace_id)
    
    if workspace:
        return jsonify(workspace), 200
    else:
        return jsonify({"error": "Workspace not found"}), 404


@workspace_bp.route('/<workspace_id>', methods=['PUT'])
def update_workspace_route(workspace_id):
    """Update workspace details"""
    data = request.json
    name = data.get('name')
    description = data.get('description')
    
    workspace = update_workspace(workspace_id, name, description)
    
    if workspace:
        return jsonify(workspace), 200
    else:
        return jsonify({"error": "Failed to update workspace"}), 500


@workspace_bp.route('/<workspace_id>', methods=['DELETE'])
def delete_workspace_route(workspace_id):
    """Delete a workspace"""
    success = delete_workspace(workspace_id)
    
    if success:
        return jsonify({"message": "Workspace deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete workspace"}), 500
