"""
Evaluates Anuj Partani's resume against target roles using the newly implemented pipeline.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.utils.matcher import match_resume_to_jd

RESUME_TEXT = """
Anuj Partani
+91-9825190621 | partanianuj98251@gmail.com | LinkedIn | GitHub | LeetCode | CodeChef

EDUCATION
Indian Institute of Information Technology, Nagpur Aug 2024 – Aug 2028
Bachelor of Technology - Computer Science and Engineering CGPA 8.85/10

EXPERIENCE
Undergraduate Researcher | AI-Assisted Vaccine Design Platform Apr 2026 – Present
Prof. Dr. Jitendra Tembhurne Nagpur,India
• Engineered an end-to-end vaccine design pipeline that converts a raw protein sequence into a fully validated multi-epitope construct + mRNA sequence in a single click, reducing prototyping time by 70%.
• Implemented automatic adjuvant selection across three TLR-targeting candidates using a weighted composite score, delivering a chimeric vaccine that achieves ≥ 97% global HLA population coverage.
• Achieved 91% accuracy, 0.89 F1-score, and 0.94 AUROC and strong docking energies (≤ -200 kcal/mol) while providing SHAP - based explainability
Project Lead - TigerTrace | Pench Tiger Reserve Aug 2026 – Sep 2026
• Delivered a prototype dashboard that secured approval from the Director of PenchTigerReserve; refined it for the Reserve's ongoing wildlife-management operations

PROJECTS
H2-OptiPlant | React, Leaflet, Node.js, Flask, TensorFlow, Supabase Nov 2025
• Architected an AI green hydrogen platform with 9 ML microservices and renewable surplus routing, cutting projected LCOH from $4.50/kg to $2.00/kg
• Formulated a 4-state hot-standby protocol (RHS-RRP) with active polarization, slashing electrolyzer restart time from 45 to <3 min while syncing telemetry to a Three.js 3D digital twin.
TigerTrace | Next.js, FastAPI, PyTorch, ONNX Runtime, SQLite, Leaflet Oct 2026
• Designed a offline CV pipeline using MegaDetector V6 (95% recall) for filtering blank frames, MobileNetV3 (98.7% F1) for species identification and ResNet-18 + BNNeck (99.17% Accuracy) for Stripe Re-ID matching across 62 tiger identities of Pench Tiger Reserve
• Developed a geospatial alert patrol engine mapping MCP home ranges, detecting territorial overlaps, and scoring 0 to 100 patrol priorities across various stations with real-time range shift and village proximity alerts
ComplyGem | React, Express, FastAPI, MongoDB, LangGraph, Tesseract OCR Sep 2026
• Orchestrated a 5-agent LangGraph compliance pipeline with Tesseract OCR across 11 statutory documents and cross-verification against 4 government registries (GSTN, PAN, Udyam, GeM Blacklist).
• Devised a 0-100 weighted risk scoring engine across 6 compliance factors with a Critic agent preventing LLM hallucinations and a Groq 4-key rotation pool handling rate limits.
• Built a synthetic document studio generating 11 statutory PDFs per bidder with planted defects and ground-truth test oracles, benchmarking the AI pipeline across 5 deterministic personas.

TECHNICAL SKILLS
Languages: C, C++, Python, Java, Javascript, SQL
Web & DB: React.js, Node.js, Express.js, FastAPI, Mysql, PostgreSQL
Core Areas: Machine learning, Deep learning, NLP, GenAI, Rag, Agents, Multimodal AI
AI / ML: TensorFlow, PyTorch, Numpy, Pandas, Scikit-learn
Developer Tools: Git, GitHub, Vercel, Docker, AWS
Core CS: Data Structures Algorithms, OOP, Operating Systems, DBMS, Computer Networks

