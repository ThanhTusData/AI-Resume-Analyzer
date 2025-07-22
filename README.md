# 📄 AI Resume Analyzer

This project is an **AI-powered resume analysis tool** that can scrape LinkedIn profiles, analyze resumes, and provide insights using machine learning and NLP techniques.

---

## 📁 Project Structure

```
AI Resume Analyzer/
│
├── app.py                         # Main entry point for running the web application
├── .gitignore                    # Git ignore rules
├── selenium_profile/            # Chrome Selenium profile storage
│
├── functions/                   # Python modules for core functionalities
│   ├── linkedin_scraper.py         # Script to scrape LinkedIn profiles using Selenium
│   └── resume_analyzer.py          # Script to analyze resumes using NLP/ML
│
├── notebooks/                   # Jupyter Notebooks for development and testing
│   ├── AI_Powered_Resume_Analyzer.ipynb
│   └── LinkedIn_scraper_with_Selenium.ipynb
```

---

## 🔁 Project Workflow

1. **Data Collection**:  
   - Use `linkedin_scraper.py` or `LinkedIn_scraper_with_Selenium.ipynb` to collect public profile data from LinkedIn.
   - Data can also be sourced from user-uploaded resumes.

2. **Resume Analysis**:  
   - The `resume_analyzer.py` module processes resumes and LinkedIn data.
   - It extracts relevant skills, experience, education, and matches against job descriptions (if provided).

3. **Web App (Optional)**:  
   - The `app.py` file serves as the main app interface (can be Streamlit or Flask).
   - Users can upload resumes or input LinkedIn URLs to get analysis reports in real-time.

---

## ▶️ How to Run the Project

### 1. Install Dependencies

Make sure you have Python 3.8+ and install the required libraries:

```bash
pip install -r requirements.txt
```

Or manually install essential packages (if `requirements.txt` is missing):

```bash
pip install selenium beautifulsoup4 pandas numpy scikit-learn nltk
```

### 2. Setup Selenium (For LinkedIn Scraping)

- Make sure you have **ChromeDriver** installed and its path correctly set.
- Use a profile stored in `selenium_profile` if login is required.

### 3. Run the Web App

```bash
python app.py
```

The app will be accessible at `http://localhost:8501` (if Streamlit is used).

---

## 💡 Features

- LinkedIn Profile Scraping (via Selenium)
- Resume Parsing & Feature Extraction
- Skill Matching & Scoring
- Jupyter Notebooks for development and testing
- Scalable structure for ML model integration

---

## 📌 Notes

- Do **not misuse** LinkedIn scraping features; follow ethical and legal guidelines.
- Ensure your ChromeDriver and browser versions are compatible.
- You may need to train or load a model inside `resume_analyzer.py` depending on implementation.

---

## 📬 Contact

For improvements, feedback, or collaborations, feel free to open an issue or pull request.
