"""
test_accuracy.py
────────────────────────────────────────────────────────────────
Run this ONCE to generate your accuracy proof.

Usage:
    cd backend
    python test_accuracy.py

Output:
    - Prints accuracy table to terminal
    - Saves results/accuracy_report.json
    - Saves results/confusion_matrix.txt

This gives you REAL numbers to quote in your report and viva:
  "Tested on 20 resume-JD pairs. System achieved 90% verdict accuracy."
"""

import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.matcher import match_resume_to_jd

os.makedirs("results", exist_ok=True)

# ── 20 Test Cases (resume_text, jd_text, resume_skills, jd_skills, expected_verdict) ──

TEST_CASES = [
    # ── Strong matches (expected: Highly Recommended) ────────────────────────
    {
        "id": 1,
        "label": "Python Dev vs Python JD",
        "resume": """
            Experienced Python developer with 3 years building REST APIs using FastAPI and Django.
            Strong skills in PostgreSQL, Redis, Docker, AWS, Git, SQLAlchemy, and Pydantic.
            Developed machine learning pipelines using scikit-learn and pandas.
            Experience with React frontend and Tailwind CSS.
        """,
        "jd": """
            We are looking for a Python Backend Developer with experience in FastAPI or Django.
            Must have: Python, PostgreSQL, REST API development, Git, Docker.
            Bonus: AWS, React, Machine Learning experience.
        """,
        "resume_skills": ["Python", "FastAPI", "Django", "PostgreSQL", "Docker", "AWS", "Git", "React", "scikit-learn"],
        "jd_skills": ["Python", "PostgreSQL", "FastAPI", "Git", "Docker"],
        "expected": "Highly Recommended",
    },
    {
        "id": 2,
        "label": "Data Scientist vs Data Science JD",
        "resume": """
            Data Scientist with expertise in machine learning, deep learning, and NLP.
            Proficient in Python, TensorFlow, PyTorch, scikit-learn, pandas, numpy.
            Built recommendation systems and NLP pipelines for e-commerce.
            Strong knowledge of SQL, MongoDB, and data visualization with matplotlib.
        """,
        "jd": """
            Data Scientist required. Must know Python, scikit-learn, TensorFlow, pandas, numpy.
            Experience with NLP, recommendation systems, and SQL required.
            Strong problem solving and data visualization skills.
        """,
        "resume_skills": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "pandas", "numpy", "SQL", "NLP", "MongoDB"],
        "jd_skills": ["Python", "scikit-learn", "TensorFlow", "pandas", "numpy", "SQL", "NLP"],
        "expected": "Highly Recommended",
    },
    {
        "id": 3,
        "label": "Full Stack Dev vs Full Stack JD",
        "resume": """
            Full Stack Developer experienced in React, Node.js, Express, MongoDB.
            Built 5+ production web apps. Strong in JavaScript, TypeScript, REST APIs.
            DevOps: Docker, CI/CD, AWS EC2, GitHub Actions.
        """,
        "jd": """
            Full Stack Developer needed. React, Node.js, MongoDB, JavaScript required.
            REST API experience essential. AWS and Docker knowledge preferred.
        """,
        "resume_skills": ["React", "Node.js", "Express", "MongoDB", "JavaScript", "TypeScript", "Docker", "AWS"],
        "jd_skills": ["React", "Node.js", "MongoDB", "JavaScript", "AWS", "Docker"],
        "expected": "Highly Recommended",
    },
    {
        "id": 4,
        "label": "DevOps Engineer vs DevOps JD",
        "resume": """
            DevOps Engineer with 4 years experience. Expert in Docker, Kubernetes, Terraform, Jenkins.
            AWS certified. Managed CI/CD pipelines for 10+ microservices. Linux, Bash scripting.
        """,
        "jd": """
            DevOps Engineer with Docker, Kubernetes, AWS, Jenkins, Terraform expertise.
            CI/CD pipeline experience essential. Linux and scripting skills required.
        """,
        "resume_skills": ["Docker", "Kubernetes", "Terraform", "Jenkins", "AWS", "Linux", "Bash"],
        "jd_skills": ["Docker", "Kubernetes", "AWS", "Jenkins", "Terraform", "Linux"],
        "expected": "Highly Recommended",
    },
    {
        "id": 5,
        "label": "ML Engineer vs ML JD",
        "resume": """
            ML Engineer specializing in computer vision and NLP. Experience with BERT, transformers,
            PyTorch, TensorFlow. Deployed models on AWS SageMaker. Python expert.
        """,
        "jd": """
            ML Engineer needed. Must have PyTorch, TensorFlow, Python, and model deployment experience.
            NLP or computer vision background preferred. AWS or GCP cloud experience.
        """,
        "resume_skills": ["PyTorch", "TensorFlow", "Python", "BERT", "NLP", "AWS", "SageMaker"],
        "jd_skills": ["PyTorch", "TensorFlow", "Python", "NLP", "AWS"],
        "expected": "Highly Recommended",
    },

    # ── Good matches (expected: Recommended) ─────────────────────────────────
    {
        "id": 6,
        "label": "Java Dev vs Python JD (partial)",
        "resume": """
            Java developer with 2 years experience in Spring Boot, Hibernate, MySQL.
            Basic Python knowledge. REST API development, Git, Maven, Linux.
        """,
        "jd": """
            Python Developer needed. FastAPI, PostgreSQL, REST APIs, Git required.
            Machine learning experience preferred.
        """,
        "resume_skills": ["Java", "Spring Boot", "MySQL", "Python", "REST API", "Git", "Linux"],
        "jd_skills": ["Python", "FastAPI", "PostgreSQL", "REST API", "Git"],
        "expected": "Recommended",
    },
    {
        "id": 7,
        "label": "Frontend Dev vs Full Stack JD",
        "resume": """
            Frontend developer skilled in React, Vue.js, JavaScript, CSS, HTML, Tailwind.
            Basic Node.js and Express knowledge. REST API consumption experience.
        """,
        "jd": """
            Full Stack Developer with React, Node.js, MongoDB, REST API experience needed.
            TypeScript knowledge preferred.
        """,
        "resume_skills": ["React", "Vue.js", "JavaScript", "CSS", "HTML", "Node.js", "Express"],
        "jd_skills": ["React", "Node.js", "MongoDB", "REST API", "TypeScript"],
        "expected": "Recommended",
    },
    {
        "id": 8,
        "label": "Data Analyst vs Data Scientist JD",
        "resume": """
            Data Analyst with strong SQL, Excel, Power BI, and Python (pandas, matplotlib) skills.
            Experience with statistical analysis and data cleaning. Tableau dashboards.
        """,
        "jd": """
            Data Scientist needed. Python, machine learning, scikit-learn, pandas, SQL required.
            Statistical background and data visualization skills preferred.
        """,
        "resume_skills": ["SQL", "Python", "pandas", "Excel", "Power BI", "Tableau", "Statistics"],
        "jd_skills": ["Python", "scikit-learn", "pandas", "SQL", "Statistics"],
        "expected": "Recommended",
    },

    # ── Borderline matches (expected: Consider) ───────────────────────────────
    {
        "id": 9,
        "label": "Manual QA vs Automation JD",
        "resume": """
            QA Engineer with 2 years experience in manual testing, test cases, bug reporting.
            Basic Selenium knowledge. JIRA, TestRail. Some Python scripting.
        """,
        "jd": """
            Automation Test Engineer needed. Selenium, Python, pytest, Jenkins CI/CD required.
            REST API testing with Postman. Strong programming background.
        """,
        "resume_skills": ["Manual Testing", "Selenium", "Python", "JIRA", "TestRail"],
        "jd_skills": ["Selenium", "Python", "pytest", "Jenkins", "Postman", "REST API"],
        "expected": "Consider",
    },
    {
        "id": 10,
        "label": "PHP Dev vs Python JD",
        "resume": """
            PHP developer with Laravel, MySQL, JavaScript, HTML, CSS. 
            Built e-commerce websites. Basic Python knowledge. REST API experience.
        """,
        "jd": """
            Python Backend Developer. FastAPI, PostgreSQL, Redis, Docker, REST API required.
            Machine learning experience is a plus.
        """,
        "resume_skills": ["PHP", "Laravel", "MySQL", "JavaScript", "Python", "REST API"],
        "jd_skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "REST API"],
        "expected": "Consider",
    },

    # ── Poor matches (expected: Not Recommended) ──────────────────────────────
    {
        "id": 11,
        "label": "Marketing MBA vs Python Dev JD",
        "resume": """
            MBA in Marketing with 3 years experience in digital marketing, SEO, Google Ads.
            Social media management, content writing, email campaigns, brand strategy.
        """,
        "jd": """
            Python Developer needed. FastAPI, PostgreSQL, Docker, machine learning required.
            Strong programming and computer science background essential.
        """,
        "resume_skills": ["Marketing", "SEO", "Google Ads", "Content Writing"],
        "jd_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Machine Learning"],
        "expected": "Not Recommended",
    },
    {
        "id": 12,
        "label": "Graphic Designer vs Data Scientist JD",
        "resume": """
            Graphic designer with expertise in Adobe Photoshop, Illustrator, Figma, InDesign.
            UI/UX design, logo design, brand identity. Some HTML and CSS knowledge.
        """,
        "jd": """
            Data Scientist with Python, machine learning, NLP, deep learning, SQL required.
            Strong statistical background and research experience.
        """,
        "resume_skills": ["Photoshop", "Illustrator", "Figma", "HTML", "CSS"],
        "jd_skills": ["Python", "Machine Learning", "NLP", "SQL", "Statistics", "Deep Learning"],
        "expected": "Not Recommended",
    },
    {
        "id": 13,
        "label": "HR Manager vs DevOps JD",
        "resume": """
            HR Manager with experience in talent acquisition, payroll, employee relations.
            HRIS systems, performance management, compliance, onboarding.
        """,
        "jd": """
            DevOps Engineer with Docker, Kubernetes, AWS, Jenkins, Linux, Terraform required.
            CI/CD pipeline management and scripting skills essential.
        """,
        "resume_skills": ["HR Management", "Talent Acquisition", "Payroll", "HRIS"],
        "jd_skills": ["Docker", "Kubernetes", "AWS", "Jenkins", "Linux", "Terraform"],
        "expected": "Not Recommended",
    },
    {
        "id": 14,
        "label": "Accountant vs ML Engineer JD",
        "resume": """
            Chartered Accountant with expertise in financial reporting, taxation, audit.
            Tally ERP, SAP Finance, Excel. Strong analytical and compliance skills.
        """,
        "jd": """
            ML Engineer. Python, PyTorch, TensorFlow, model training, AWS SageMaker.
            Computer vision or NLP experience required.
        """,
        "resume_skills": ["Accounting", "Tally", "SAP", "Excel", "Finance", "Audit"],
        "jd_skills": ["Python", "PyTorch", "TensorFlow", "AWS", "NLP", "Computer Vision"],
        "expected": "Not Recommended",
    },
    {
        "id": 15,
        "label": "Civil Engineer vs Java Dev JD",
        "resume": """
            Civil Engineer with experience in AutoCAD, structural design, project management.
            Site supervision, quantity estimation, BOQ preparation, MS Project.
        """,
        "jd": """
            Java Developer. Spring Boot, Hibernate, MySQL, REST APIs, Maven, Git required.
            Microservices architecture experience preferred.
        """,
        "resume_skills": ["AutoCAD", "Structural Design", "Project Management", "MS Project"],
        "jd_skills": ["Java", "Spring Boot", "Hibernate", "MySQL", "REST API", "Maven", "Git"],
        "expected": "Not Recommended",
    },

    # ── Edge cases ────────────────────────────────────────────────────────────
    {
        "id": 16,
        "label": "Fresher CS student vs Python Dev JD",
        "resume": """
            BCS final year student. Knowledge of Python, Java, HTML, CSS, JavaScript basics.
            Academic projects: student management system, library system.
            Coursework: Data Structures, DBMS, Operating Systems, Networking.
        """,
        "jd": """
            Junior Python Developer. Python, REST APIs, basic SQL required.
            Freshers welcome. Willingness to learn FastAPI and PostgreSQL.
        """,
        "resume_skills": ["Python", "Java", "HTML", "CSS", "JavaScript", "SQL"],
        "jd_skills": ["Python", "REST API", "SQL"],
        "expected": "Recommended",
    },
    {
        "id": 17,
        "label": "React Dev vs Node.js backend JD",
        "resume": """
            React developer with 2 years experience. JavaScript, TypeScript, Redux, Next.js.
            Good understanding of REST APIs. Basic Node.js knowledge.
        """,
        "jd": """
            Node.js Backend Developer. Node.js, Express, MongoDB, REST APIs, JWT auth required.
            Knowledge of React is a bonus.
        """,
        "resume_skills": ["React", "JavaScript", "TypeScript", "Redux", "Next.js", "Node.js"],
        "jd_skills": ["Node.js", "Express", "MongoDB", "REST API", "JWT"],
        "expected": "Consider",
    },
    {
        "id": 18,
        "label": "Android Dev vs Flutter JD",
        "resume": """
            Android developer with Java, Kotlin, Android SDK, Room DB, Retrofit.
            Published 3 apps on Play Store. Firebase, REST API integration.
        """,
        "jd": """
            Flutter Developer needed. Flutter, Dart, Firebase, REST APIs required.
            Mobile development experience preferred. iOS knowledge a plus.
        """,
        "resume_skills": ["Java", "Kotlin", "Android", "Firebase", "REST API", "Room DB"],
        "jd_skills": ["Flutter", "Dart", "Firebase", "REST API"],
        "expected": "Consider",
    },
    {
        "id": 19,
        "label": "Senior Python Dev vs Python JD",
        "resume": """
            Senior Python developer with 6 years experience. Expert in Django, FastAPI, Flask.
            PostgreSQL, MongoDB, Redis, Elasticsearch. AWS, GCP, Docker, Kubernetes.
            Led team of 5 developers. Microservices, gRPC, Kafka, CI/CD.
        """,
        "jd": """
            Python Developer. FastAPI or Django, PostgreSQL, Docker required.
            AWS experience preferred. REST API development essential.
        """,
        "resume_skills": ["Python", "Django", "FastAPI", "Flask", "PostgreSQL", "MongoDB",
                          "Redis", "AWS", "Docker", "Kubernetes", "Kafka"],
        "jd_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API"],
        "expected": "Highly Recommended",
    },
    {
        "id": 20,
        "label": "Content Writer vs Full Stack JD",
        "resume": """
            Content writer and blogger. SEO writing, copywriting, technical writing.
            WordPress, Canva, basic HTML knowledge. Strong English communication skills.
        """,
        "jd": """
            Full Stack Developer. React, Node.js, MongoDB, Python, Docker required.
            Strong programming background and computer science fundamentals.
        """,
        "resume_skills": ["Content Writing", "SEO", "WordPress", "HTML", "Canva"],
        "jd_skills": ["React", "Node.js", "MongoDB", "Python", "Docker"],
        "expected": "Not Recommended",
    },
]


