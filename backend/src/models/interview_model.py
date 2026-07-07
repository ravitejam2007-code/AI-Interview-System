from src.database.db import db
from datetime import datetime

class InterviewResult(db.Model):
    __tablename__ = 'interview_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ats_score = db.Column(db.Float, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)
    technical_accuracy = db.Column(db.Float, nullable=True)
    feedback_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with User
    user = db.relationship('User', backref=db.backref('interviews', lazy=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ats_score": self.ats_score,
            "confidence_score": self.confidence_score,
            "technical_accuracy": self.technical_accuracy,
            "feedback_text": self.feedback_text,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
