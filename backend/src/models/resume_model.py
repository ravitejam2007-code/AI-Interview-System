# Resume model placeholder

class Resume:
    def __init__(self, resume_id, user_id, resume_path, ats_score):
        self.id = resume_id
        self.user_id = user_id
        self.resume_path = resume_path
        self.ats_score = ats_score
        
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "resume_path": self.resume_path,
            "ats_score": self.ats_score
        }