ACHIEVEMENTS
• Competitive Programming: CodeChef 2-Star (Peak Rating: 1480); Solved 450+ Data Structures and Algorithms (DSA) problems.
• Hackathons: SIH'25 National Winner (Smart India Hackathon); Achieved 2nd Place at Viksit4Nagpur Hackathon (VNIT Nagpur) among 100+ teams.
"""

RESUME_SKILLS = [
    "Python", "C++", "Java", "Javascript", "SQL", "React", "Node.js", "Express.js",
    "FastAPI", "PostgreSQL", "MySQL", "MongoDB", "SQLite", "TensorFlow", "PyTorch",
    "scikit-learn", "Pandas", "NumPy", "Docker", "AWS", "Git", "Machine learning",
    "Deep learning", "NLP", "GenAI", "RAG", "LangGraph", "Computer Vision", "ONNX"
]

TARGET_JDS = [
    {
        "role": "AI / ML Engineer",
        "jd_text": """
        We are hiring an AI / Machine Learning Engineer to design and deploy scalable deep learning models.
        Requirements:
        - Strong proficiency in Python, PyTorch, TensorFlow, and scikit-learn.
        - Experience in Natural Language Processing (NLP), Deep Learning, or Computer Vision.
        - Hands-on experience building ML pipelines, REST APIs using FastAPI or Flask, and containerization with Docker.
        - Familiarity with cloud platforms (AWS), Git, and data manipulation with Pandas and NumPy.
        - Bonus: Experience with GenAI, RAG, agentic frameworks (LangGraph/LangChain), and model deployment.
        """,
        "jd_skills": ["Python", "PyTorch", "TensorFlow", "scikit-learn", "NLP", "Deep learning", "FastAPI", "Docker", "AWS", "Git", "Pandas", "Machine learning", "GenAI"]
    },
    {
        "role": "Python Backend & AI Developer",
        "jd_text": """
        Looking for a Python Backend Developer with strong AI integration skills.
        Must have:
        - Expertise in Python, FastAPI, PostgreSQL, and RESTful API architecture.
        - Experience with Docker, Git, and deploying backend microservices on AWS.
        - Knowledge of integrating ML/AI models, LangChain/LangGraph, or RAG pipelines.
        - Strong computer science fundamentals, DBMS, and data structures.
        """,
        "jd_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git", "AWS", "REST", "DBMS", "Data Structures", "LangGraph"]
    },
    {
        "role": "Full Stack AI Engineer",
        "jd_text": """
        Full Stack Engineer needed to build AI-driven web applications.
        Must have:
        - Frontend: React.js, JavaScript, modern responsive UI.
        - Backend: Node.js, Express, Python, FastAPI.
        - Databases: PostgreSQL, MongoDB.
        - Experience deploying LLM agents, vector search, or computer vision workflows.
        """,
        "jd_skills": ["React", "JavaScript", "Node.js", "FastAPI", "Python", "PostgreSQL", "MongoDB", "Express", "Docker"]
    }
]

import json

for item in TARGET_JDS:
    res = match_resume_to_jd(
        resume_text=RESUME_TEXT,
        jd_text=item["jd_text"],
        resume_skills=RESUME_SKILLS,
        jd_required_skills=item["jd_skills"]
    )
    print("="*70)
    print(f"ROLE: {item['role']}")
    print(f"MATCH SCORE: {res['match_score']}%  |  VERDICT: {res['verdict']}")
    print(f"BERT Semantic Score: {res.get('bert_score', 0):.4f}")
    print(f"TF-IDF Cosine: {res.get('cosine_similarity', 0):.4f}")
    print(f"BM25F Section Fit: {res.get('bm25f_score', 0)}%")
    print(f"Fuzzy Set Similarity: {res.get('fuzzy_similarity_score', 0)}% (Coverage: {res.get('fuzzy_coverage', 0)})")
    print(f"Skill Match Pct: {res.get('skill_match_percentage', 0)}%")
    print(f"Matched Skills ({len(res['matched_skills'])}): {res['matched_skills']}")
    print(f"Missing Skills ({len(res['missing_skills'])}): {res['missing_skills']}")
    if res.get("edit_distance_matches"):
        print(f"Edit Distance Matches: {res['edit_distance_matches']}")
    summary = res.get('textrank_summary', '').encode('ascii', 'ignore').decode('ascii')
    recom = res.get('recommendations', '').encode('ascii', 'ignore').decode('ascii')
    print(f"TextRank Summary: {summary}")
    print(f"Recommendations: {recom}")
    print("="*70)
