import re
import spacy
from extract_text import extract_resume_text

nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = [
    "python", "java", "javascript", "html", "css", "sql", "react",
    "node.js", "machine learning", "data analysis", "excel", "communication",
    "leadership", "project management", "c++", "django", "flask",
    "aws", "docker", "git", "tensorflow", "pandas", "numpy"
]

SKILL_CATEGORIES = {
    "Languages": ["python", "java", "javascript", "c++"],
    "Web & Frameworks": ["html", "css", "react", "node.js", "django", "flask"],
    "Database": ["sql"],
    "Tools & Cloud": ["docker", "git", "aws", "tensorflow", "pandas", "numpy"],
    "Soft Skills": ["communication", "leadership", "project management", "excel", "machine learning", "data analysis"]
}

SECTION_HEADERS = [
    "education", "academic background", "qualifications",
    "experience", "work experience", "professional experience",
    "employment history", "internship", "internships",
    "projects", "skills", "technical skills", "certifications",
    "professional summary", "summary", "extracurricular activities"
]

DEGREE_KEYWORDS = [
    "b.tech", "btech", "b.e", "be", "bachelor", "b.sc", "bsc",
    "m.tech", "mtech", "master", "mba", "m.sc", "msc",
    "intermediate", "ssc", "10th", "12th", "diploma", "phd"
]

NOT_ORGS = [
    "css", "html", "javascript", "vscode", "express.js", "git",
    "hyderabad", "telangana", "professional summary", "extracurricular activities",
    "dbms", "php", "api", "education", "linkedin", "actively",
    "computer science", "data structures", "object-oriented programming",
    "core computer science data structures", "cgpa", "crud"
]


def extract_email(text):
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group() if match else None


def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?\d{10}', text)
    return match.group() if match else None


def extract_name(text, doc):
    first_lines = "\n".join(text.split("\n")[:3])
    first_doc = nlp(first_lines)
    for ent in first_doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    for line in text.split("\n"):
        if line.strip():
            return line.strip()
    return None


def extract_skills(text):
    text_lower = text.lower()
    found_skills = [skill for skill in SKILLS_LIST if skill in text_lower]
    return found_skills


def categorize_skills(skills):
    skills_lower = [s.lower() for s in skills]
    breakdown = []
    for category, cat_skills in SKILL_CATEGORIES.items():
        count = sum(1 for s in cat_skills if s in skills_lower)
        if count > 0:
            breakdown.append({"category": category, "count": count})
    return breakdown


def split_into_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        clean_line = line.strip().lower()
        matched_header = None
        for header in SECTION_HEADERS:
            if header in clean_line and len(clean_line) < 50:
                matched_header = header
                break
        if matched_header:
            current_section = matched_header
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_years(text):
    return re.findall(r'\b(?:19|20)\d{2}\b', text)


def extract_education(sections):
    edu_text = ""
    for key in sections:
        if "education" in key or "academic" in key or "qualification" in key:
            edu_text += sections[key] + "\n"

    if not edu_text.strip():
        return []

    results = []
    lines = [l.strip() for l in edu_text.split("\n") if l.strip()]
    for line in lines:
        line_lower = line.lower()
        found_degree = next((d for d in DEGREE_KEYWORDS if d in line_lower), None)
        years = extract_years(line)
        if found_degree or years:
            results.append({
                "raw_line": line,
                "degree_hint": found_degree,
                "year": years[0] if years else None
            })
    return results


def extract_experience(sections):
    exp_text = ""
    for key in sections:
        if "experience" in key or "internship" in key or "employment" in key:
            exp_text += sections[key] + "\n"

    if not exp_text.strip():
        return []

    results = []
    lines = [l.strip() for l in exp_text.split("\n") if l.strip()]
    for line in lines:
        years = extract_years(line)
        if years or len(line) > 20:
            results.append({
                "raw_line": line,
                "year_mentioned": years if years else None
            })
    return results


def extract_organizations(sections, skills):
    org_text = ""
    for key in sections:
        if ("education" in key or "academic" in key or "qualification" in key
                or "experience" in key or "internship" in key or "employment" in key):
            org_text += sections[key] + "\n"

    if not org_text.strip():
        return []

    doc = nlp(org_text)
    skills_lower = [s.lower() for s in skills]
    orgs = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            clean = ent.text.strip()
            clean_lower = clean.lower()
            if "\n" in clean:
                continue
            if clean_lower in NOT_ORGS:
                continue
            if clean_lower in skills_lower:
                continue
            if len(clean) < 3 or len(clean) > 50:
                continue
            orgs.append(clean)
    return list(set(orgs))


