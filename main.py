from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Optional, List
import shutil
import os
from parse_resume_free import parse_resume_free, match_resume_to_job
from database import create_tables, save_resume, get_all_resumes, delete_resume

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# DB tables create చేయండి startup లో
create_tables()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), job_description: Optional[str] = Form(None)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    data = parse_resume_free(file_path)
    data["filename"] = file.filename
    if job_description and job_description.strip():
        match_result = match_resume_to_job(data.get("skills", []), job_description)
        data["job_match"] = match_result

    # ✅ Database లో save చేయండి
    save_resume(data)
    return data

@app.post("/upload-multiple-resumes")
async def upload_multiple_resumes(files: List[UploadFile] = File(...), job_description: Optional[str] = Form(None)):
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        data = parse_resume_free(file_path)
        data["filename"] = file.filename
        if job_description and job_description.strip():
            match_result = match_resume_to_job(data.get("skills", []), job_description)
            data["job_match"] = match_result
            data["match_percentage"] = match_result["match_percentage"]
        else:
            data["match_percentage"] = None

        # ✅ Database లో save చేయండి
        save_resume(data)
        results.append(data)

    results.sort(key=lambda x: (x["match_percentage"] is None, -(x["match_percentage"] or 0)))
    return {"candidates": results}

# ✅ History endpoint
@app.get("/history")
def get_history():
    return {"resumes": get_all_resumes()}

# ✅ Delete endpoint
@app.delete("/history/{resume_id}")
def delete_history(resume_id: int):
    success = delete_resume(resume_id)
    return {"success": success}