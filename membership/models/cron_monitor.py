from sqlalchemy import ForeignKey
from core.db import db

class CronMonitor(db.Model):
  __tablename__ = "CronMonitor"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
  last_active_at = db.Column(db.DateTime, nullable=False)
  last_notified_at = db.Column(db.DateTime, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False)
  last_modified_at = db.Column(db.DateTime, nullable=False)
  