from flask import Blueprint, request, jsonify, current_app
from src.services.question_generator import generate_interview_questions
from src.services.emotion_detector import analyze_face_emotions

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/generate-questions', methods=['POST'])
@interview_bp.route('/generate', methods=['POST'])
def generate_questions():
    """
    Endpoint for generating technical questions based on resume text or skills.
    """
    data = request.json or {}
    resume_text = data.get('resume_text', '')
    skills = data.get('skills', [])
    
    if not skills and not resume_text:
        # Use default skills as fallback
        skills = ["python", "machine learning", "sql", "react"]
        
    if not skills and resume_text:
        from src.services.resume_parser import extract_skills
        skills = extract_skills(resume_text)
        
    api_key = current_app.config.get('GEMINI_API_KEY')
    questions = generate_interview_questions(skills, resume_text, api_key=api_key)
    
    # Backwards compatible formatting: join list with newlines
    questions_str = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    return jsonify({
        "questions": questions_str
    })

@interview_bp.route('/emotion', methods=['POST'])
def detect_emotion():
    """
    Endpoint for detecting facial emotion metrics.
    """
    # Simply delegates to emotion detection service
    emotions = analyze_face_emotions()
    return jsonify(emotions)

@interview_bp.route('/chat', methods=['POST'])
def chatbot_response():
    """
    Endpoint for the AI Chatbot widget.
    """
    data = request.json or {}
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
        
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({"reply": "I'm currently in offline mode because the Gemini API key is not configured."})
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"You are a helpful AI Interview Coach. Answer the following user query concisely and provide actionable advice. Query: {message}")
        
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({"reply": "I'm having trouble connecting right now. Please try again later."})
