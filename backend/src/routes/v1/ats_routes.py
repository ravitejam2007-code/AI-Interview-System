from flask import Blueprint, request, jsonify
from src.services.ats_checker import check_ats

ats_bp = Blueprint('ats', __name__)

@ats_bp.route('/ats-score', methods=['POST'])
def ats_score():
    """
    Endpoint for scoring resume text against defined job skills.
    """
    data = request.json or {}
    resume_text = data.get('resume_text', '')
    skills = data.get('skills', [])
    
    if not resume_text:
        return jsonify({"error": "Resume text is required"}), 400
        
    results = check_ats(resume_text, skills)
    return jsonify(results)

@ats_bp.route('/results', methods=['GET'])
def get_results():
    """
    Endpoint for fetching final mock interview performance results.
    """
    return jsonify({
        "status": "success",
        "performance": {
            "ats_score": 85,
            "confidence": 88,
            "technical_accuracy": 92,
            "communication": "Excellent"
        }
    })
