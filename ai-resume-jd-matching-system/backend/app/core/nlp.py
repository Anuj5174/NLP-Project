try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
except ImportError:
    spacy = None
    nlp = None

def get_nlp():
    return nlp