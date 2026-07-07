import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = (formData) => {
  return api.post('/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const generateQuestions = (skills, resumeText) => {
  return api.post('/interview/generate-questions', {
    skills,
    resume_text: resumeText,
  });
};

export const detectEmotion = () => {
  return api.post('/interview/emotion');
};

export const evaluateAnswer = (question, answer, resumeText, token) => {
  return api.post('/interview/evaluate-answer', {
    question,
    answer,
    resume_text: resumeText,
  }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const fetchResults = () => {
  return api.get('/ats/results');
};

export default api;
