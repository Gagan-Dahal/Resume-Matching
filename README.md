# Resume-Matching
Indented to match Job description with resume and ouput a score.

# Intended Architecture
PDF -> Text Extraction -> Preprocessing -> Embedding -> Similarity Scoring -> Report

1. Text Extraction from PDFs: Using PyMuPDF(fitz)
2. Preprocessing and Keyword Extraction(skill, education and experience): Using Regex, spacy and skillNER (Named Entity Recognition)
3. Similarity System: Two-layer similarity system
    - Keyword ovesrlap between description and resume
    - Contextual overlap and extra skills/experience/eduaction
4. Weighted Scoring and Output
