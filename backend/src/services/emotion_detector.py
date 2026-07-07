def analyze_face_emotions(frame_bytes=None):
    """
    Placeholder for Emotion Detection service using TensorFlow/DeepFace.
    Returns simulated/mock emotion confidence scores for mock interview telemetry.
    """
    import random
    
    emotions = {
        "confidence": random.randint(70, 95),
        "happiness": random.randint(5, 20),
        "nervousness": random.randint(10, 30),
        "stress": random.randint(5, 15)
    }
    
    return emotions
