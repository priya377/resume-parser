from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ParsedResume(Base):
    __tablename__ = "parsed_resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    skills = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    organizations = Column(Text)
    parsed_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

def save_resume(data: dict):
    db = SessionLocal()
    try:
        resume = ParsedResume(
            filename=data.get("filename", "unknown"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            skills=json.dumps(data.get("skills", [])),
            education=json.dumps(data.get("education", [])),
            experience=json.dumps(data.get("experience", [])),
            organizations=json.dumps(data.get("organizations_mentioned", []))
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume.id
    finally:
        db.close()

def get_all_resumes():
    db = SessionLocal()
    try:
        resumes = db.query(ParsedResume).order_by(ParsedResume.parsed_at.desc()).all()
        result = []
        for r in resumes:
            result.append({
                "id": r.id,
                "filename": r.filename,
                "name": r.name,
                "email": r.email,
                "phone": r.phone,
                "skills": json.loads(r.skills or "[]"),
                "education": json.loads(r.education or "[]"),
                "experience": json.loads(r.experience or "[]"),
                "organizations_mentioned": json.loads(r.organizations or "[]"),
                "parsed_at": r.parsed_at.strftime("%d %b %Y, %I:%M %p")
            })
        return result
    finally:
        db.close()

def delete_resume(resume_id: int):
    db = SessionLocal()
    try:
        resume = db.query(ParsedResume).filter(ParsedResume.id == resume_id).first()
        if resume:
            db.delete(resume)
            db.commit()
            return True
        return False
    finally:
        db.close()