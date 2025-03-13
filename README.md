# Automated Resume Screening using Machine Learning

## 📌 Project Overview
Automated Resume Screening is a machine learning-based application that filters and ranks resumes based on predefined criteria. This project aims to reduce manual effort in hiring by using Natural Language Processing (NLP) to analyze and score resumes.

## 🚀 Features
- Extracts text from resumes (PDF/DOCX format)
- Preprocesses and cleans the extracted text
- Uses NLP techniques for keyword matching and similarity scoring
- Implements machine learning models to rank candidates
- Provides a user-friendly interface for HR teams

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Libraries**: 
  - Pandas, NumPy (Data Processing)
  - Scikit-learn (Machine Learning)
  - NLTK, SpaCy (NLP Processing)
  - Flask / Streamlit (Web Interface, if applicable)
  - PyPDF2, docx2txt (Resume Parsing)

## 📂 Project Structure
```
📦 Automated-resume_screening
├── 📂 data                    # Sample resume dataset
├── 📂 models                  # Trained ML models
├── 📂 scripts                 # Preprocessing and training scripts
├── app.py                     # Main application script
├── requirements.txt           # Required Python dependencies
├── README.md                  # Project documentation
```

## 📊 How It Works
1. Upload resumes in PDF/DOCX format.
2. Extract text and preprocess (remove stopwords, lemmatization, etc.).
3. Compare skills and experience with job descriptions.
4. Rank candidates based on similarity scores using ML models.
5. Display results with recommendations.

## 🔧 Installation & Usage
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/tatakae-B/Automated-resume_screening-using-Machine-learning.git
cd Automated-resume_screening-using-Machine-learning
```
### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 3️⃣ Run the Application
```sh
python app.py
```
*If using Flask/Streamlit, access the web UI at `http://localhost:5000`.*

## 📈 Model Training
- Dataset: Use a labeled dataset of resumes and job descriptions.
- Preprocessing: Tokenization, stopword removal, TF-IDF vectorization.
- Model: Train a machine learning classifier (e.g., Logistic Regression, SVM, or Transformer-based models like BERT).
- Evaluation: Use accuracy, precision, recall, and F1-score metrics.

## 🎯 Future Enhancements
- Improve NLP processing with contextual embeddings (BERT, GPT, etc.).
- Integrate an API for real-time resume screening.
- Develop a web-based dashboard for HR teams.

## 📜 License
This project is open-source and available under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## 📧 Contact
For any queries or collaborations, reach out via [GitHub Issues](https://github.com/tatakae-B/Automated-resume_screening-using-Machine-learning/issues).
