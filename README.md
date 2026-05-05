# Resume-Matching
Indented to match Job description with resume and ouput a score.

# Intended Architecture
PDF -> Text Extraction -> Preprocessing -> Embedding -> Similarity Scoring -> Report

1. Text Extraction from PDFs: Using PyMuPDF
2. Preprocessing and Keyword Extraction: Using spacy (Named Entity Recognition)
3. Similarity System: Two-layer similarity system
    - Keyword ovesrlap between description and resume
    - Cosine Similarity using sentence embeddings
4. Weighted Scoring and Output
