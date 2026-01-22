from flask import Flask, render_template, request
import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import extract_and_preprocess_resumes, vectorize_and_calculate_similarity, rank_resumes_by_similarity
from werkzeug.utils import secure_filename
import time

app = Flask(__name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

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

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
