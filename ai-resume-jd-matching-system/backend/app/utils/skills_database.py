"""
Skills Database - 500+ technical and soft skills across 10 categories
"""

SKILLS_DATABASE = {

    "programming_languages": [
        "python", "java", "javascript", "typescript", "c", "c++", "c#",
        "php", "ruby", "swift", "kotlin", "go", "rust", "scala", "r",
        "matlab", "perl", "shell", "bash", "powershell", "dart", "lua",
        "haskell", "elixir", "clojure", "groovy", "objective-c", "assembly",
        "cobol", "fortran", "vba", "sql", "plsql", "tsql"
    ],

    "frameworks_libraries": [
        "react", "reactjs", "react.js", "angular", "angularjs", "vue",
        "vuejs", "vue.js", "nextjs", "next.js", "nuxtjs", "svelte",
        "django", "flask", "fastapi", "spring", "spring boot", "springboot",
        "express", "expressjs", "nodejs", "node.js", "laravel", "rails",
        "ruby on rails", "asp.net", "dotnet", ".net", "hibernate",
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "scipy",
        "opencv", "nltk", "spacy", "huggingface", "transformers",
        "bootstrap", "tailwind", "tailwindcss", "material-ui", "mui",
        "jquery", "redux", "graphql", "rest", "restful", "soap",
        "celery", "rabbitmq", "kafka", "socket.io", "websocket"
    ],

    "databases": [
        "mysql", "postgresql", "postgres", "sqlite", "oracle", "sql server",
        "mssql", "mongodb", "cassandra", "redis", "elasticsearch", "dynamodb",
        "firebase", "firestore", "neo4j", "couchdb", "mariadb", "db2",
        "hbase", "influxdb", "timescaledb", "cockroachdb", "supabase",
        "planetscale", "prisma", "sqlalchemy", "sequelize", "mongoose"
    ],

    "cloud_devops": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp",
        "google cloud", "docker", "kubernetes", "k8s", "terraform",
        "ansible", "jenkins", "github actions", "gitlab ci", "circleci",
        "travis ci", "helm", "prometheus", "grafana", "elk stack",
        "logstash", "kibana", "nginx", "apache", "linux", "ubuntu",
        "centos", "debian", "vagrant", "puppet", "chef", "saltstack",
        "cloudformation", "pulumi", "heroku", "vercel", "netlify",
        "digitalocean", "linode", "ec2", "s3", "lambda", "rds",
        "cloudwatch", "iam", "vpc", "load balancer", "cdn", "ci/cd",
        "devops", "sre", "site reliability"
    ],

    "web_technologies": [
        "html", "html5", "css", "css3", "sass", "scss", "less",
        "javascript", "typescript", "json", "xml", "yaml", "rest api",
        "graphql", "websocket", "http", "https", "oauth", "jwt",
        "cors", "webpack", "vite", "babel", "eslint", "prettier",
        "npm", "yarn", "pnpm", "responsive design", "pwa",
        "progressive web app", "spa", "single page application",
        "ssr", "server side rendering", "seo", "web scraping",
        "selenium", "puppeteer", "playwright"
    ],

    "tools_ides": [
        "git", "github", "gitlab", "bitbucket", "vs code", "vscode",
        "visual studio", "intellij", "pycharm", "eclipse", "netbeans",
        "xcode", "android studio", "postman", "insomnia", "swagger",
        "jira", "confluence", "trello", "slack", "figma", "adobe xd",
        "photoshop", "illustrator", "sketch", "notion", "linear",
        "datagrip", "dbeaver", "pgadmin", "mongodb compass",
        "tableau", "power bi", "excel", "jupyter", "jupyter notebook",
        "google colab", "anaconda", "virtualenv", "poetry"
    ],

    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "project management",
        "analytical thinking", "creativity", "adaptability", "collaboration",
        "presentation skills", "public speaking", "negotiation",
        "conflict resolution", "mentoring", "coaching", "decision making",
        "attention to detail", "self-motivated", "fast learner",
        "multitasking", "organizational skills", "interpersonal skills"
    ],

    "methodologies": [
        "agile", "scrum", "kanban", "waterfall", "lean", "xp",
        "extreme programming", "tdd", "test driven development",
        "bdd", "behavior driven development", "ddd", "domain driven design",
        "microservices", "monolithic", "mvc", "mvvm", "clean architecture",
        "solid principles", "design patterns", "oop", "object oriented",
        "functional programming", "event driven", "rest", "soap",
        "api design", "system design", "high level design"
    ],

    "testing": [
        "unit testing", "integration testing", "e2e testing",
        "end to end testing", "selenium", "cypress", "jest",
        "pytest", "unittest", "mocha", "chai", "jasmine",
        "testng", "junit", "mockito", "postman", "jmeter",
        "load testing", "performance testing", "regression testing",
        "manual testing", "automation testing", "qa", "quality assurance"
    ],

    "domain_knowledge": [
        "machine learning", "ml", "deep learning", "artificial intelligence",
        "ai", "natural language processing", "nlp", "computer vision",
        "data science", "data analysis", "data engineering", "big data",
        "data visualization", "business intelligence", "bi",
        "blockchain", "cryptocurrency", "web3", "iot",
        "internet of things", "ar", "augmented reality", "vr",
        "virtual reality", "cybersecurity", "network security",
        "penetration testing", "ethical hacking", "cloud computing",
        "distributed systems", "system design", "algorithms",
        "data structures", "fintech", "edtech", "healthtech",
        "ecommerce", "saas", "paas", "iaas"
    ]
}

# Synonym mapping - maps variations to standard skill name
SKILL_SYNONYMS = {
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node": "node.js",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular",
    "nextjs": "next.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "tf": "tensorflow",
    "k8s": "kubernetes",
    "aws": "amazon web services",
    "gcp": "google cloud",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "dl": "deep learning",
    "cv": "computer vision",
    "oop": "object oriented programming",
    "tdd": "test driven development",
    "bdd": "behavior driven development",
    "ci/cd": "ci cd",
    "vscode": "vs code",
    "springboot": "spring boot",
    ".net": "dotnet",
    "tailwind": "tailwindcss",
    "mui": "material-ui",
}


def get_all_skills() -> list:
    """Returns flat list of all skills"""
    all_skills = []
    for category_skills in SKILLS_DATABASE.values():
        all_skills.extend(category_skills)
    return list(set(all_skills))


def get_skill_category(skill: str) -> str:
    """Returns category of a skill"""
    skill_lower = skill.lower()
    for category, skills in SKILLS_DATABASE.items():
        if skill_lower in skills:
            return category
    return "other"


def normalize_skill(skill: str) -> str:
    """Normalize skill using synonym mapping"""
    skill_lower = skill.lower().strip()
    return SKILL_SYNONYMS.get(skill_lower, skill_lower)
