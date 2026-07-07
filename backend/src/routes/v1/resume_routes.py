import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from src.services.resume_parser import parse_resume
from src.services.ats_checker import check_ats

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    Endpoint for uploading a resume PDF and parsing details.
    """
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
        
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    # Parse resume details
    parsed_data = parse_resume(filepath)
    # Check ATS compatibility
    ats_results = check_ats(parsed_data['text'])
    
    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": filename,
        "ats_score": ats_results['ats_score'],
        "matched_skills": ats_results['matched_skills'],
        "missing_skills": ats_results['missing_skills'],
        "education": parsed_data['education'],
        "experience": parsed_data['experience']
    })
