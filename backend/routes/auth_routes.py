"""
Authentication routes for Clerk user management
"""
from flask import Blueprint, request, jsonify
from utils.db_client import get_user_by_clerk_id, create_or_update_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/sync-user', methods=['POST'])
def sync_user():
    """
    Sync Clerk user data to database
    Called from frontend after user signs in
    """
    data = request.json
    clerk_user_id = data.get('clerk_user_id')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    if not clerk_user_id or not email:
        return jsonify({"error": "clerk_user_id and email are required"}), 400
    
    try:
        # Create or update user
        user = create_or_update_user(clerk_user_id, email, first_name, last_name)
        
        existing_user = get_user_by_clerk_id(clerk_user_id)
        is_new = not existing_user
        
        print(f"✅ User {'created' if is_new else 'updated'}: {clerk_user_id}")
        return jsonify({
            "message": f"User {'created' if is_new else 'updated'} successfully",
            "user": user
        }), 201 if is_new else 200
            
    except Exception as e:
        print(f"❌ User sync error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/user/<clerk_user_id>', methods=['GET'])
def get_user(clerk_user_id):
    """Get user data by Clerk user ID"""
    try:
        user = get_user_by_clerk_id(clerk_user_id)
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
