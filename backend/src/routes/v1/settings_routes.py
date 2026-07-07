from flask import Blueprint, request, jsonify, current_app
from src.database.db import db
from src.models.user_model import User
from src.utils.auth import token_required
import requests

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
@token_required
def get_settings(current_user):
    """Get user settings including OpenRouter configuration"""
    return jsonify({
        "user": current_user.to_dict_with_key()
    })

@settings_bp.route('/settings', methods=['PUT'])
@token_required
def update_settings(current_user):
    """Update user settings"""
    data = request.json or {}
    
    if 'name' in data:
        current_user.name = data['name']
    if 'avatar' in data:
        current_user.avatar = data['avatar']
    if 'openrouter_api_key' in data:
        current_user.openrouter_api_key = data['openrouter_api_key']
    if 'openrouter_base_url' in data:
        current_user.openrouter_base_url = data['openrouter_base_url']
    if 'selected_model' in data:
        current_user.selected_model = data['selected_model']
    
    db.session.commit()
    
    return jsonify({
        "message": "Settings updated successfully",
        "user": current_user.to_dict_with_key()
    })

@settings_bp.route('/settings/models', methods=['GET', 'POST'])
@token_required
def get_available_models(current_user):
    """Fetch free available models from OpenRouter"""
    if request.method == 'POST':
        data = request.json or {}
        api_key = data.get('api_key') or current_user.openrouter_api_key
        base_url = data.get('base_url') or current_user.openrouter_base_url or 'https://openrouter.ai/api/v1'
    else:
        api_key = request.args.get('api_key') or current_user.openrouter_api_key
        base_url = request.args.get('base_url') or current_user.openrouter_base_url or 'https://openrouter.ai/api/v1'
    
    if not api_key:
        return jsonify({
            "models": [],
            "error": "OpenRouter API key not configured"
        }), 400
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{base_url}/models', headers=headers, timeout=10)
        
        if not response.ok:
            return jsonify({
                "models": [],
                "error": f"Failed to fetch models: {response.status_code}"
            }), response.status_code
        
        data = response.json()
        models = data.get('data', [])
        
        free_models = [
            {
                "id": model.get('id'),
                "name": model.get('name'),
                "description": model.get('description', ''),
                "context_length": model.get('context_length', 0),
                "pricing": model.get('pricing', {}),
                "is_free": model.get('pricing', {}).get('prompt', '0') == '0' and model.get('pricing', {}).get('completion', '0') == '0'
            }
            for model in models
            if model.get('pricing', {}).get('prompt', '0') == '0' and model.get('pricing', {}).get('completion', '0') == '0'
        ]
        
        return jsonify({
            "models": free_models
        })
    except requests.RequestException as e:
        return jsonify({
            "models": [],
            "error": f"Failed to connect to OpenRouter: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "models": [],
            "error": f"Error fetching models: {str(e)}"
        }), 500

@settings_bp.route('/settings/test-key', methods=['POST'])
@token_required
def test_api_key(current_user):
    """Test if the OpenRouter API key is valid"""
    data = request.json or {}
    api_key = data.get('api_key') or current_user.openrouter_api_key
    base_url = data.get('base_url') or current_user.openrouter_base_url or 'https://openrouter.ai/api/v1'
    
    if not api_key:
        return jsonify({"valid": False, "error": "API key is required"}), 400
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{base_url}/auth/key', headers=headers, timeout=10)
        
        if response.ok:
            key_data = response.json()
            return jsonify({
                "valid": True,
                "data": key_data
            })
        else:
            return jsonify({
                "valid": False,
                "error": f"Invalid API key: {response.status_code}"
            }), 401
    except requests.RequestException as e:
        return jsonify({
            "valid": False,
            "error": f"Connection error: {str(e)}"
        }), 500