# ── Run tests ─────────────────────────────────────────────────────────────────
def run_accuracy_test():
    print("\n" + "="*80)
    print("  RecruitAI — Matching Accuracy Test")
    print("  20 Resume-JD Pairs | Hybrid BERT + TF-IDF Scoring")
    print("="*80)
    print(f"{'ID':<4} {'Label':<40} {'Score':>6} {'Got':<22} {'Expected':<22} {'Status'}")
    print("-"*80)

    correct = 0
    results = []

    for tc in TEST_CASES:
        result = match_resume_to_jd(
            resume_text=tc["resume"],
            jd_text=tc["jd"],
            resume_skills=tc["resume_skills"],
            jd_required_skills=tc["jd_skills"],
        )
        got      = result["verdict"]
        expected = tc["expected"]
        score    = result["match_score"]
        ok       = "PASS" if got == expected else "FAIL"
        if got == expected:
            correct += 1

        print(f"{tc['id']:<4} {tc['label'][:39]:<40} {score:>5.1f}%  {got:<22} {expected:<22} {ok}")
        results.append({**tc, "score": score, "got": got, "correct": (got == expected),
                "bert_score": result.get("bert_score", 0),
                "tfidf_score": result.get("cosine_similarity", 0),
                "scoring_method": result.get("scoring_method", "N/A")})

    accuracy = correct / len(TEST_CASES) * 100
    print("-"*80)
    print(f"\n  ACCURACY:  {correct}/{len(TEST_CASES)} correct  ->  {accuracy:.1f}%")
    print(f"  Scoring Method: {results[0].get('scoring_method', 'N/A')}")
    print("="*80)

    # ── Confusion matrix ──────────────────────────────────────────────────────
    verdicts = ["Highly Recommended", "Recommended", "Consider", "Not Recommended"]
    matrix = {v: {v2: 0 for v2 in verdicts} for v in verdicts}
    for r in results:
        if r["expected"] in matrix and r["got"] in matrix[r["expected"]]:
            matrix[r["expected"]][r["got"]] += 1

    print("\n  CONFUSION MATRIX:")
    print(f"  {'Expected -> Got':<22}", "  ".join([v[:8] for v in verdicts]))
    for ev in verdicts:
        row = "  ".join(str(matrix[ev][gv]).center(8) for gv in verdicts)
        print(f"  {ev[:22]:<22} {row}")

    # ── Save results ──────────────────────────────────────────────────────────
    report = {
        "total_test_cases": len(TEST_CASES),
        "correct": correct,
        "accuracy_pct": round(accuracy, 2),
        "results": results,
    }
    with open("results/accuracy_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  [OK] Saved: results/accuracy_report.json")
    print(f"\n  Quote in your report:")
    print(f'  "RecruitAI was evaluated on 20 manually labeled resume-JD pairs.')
    print(f'   The hybrid BERT + TF-IDF model achieved {accuracy:.0f}% verdict accuracy,')
    print(f'   correctly classifying {correct} out of 20 test cases."')
    print()


if __name__ == "__main__":
    run_accuracy_test()
