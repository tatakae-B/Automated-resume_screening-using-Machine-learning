import numpy as np
from resume_processing import extract_text_from_pdf, preprocess_text

def extract_and_preprocess_resumes(resume_paths):
    """
    Extracts and preprocesses resumes from the given paths.
    Skips files with no valid text and logs them.
    """
    resumes = []
    skipped_files = []

    for resume_path in resume_paths:
        text = extract_text_from_pdf(resume_path)
        if not text.strip():
            print(f"Skipping {resume_path}: No text extracted.")
            skipped_files.append(resume_path)
            continue
        processed_text = preprocess_text(text)
        if not processed_text.strip():
            print(f"Skipping {resume_path}: No valid content after preprocessing.")
            skipped_files.append(resume_path)
            continue
        resumes.append((resume_path, processed_text))

    # Log skipped files
    if skipped_files:
        print(f"Skipped files: {skipped_files}")

    return resumes

def calculate_tfidf_similarity(resume_texts, job_description):
    """
    Calculate similarity using simple keyword matching and term frequency.
    Lightweight alternative to scikit-learn's TfidfVectorizer.
    """
    # Tokenize all texts
    def tokenize(text):
        return set(text.lower().split())
    
    job_tokens = tokenize(job_description)
    
    similarity_scores = []
    for resume_text in resume_texts:
        resume_tokens = tokenize(resume_text)
        
        # Calculate Jaccard similarity
        if len(job_tokens | resume_tokens) == 0:
            similarity = 0.0
        else:
            intersection = len(job_tokens & resume_tokens)
            union = len(job_tokens | resume_tokens)
            similarity = intersection / union
        
        # Also calculate term frequency overlap
        resume_word_count = len(resume_tokens)
        if resume_word_count > 0:
            matching_words = len(job_tokens & resume_tokens)
            tf_score = matching_words / resume_word_count
            # Combine both metrics
            combined_score = (similarity + tf_score) / 2
        else:
            combined_score = similarity
        
        similarity_scores.append(combined_score)
    
    return similarity_scores

def vectorize_and_calculate_similarity(resumes, job_description):
    """
    Calculates similarity scores using lightweight keyword matching.
    """
    job_desc_processed = preprocess_text(job_description)
    if not job_desc_processed.strip():
        raise ValueError("Job description is empty or invalid after preprocessing.")

    resume_texts = [resume[1] for resume in resumes]
    if not resume_texts:
        raise ValueError("No valid resumes to process.")

    # Calculate similarity scores
    similarity_scores = calculate_tfidf_similarity(resume_texts, job_desc_processed)
    similarity_percentages = [round(score * 100, 2) for score in similarity_scores]

    # Debugging: Print similarity scores
    for i, score in enumerate(similarity_percentages):
        print(f"Resume {i + 1} Similarity: {score}%")

    return similarity_percentages

def rank_resumes_by_similarity(similarity_scores, resumes):
    """
    Ranks resumes based on similarity scores in descending order.
    """
    ranked_resumes = sorted(zip(resumes, similarity_scores), key=lambda x: x[1], reverse=True)
    return ranked_resumes
