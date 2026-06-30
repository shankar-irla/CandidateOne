# 🎬 CandidateOne - Demo Guide

## End-to-End Multi-Source Candidate Canonicalization Engine

---

# 📌 Overview

This guide demonstrates how to execute the CandidateOne pipeline and verify the generated canonical candidate profile.

The application consolidates candidate information from multiple data sources into a single, validated, confidence-scored canonical representation.

---

# 📋 Prerequisites

Ensure the following are installed:

- Python 3.10+
- pip
- Git

---

# 🚀 Running the Project

Clone the repository

```bash
git clone https://github.com/shankar-irla/CandidateOne.git
```

Navigate to the project

```bash
cd CandidateOne
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 📁 Sample Input Files

Upload the following files from the `sample_input/` directory.

| Source | Format |
|---------|--------|
| Resume | PDF |
| ATS Export | JSON |
| LinkedIn Profile | JSON |
| GitHub Profile | JSON |
| Recruiter Export | CSV |

---

# ▶ Demo Workflow

## Step 1

Launch the Flask application.

---

## Step 2

Open

```
http://127.0.0.1:5000
```

---

## Step 3

Upload one or more supported candidate sources.

Supported sources include:

- Resume (PDF)
- ATS Export (JSON)
- LinkedIn Profile (JSON)
- GitHub Profile (JSON)
- Recruiter CSV

---

## Step 4

Click

```
Run CandidateOne Pipeline
```

---

## Step 5

The application performs the following stages:

```text
Input Sources
      │
      ▼
Extraction
      │
      ▼
Normalization
      │
      ▼
Merge Engine
      │
      ▼
Confidence Calculation
      │
      ▼
Projection Layer
      │
      ▼
Schema Validation
      │
      ▼
Canonical Candidate Profile
```

---

## Step 6

Review the generated results.

CandidateOne displays:

- Canonical Candidate Profile
- Projected Candidate Profile
- Overall Confidence Score
- Provenance Information
- Pipeline Statistics

---

## Step 7

Download the generated JSON output files if required.

---

# 📤 Expected Output

After successful execution, CandidateOne generates:

- Unified Canonical Candidate Profile
- Configurable Projected Output
- Confidence Score
- Provenance Metadata

Generated files are stored in the `output/` directory.

---

# 📂 Project Structure

```text
CandidateOne/

├── app.py
├── pipeline.py
├── config/
├── docs/
├── extractors/
├── merger/
├── models/
├── normalizer/
├── projection/
├── validator/
├── utils/
├── templates/
├── static/
├── tests/
├── sample_input/
├── output/
└── README.md
```

---

# 🎥 Demo Video

A complete walkthrough of the application is available in the project repository.

```
docs/CandidateOne.mp4
```

---

# 🧪 Verification Checklist

Use the following checklist to verify the implementation:

- ✅ Resume successfully parsed
- ✅ ATS JSON successfully parsed
- ✅ LinkedIn profile parsed
- ✅ GitHub profile parsed
- ✅ Recruiter CSV parsed
- ✅ Candidate information normalized
- ✅ Profiles merged correctly
- ✅ Conflicts resolved
- ✅ Provenance generated
- ✅ Confidence score calculated
- ✅ Output validated against schema
- ✅ Canonical JSON generated
- ✅ Projected JSON generated

---

# 📄 Notes

CandidateOne follows a deterministic ETL architecture.

All candidate information is transformed into a common canonical schema before normalization, merging, projection, and validation. This design enables consistent processing while making the pipeline modular, extensible, and easy to maintain.

---

## 👨‍💻 Developed By

**I G Siva Shankar**

B.Tech – Computer Science & Engineering (Data Science)

CMR Engineering College, Hyderabad

---

**CandidateOne – End-to-End Multi-Source Candidate Canonicalization Engine**