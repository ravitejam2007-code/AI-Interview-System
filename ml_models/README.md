# Pre-trained ML & Deep Learning Models

This directory is reserved for storing binary model files used for resume classification and emotion detection.

## Recommended Models

1. **`emotion_model.h5`**: TensorFlow Keras H5 model for facial expression and emotion classification.
2. **`resume_classifier.pkl`**: Scikit-Learn pipeline (TF-IDF + Random Forest / SVM) to classify resumes into job sectors.
3. **`question_model.pkl`**: Model/tokenizers used to map keywords to semantic questions.

## Storage Recommendation
Due to the large size of binary weights, do not push large model files directly to GitHub. Instead, use:
- **Git LFS (Large File Storage)**, or
- Store on cloud storage (AWS S3, Google Cloud Storage) and pull during deployment using a setup script.
