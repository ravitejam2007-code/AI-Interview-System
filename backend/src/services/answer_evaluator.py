import json
import re
from src.services.openrouter_service import get_openrouter_service
from src.services.answer_validator import is_valid_answer, is_gibberish
from src.services.expected_answers import EXPECTED_ANSWERS


def normalize_question(question):
    """Remove leading numbers, bullets, and extra whitespace from question text."""
    q = question.strip()
    q = re.sub(r'^[\d]+\.\s*', '', q)
    q = re.sub(r'^[-*]\s*', '', q)
    return q.strip()


def keyword_score(question, answer):
    normalized_question = normalize_question(question)
    entry = EXPECTED_ANSWERS.get(normalized_question)
    if not entry:
        return None

    keywords = entry["keywords"]
    answer_lower = answer.lower()
    matches = 0

    for keyword in keywords:
        if keyword.lower() in answer_lower:
            matches += 1

    score = int((matches / len(keywords)) * 100) if keywords else 0
    return score


def evaluate_answer(question, user_answer, resume_context="", api_key=None, user=None):
    if not api_key and not (user and user.openrouter_api_key):
        return {
            "technical_score": 0,
            "confidence_score": 0,
            "feedback": "API key not configured. Cannot evaluate answer."
        }

    if not is_valid_answer(user_answer):
        return {
            "technical_score": 0,
            "confidence_score": 0,
            "feedback": "The answer appears to be incomplete or nonsensical. Please provide a meaningful response related to the question."
        }

    if is_gibberish(user_answer):
        return {
            "technical_score": 0,
            "confidence_score": 0,
            "feedback": "The answer does not appear to be a valid response. Please provide a thoughtful answer related to the question."
        }

    kw_score = keyword_score(question, user_answer)
    if kw_score is not None and kw_score < 20:
        return {
            "technical_score": kw_score,
            "confidence_score": max(0, kw_score - 10),
            "feedback": "Your answer does not cover the key concepts expected for this question. Review the fundamental topics related to the question and try again."
        }

    try:
        service = get_openrouter_service(user) if user else None

        normalized_question = normalize_question(question)
        entry = EXPECTED_ANSWERS.get(normalized_question)
        expected_section = ""
        if entry:
            expected_section = f"""
Expected Concepts (key topics the answer should cover):
{entry["expected_answer"]}

Keywords that should appear in a good answer:
{", ".join(entry["keywords"])}
"""

        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer.

Question:
{question}
{expected_section}
Candidate Answer:
{user_answer}

Resume Context (skills, experience):
{resume_context[:1500]}

Instructions:
1. Check if the answer is meaningful and addresses the question.
2. Detect gibberish, random text, or irrelevant answers.
3. If the answer is gibberish or completely off-topic:
   - Technical Score = 0
   - Confidence Score = 0
   - Give short corrective feedback asking for a proper answer.
4. If partially correct:
   - Score proportionally based on how many key concepts are covered.
5. If the answer is strong and covers most expected concepts, score accordingly.
6. Return JSON only, no other text.

Return exactly this JSON structure:
{{
  "technical_score": <integer 0-100>,
  "confidence_score": <integer 0-100>,
  "feedback": "<2-3 sentences: what was good, what to improve, specific actionable advice>"
}}"""
        system_prompt = "You are a senior technical interviewer. Evaluate the candidate's answer and return ONLY a JSON object with technical_score, confidence_score, and feedback fields."

        if service:
            response = service.generate_content(prompt, system_prompt=system_prompt, temperature=0.3, max_tokens=500)
        else:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt).text

        if response:
            text = response.strip()
            if text.startswith('```json'):
                text = text[7:-3].strip()
            elif text.startswith('```'):
                text = text[3:-3].strip()

            result = json.loads(text)
            llm_score = max(0, min(100, int(result.get("technical_score", 0))))

            if kw_score is not None:
                final_score = int((llm_score * 0.6) + (kw_score * 0.4))
            else:
                final_score = llm_score

            return {
                "technical_score": final_score,
                "confidence_score": max(0, min(100, int(result.get("confidence_score", 0)))),
                "feedback": result.get("feedback", "No feedback generated.")
            }
    except Exception as e:
        print(f"Answer evaluation error: {e}")

    if kw_score is not None:
        return {
            "technical_score": kw_score,
            "confidence_score": max(0, kw_score - 20),
            "feedback": "Evaluation based on keyword coverage. Your answer was scored on how well it covered expected topics."
        }

    return {
        "technical_score": 0,
        "confidence_score": 0,
        "feedback": "Evaluation failed. Please try again."
    }