def match_resume_to_job(candidate_skills, job_description_text):
    job_text_lower = job_description_text.lower()
    required_skills = [skill for skill in SKILLS_LIST if skill in job_text_lower]

    if not required_skills:
        return {
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0
        }

    candidate_skills_lower = [s.lower() for s in candidate_skills]
    matched = [s for s in required_skills if s in candidate_skills_lower]
    missing = [s for s in required_skills if s not in candidate_skills_lower]

    match_percentage = round((len(matched) / len(required_skills)) * 100)

    return {
        "required_skills": required_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_percentage
    }


def calculate_ats_score(text, sections, result):
    score = 0
    feedback = []

    if result.get("name"):
        score += 5
    else:
        feedback.append({"status": "warning", "message": "Name not clearly detected — keep your name at the very top of the resume"})

    if result.get("email"):
        score += 8
    else:
        feedback.append({"status": "warning", "message": "No email address found — add a professional email near the top"})

    if result.get("phone"):
        score += 7
    else:
        feedback.append({"status": "warning", "message": "No phone number found — add a contact number"})

    has_edu = any("education" in k or "academic" in k or "qualification" in k for k in sections)
    has_exp = any("experience" in k or "internship" in k or "employment" in k for k in sections)
    has_skills = bool(result.get("skills"))

    if has_edu:
        score += 10
    else:
        feedback.append({"status": "warning", "message": "No clear 'Education' section heading found — use a standard heading like 'Education'"})

    if has_exp:
        score += 10
    else:
        feedback.append({"status": "warning", "message": "No clear 'Experience' section found — even internships or projects help ATS parsing"})

    if has_skills:
        score += 10
    else:
        feedback.append({"status": "warning", "message": "No skills detected — add a dedicated 'Skills' section listing your technical skills"})

    word_count = len(text.split())
    if 150 <= word_count <= 800:
        score += 15
    elif word_count < 150:
        score += 5
        feedback.append({"status": "warning", "message": "Resume content seems short — aim for a fuller 1-page resume"})
    else:
        score += 10
        feedback.append({"status": "warning", "message": "Resume is quite long — consider trimming to 1-2 pages for better ATS scanning"})

    bullet_count = text.count("\u2022") + len(re.findall(r'(?m)^\s*[-*]\s', text))
    if bullet_count >= 3:
        score += 15
    else:
        score += 5
        feedback.append({"status": "warning", "message": "Use bullet points (•) to list responsibilities/achievements — ATS systems parse these better than paragraphs"})

    if text:
        clean_chars = sum(1 for c in text if c.isalnum() or c.isspace() or c in ".,|-/@")
        clean_ratio = clean_chars / len(text)
    else:
        clean_ratio = 0

    if clean_ratio > 0.9:
        score += 20
    elif clean_ratio > 0.75:
        score += 12
        feedback.append({"status": "warning", "message": "Resume formatting has some unusual characters that may confuse ATS parsers"})
    else:
        score += 5
        feedback.append({"status": "warning", "message": "Resume contains complex formatting (tables, icons, columns) that ATS systems often fail to read correctly"})

    score = min(score, 100)

    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Needs Improvement"
    else:
        rating = "Poor"

    if not feedback:
        feedback.append({"status": "good", "message": "Your resume is well-structured and ATS-friendly!"})

    return {
        "score": score,
        "rating": rating,
        "feedback": feedback
    }


def parse_resume_free(file_path):
    text = extract_resume_text(file_path)
    doc = nlp(text)
    sections = split_into_sections(text)
    skills = extract_skills(text)

    result = {
        "name": extract_name(text, doc),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "skills_breakdown": categorize_skills(skills),
        "education": extract_education(sections),
        "experience": extract_experience(sections),
        "organizations_mentioned": extract_organizations(sections, skills),
    }

    result["ats_score"] = calculate_ats_score(text, sections, result)

    return result


if __name__ == "__main__":
    file_path = "PADMA_PRIYA_PEDDINTI.pdf"
    data = parse_resume_free(file_path)

    import json
    print(json.dumps(data, indent=2))

    with open("parsed_resume.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("\nSaved to parsed_resume.json")