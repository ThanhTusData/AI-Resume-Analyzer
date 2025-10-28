# scripts/generate_fake_processed.py
import json
from pathlib import Path
import uuid
import random

OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

N = 10

sample_skills = [
    "Python", "Machine Learning", "SQL", "Data Analysis", "Pandas", "Docker",
    "AWS", "Deep Learning", "NLP", "Computer Vision", "Git", "Linux"
]
sample_titles = ["Data Analyst", "Machine Learning Engineer", "Software Engineer", "Research Intern"]
sample_companies = ["Acme Corp", "Globex", "FPT Software", "ACB Bank", "StartupX"]

for i in range(N):
    rid = str(uuid.uuid4())
    skills = random.sample(sample_skills, k=random.randint(3,6))
    experiences = []
    for j in range(random.randint(1,3)):
        experiences.append({
            "title": random.choice(sample_titles),
            "company": random.choice(sample_companies),
            "description": f"Worked on project {j+1} using {', '.join(random.sample(skills, k=min(2,len(skills))))}. Delivered features and improved metrics."
        })
    rec = {
        "id": rid,
        "name": f"Candidate {i+1}",
        "raw_text": f"Resume of candidate {i+1}. Skills: {', '.join(skills)}. Experience: " + " ".join([e["description"] for e in experiences]),
        "summary": f"Experienced {random.choice(sample_titles)} with skills in {', '.join(skills)}.",
        "skills": skills,
        "emails": [f"user{i+1}@example.com"],
        "phones": [f"+84{random.randint(900000000, 999999999)}"],
        "experiences": experiences
    }
    out = OUT / f"{rid}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
print(f"Generated {N} fake processed resumes in {OUT}")
