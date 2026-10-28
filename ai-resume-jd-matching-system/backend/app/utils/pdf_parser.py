"""
PDF parsing utilities
"""
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

from typing import Optional
import re


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF file using pdfplumber, with pypdf and fitz fallbacks
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    # 1. Try pdfplumber
    if pdfplumber is not None:
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass

    # 2. Fallback to pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    # 3. Fallback to PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    raise Exception(f"Unable to extract text from PDF: {pdf_path}")


def clean_text(text: str) -> str:
    """
    Clean extracted text
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep essential punctuation
    text = re.sub(r'[^\w\s@.,\-+()]', '', text)
    
    return text.strip()


def extract_email(text: str) -> Optional[str]:
    """
    Extract email from text
    
    Args:
        text: Text to search
        
    Returns:
        Email address or None
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text
    
    Args:
        text: Text to search
        
    Returns:
        Phone number or None
    """
    # Indian phone patterns
    phone_patterns = [
        r'\+91[-\s]?\d{10}',  # +91-1234567890
        r'\d{10}',            # 1234567890
        r'\(\d{3}\)[-\s]?\d{3}[-\s]?\d{4}'  # (123) 456-7890
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None


def extract_name_from_text(text: str) -> Optional[str]:
    """
    Extract candidate name from resume text
    Simple heuristic: first line that looks like a name
    
    Args:
        text: Resume text
        
    Returns:
        Candidate name or None
    """
    lines = text.split('\n')
    
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip lines with email or phone
        if '@' in line or re.search(r'\d{10}', line):
            continue
        
        # Check if line looks like a name (2-4 words, title case)
        words = line.split()
        if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words if word):
            return line
    
    return None


def parse_resume(pdf_path: str) -> dict:
    """
    Parse resume and extract all information
    """
    from app.utils.skill_extractor import get_skill_names_only

    # Extract raw text
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Clean text
    cleaned_text = clean_text(raw_text)
    
    # Extract metadata
    candidate_name  = extract_name_from_text(raw_text)
    candidate_email = extract_email(raw_text)
    candidate_phone = extract_phone(raw_text)
    
    # ── Extract skills ──────────────────────────────
    skills = get_skill_names_only(raw_text)
    
    return {
        "extracted_text":   raw_text,
        "cleaned_text":     cleaned_text,
        "candidate_name":   candidate_name,
        "candidate_email":  candidate_email,
        "candidate_phone":  candidate_phone,
        "skills_extracted": skills,       # ← NEW
    }