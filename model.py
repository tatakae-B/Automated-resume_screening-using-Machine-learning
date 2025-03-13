from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

def vectorize_and_calculate_similarity(resumes, job_description):
    """
    Vectorizes resumes and job description, then calculates similarity scores.
    Uses less restrictive parameters for TF-IDF.
    """
    job_desc_processed = preprocess_text(job_description)
    if not job_desc_processed.strip():
        raise ValueError("Job description is empty or invalid after preprocessing.")

    resume_texts = [resume[1] for resume in resumes]
    if not resume_texts:
        raise ValueError("No valid resumes to process.")

    all_text = resume_texts + [job_desc_processed]

    # Adjust vectorizer for flexibility
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words=None, ngram_range=(1, 2), use_idf=False)
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # Debugging: Print TF-IDF features
    print("TF-IDF Feature Names:", vectorizer.get_feature_names_out())

    # Calculate cosine similarities
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    similarity_percentages = [round(score * 100, 2) for score in cosine_similarities.flatten()]

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
