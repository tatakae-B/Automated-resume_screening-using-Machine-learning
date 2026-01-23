from flask import Flask, render_template, request
import os
import sys
import tempfile
from werkzeug.utils import secure_filename
import time
import pdfplumber
import re

# Create Flask app with correct paths
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# ============ Embedded Functions ============

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        if not text.strip():
            print(f"Warning: No text extracted from {pdf_path}.")
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def preprocess_text(text):
    """Preprocesses text for comparison."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
    text = ' '.join(text.split())
    return text

def extract_and_preprocess_resumes(resume_paths):
    """Extracts and preprocesses resumes from the given paths."""
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

    if skipped_files:
        print(f"Skipped files: {skipped_files}")

    return resumes

def calculate_tfidf_similarity(resume_texts, job_description):
    """Calculate similarity using simple keyword matching and term frequency."""
    def tokenize(text):
        return set(text.lower().split())
    
    job_tokens = tokenize(job_description)
    similarity_scores = []
    
    for resume_text in resume_texts:
        resume_tokens = tokenize(resume_text)
        
        if len(job_tokens | resume_tokens) == 0:
            similarity = 0.0
        else:
            intersection = len(job_tokens & resume_tokens)
            union = len(job_tokens | resume_tokens)
            similarity = intersection / union
        
        resume_word_count = len(resume_tokens)
        if resume_word_count > 0:
            matching_words = len(job_tokens & resume_tokens)
            tf_score = matching_words / resume_word_count
            combined_score = (similarity + tf_score) / 2
        else:
            combined_score = similarity
        
        similarity_scores.append(combined_score)
    
    return similarity_scores

def vectorize_and_calculate_similarity(resumes, job_description):
    """Calculates similarity scores using lightweight keyword matching."""
    job_desc_processed = preprocess_text(job_description)
    if not job_desc_processed.strip():
        raise ValueError("Job description is empty or invalid after preprocessing.")

    resume_texts = [resume[1] for resume in resumes]
    if not resume_texts:
        raise ValueError("No valid resumes to process.")

    similarity_scores = calculate_tfidf_similarity(resume_texts, job_desc_processed)
    similarity_percentages = [round(score * 100, 2) for score in similarity_scores]

    for i, score in enumerate(similarity_percentages):
        print(f"Resume {i + 1} Similarity: {score}%")

    return similarity_percentages

def rank_resumes_by_similarity(similarity_scores, resumes):
    """Ranks resumes based on similarity scores in descending order."""
    ranked_resumes = sorted(zip(resumes, similarity_scores), key=lambda x: x[1], reverse=True)
    return ranked_resumes

# ============ Flask Routes ============

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return render_template('index.html', error="Job description cannot be empty.")

        uploaded_files = request.files.getlist('resumes')
        if len(uploaded_files) > 5:
            return render_template('index.html', error="You can only upload up to 5 resumes at a time.")

        resume_paths = []
        for file in uploaded_files:
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{int(time.time())}_{filename}")
                file.save(filepath)
                resume_paths.append(filepath)

        if not resume_paths:
            return render_template('index.html', error="Please upload at least one PDF resume.")

        resumes = extract_and_preprocess_resumes(resume_paths)
        if not resumes:
            return render_template('index.html', error="No valid resumes to process.")

        try:
            similarity_percentages = vectorize_and_calculate_similarity(resumes, job_description)
            ranked_resumes = rank_resumes_by_similarity(similarity_percentages, resumes)
            ranked_resumes = [(os.path.basename(resume[0]), score) for resume, score in ranked_resumes]
        except ValueError as e:
            return render_template('index.html', error=str(e))

        return render_template('results.html', ranked_resumes=ranked_resumes)

    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
    return index()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# Fresh deploy trigger
