# RecruitAI — Backend API Service

FastAPI-powered backend for the AI Resume & Job Description Matching System.

## Features
- **FastAPI** with async endpoints and automatic Swagger documentation
- **Sentence-BERT (`all-MiniLM-L6-v2`)** for semantic text embeddings
- **TF-IDF + Cosine Similarity** for lexical keyword matching
- **500+ Skills Database & spaCy NLP** for structured entity extraction
- **PostgreSQL Database** with SQLAlchemy ORM
- **JWT Authentication** with password hashing
- **Candidate Email Dispatch** (Gmail SMTP & SendGrid)
- **Executive PDF & CSV Reports** with ReportLab

## Quick Start

### 1. Setup Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate    # Linux / macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your database credentials and optional email settings:
```bash
cp .env.example .env
```

### 4. Create Tables & Verify DB
```bash
python create_tables.py
python test_db.py
```

### 5. Run Server
```bash
python run.py
```
API Documentation: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### 6. Run Accuracy Benchmark & NLP Pipeline Tests
```bash
# Test custom Edit Distance & all 5 literature review modules
python tests/test_nlp_pipeline.py

# Run 20-case end-to-end benchmark suite
python test_accuracy.py
```
Results will be displayed and saved in `results/accuracy_report.json`.
