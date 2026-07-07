import sys
import os

# Include backend directory in python path to allow importing src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from src.services.resume_parser import extract_skills
from src.services.ats_checker import check_ats
from src.services.answer_validator import is_valid_answer, is_gibberish
from src.services.answer_evaluator import keyword_score

def test_extract_skills():
    """
    Test skill extraction logic.
    """
    text = "Experienced software engineer with Python, React, and SQL skills."
    skills = extract_skills(text)
    assert "python" in skills
    assert "react" in skills
    assert "sql" in skills
    assert "java" not in skills

def test_ats_checker():
    """
    Test ATS scoring computation.
    """
    text = "Skillset: Python, Machine Learning, Flask, SQL, React, Javascript."
    results = check_ats(text)
    assert results['ats_score'] >= 80
    assert "python" in results['matched_skills']
    assert len(results['missing_skills']) == 0


def test_is_valid_answer():
    assert is_valid_answer("React state stores data") is True
    assert is_valid_answer("hi") is False
    assert is_valid_answer("a") is False
    assert is_valid_answer("") is False
    assert is_valid_answer("   ") is False
    assert is_valid_answer("Python list mutable") is True


def test_is_gibberish():
    assert is_gibberish("hgfyusa") is True
    assert is_gibberish("asdfghjkl") is True
    assert is_gibberish("qwerty") is True
    assert is_gibberish("React state stores data") is False
    assert is_gibberish("Python is great") is False
    assert is_gibberish("") is False


def test_keyword_score():
    q = "What is the difference between state and props in React?"
    score = keyword_score(q, "Props are passed from parent to child. State is mutable.")
    assert score >= 50
    assert score <= 100

    score = keyword_score(q, "Completely unrelated text here")
    assert score < 30

    score = keyword_score(q, "")
    assert score == 0

    no_match = keyword_score("Unknown question not in expected answers", "some answer")
    assert no_match is None
