import os
import random
import google.generativeai as genai

STATIC_QUESTIONS = {
    "python": [
        "Explain decorators in Python and their common use cases.",
        "What is the difference between a list and a tuple in Python?",
        "Explain Python's memory management and garbage collection.",
        "What are generators and yield in Python?"
    ],
    "machine learning": [
        "Explain the bias-variance tradeoff in Machine Learning.",
        "What is gradient descent and how does it work?",
        "What is the difference between overfitting and underfitting, and how do you prevent them?",
        "Explain how a Random Forest classifier works."
    ],
    "flask": [
        "What is Flask and why is it called a microframework?",
        "How do you handle request parameters and route variables in Flask?",
        "Explain application context and request context in Flask.",
        "How do you implement database migrations in Flask?"
    ],
    "sql": [
        "What is the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN?",
        "What are indexes in SQL and how do they improve query performance?",
        "Explain the ACID properties of a database transaction.",
        "What is normalization and why is it important?"
    ],
    "react": [
        "What are React Hooks and why were they introduced?",
        "Explain the virtual DOM and how React renders components.",
        "What is the difference between state and props in React?",
        "How do you manage global state in a React application?"
    ],
    "javascript": [
        "What is a closure in JavaScript?",
        "Explain the difference between let, const, and var.",
        "What is the event loop in JavaScript and how does it work?",
        "Explain promises and async/await syntax."
    ],
    "docker": [
        "What is the difference between a Docker image and a Docker container?",
        "Explain Docker Compose and how it simplifies multi-container deployments.",
        "How do you optimize a Dockerfile for smaller image sizes?",
        "What are Docker volumes and when would you use them?"
    ],
    "aws": [
        "What is Amazon S3 and what are its primary use cases?",
        "Explain the difference between AWS EC2 and AWS Lambda (Serverless).",
        "What is Amazon VPC and how do you secure a database within it?",
        "What is IAM and what is the principle of least privilege?"
    ]
}

def generate_interview_questions(skills, resume_text="", api_key=None):
    """
    Generates interview questions based on skills and resume text.
    Uses Gemini API if key is provided, else falls back to a curated pool.
    """
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
                f"You are a technical interviewer. Generate exactly 5 relevant, challenging "
                f"technical interview questions based on the candidate's skills: {', '.join(skills)} "
                f"and resume content. Return the questions as a numbered list from 1 to 5. "
                f"Resume snippet: {resume_text[:2000]}"
            )
            response = model.generate_content(prompt)
            if response and response.text:
                # Split questions by newline and filter out empty lines or numbers
                lines = response.text.split('\n')
                q_list = []
                for line in lines:
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                        # Strip standard bullet characters and numbers
                        cleaned = line.lstrip('0123456789.-* ')
                        if cleaned:
                            q_list.append(cleaned)
                if len(q_list) >= 3:
                    return q_list[:5]
        except Exception as e:
            print(f"Gemini question generation error: {e}. Falling back to rule-based pool.")

    # Fallback to rule-based questions
    questions = []
    matched_skills = [s.lower() for s in skills if s.lower() in STATIC_QUESTIONS]
    
    if matched_skills:
        for skill in matched_skills:
            questions.extend(STATIC_QUESTIONS[skill])
    else:
        # Default questions if no skills matched
        questions = [
            "Can you describe a technically challenging project you worked on recently and how you resolved the obstacles?",
            "What is your approach to writing clean, maintainable, and well-tested code?",
            "How do you handle collaborating with other developers and stakeholders under tight deadlines?",
            "Describe a time you had to debug a complex system issue. What tools and methods did you use?",
            "What strategies do you use to continuously learn and integrate new programming libraries or patterns?"
        ]

    # Deduplicate and pick 5 randomly
    unique_questions = list(set(questions))
    random.shuffle(unique_questions)
    return unique_questions[:5]
