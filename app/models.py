from app import db
from datetime import datetime
class ExposedInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    local_url = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    last_heartbeat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    home_data = db.Column(db.JSON, nullable=True)
    files_data = db.Column(db.JSON, nullable=True)
    behaviors_data = db.Column(db.JSON, nullable=True)
    allowed_users = db.Column(db.JSON, nullable=True)  # Added field for allowed_users
    last_data_sync = db.Column(db.DateTime, nullable=True)
    pending_uploads = db.Column(db.JSON, default=list)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'local_url': self.local_url,
            'token': self.token,
            'last_heartbeat': self.last_heartbeat.isoformat()
        }
    
    def is_online(self):
        return (datetime.utcnow() - self.last_heartbeat).total_seconds() <= 300
