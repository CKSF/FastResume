import os
import sys
import time
import logging
from pdf2docx import Converter
from docx import Document

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
from pdf_generator import generate_pdf

# --- Configuration ---
# The text to verify in the final PDF, chosen to confirm dynamic content rendering.
VERIFICATION_TEXT = "SeizureFormer"
CHECK_INTERVAL_SECONDS = 10

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_content_via_roundtrip(pdf_path, expected_text):
    """
    Verifies content by converting PDF back to DOCX and then checking the text.
    """
    temp_docx_path = pdf_path.replace('.pdf', '-reconverted.docx')
    try:
        # Convert PDF back to DOCX
        cv = Converter(pdf_path)
        cv.convert(temp_docx_path, start=0, end=None)
        cv.close()

        # Read the text from the reconverted DOCX
        doc = Document(temp_docx_path)
        full_text = "\n".join([p.text for p in doc.paragraphs])

        if expected_text.lower() in full_text.lower():
            logging.info(f"SUCCESS: Found '{expected_text}' in the reconverted DOCX. The dynamic template system is working!")
            return True
        else:
            logging.error(f"FAILURE: Did not find '{expected_text}' in the reconverted DOCX.")
            return False
    finally:
        # Clean up temporary files
        if os.path.exists(temp_docx_path):
            os.remove(temp_docx_path)

def main():
    """Main entry point for the validation run."""
    logging.info("--- Starting Final Validation Run ---")
    
    # Full context data based on the user's resume
    context_data = {
        "name": "Tianning Feng",
        "address": "3131 Walnut Street, Philadelphia, PA",
        "phone": "+1 (404)519-1450",
        "email": "tfeng24@seas.upenn.edu",
        "github": "github.com/CKSF",
        "linkedin": "linkedin.com/in/cksf",
        "education": [
            {"institution": "University of Pennsylvania", "degree": "MSE in Computer & Information Science", "dates": "Expected May 2027"},
            {"institution": "Emory University", "degree": "B.S. in Computer Science, GPA: 3.794/4.0", "dates": "Aug 2021 - May 2025"}
        ],
        "professional_experience": [
            {
                "company": "Shen Tong Technology Group Co., Ltd (Ningbo, China)", "title": "Frontend Developer Intern", "dates": "Jun 2021 – Aug 2021",
                "description_points": [
                    "Coordinated a team UI redesign for automotive cooling & intake systems. I ran user studies/usability tests, turned insights into wireframes/prototypes with partner teams, contributing to a +30% usability gain.",
                    "Led the design of the subsidiary’s logo and corporate branding/visual identity guidelines (including standardized designs for company stationery and merchandise); the design was officially adopted and registered as a company trademark."
                ]
            }
        ],
        "research_experience": [
            {
                "lab": "Melody Lab (Emory University)", "title": "Deep Learning Researcher", "dates": "Sep 2023 – May 2025",
                "description_points": [
                    "Collaborated with Emory Clinic on seizure forecasting using RNS data; led the development of a Transformer-based model (SeizureFormer) capable of predicting seizure risk 1–14 days in advance, achieving state-of-the-art performance.",
                    "Researched epidemic source detection and spread prediction with Hypergraph Neural Networks (EpiDHGNN), achieving up to 7–12% accuracy improvement and 30% faster convergence compared to baseline models"
                ]
            },
            {
                "lab": "Language Biomarker Lab (Emory University)", "title": "Research Assistant", "dates": "Sep 2022 – Nov 2024",
                "description_points": [
                    "Built automated pipelines using pretrained models from Hugging Face, finetuned in PyTorch, and integrated with statistical analysis approaches, enabling 24/7 processing, reducing manual workload by 80%",
                    "Preprocessed 100+ GB of raw primate data and standardized thousands of unstructured entries (video, annotations, sensor data), making previously unusable data usable for ongoing studies"
                ]
            }
        ],
        "projects": [
            {
                "name": "SeizureFormer", "dates": "Sep 2024 – Present",
                "description_points": [
                    "Led a team of 3 in seizure forecasting research, resulting in a paper accepted by PSB 2026 (oral presentations in Hawaii).",
                    "Preliminary results are now being translated into clinical applications, drawing industry interest from NeuroPace.",
                    "Currently expanding to full-cohort validation and patient-specific factor analysis to support real-world deployment."
                ]
            },
            {
                "name": "Smart Home Assistant Development", "dates": "Jan 2024 – Jan 2025",
                "description_points": ["Key contributor to a cross-platform smart home assistant. I owned MongoDB design, Swift architecture, and real-time sync, reducing latency to <200ms and supporting simultaneous control of 15+ smart devices."]
            }
        ],
        "skills": [
            {"category": "Programming", "items": "Python, Java, C/C++, Swift"},
            {"category": "Databases", "items": "SQL, NoSQL (MongoDB, Neo4j), Vector Databases"},
            {"category": "Machine Learning & AI", "items": "Deep Learning, Reinforcement Learning, Data Mining"},
            {"category": "Lab & Research", "items": "Experimental design, academic writing, literature review, scientific presentation"}
        ],
        "publications": [
            {"citation": "Feng, T., Ni, J., Gleichgerrcht, E., Jin, W. SeizureFormer: A Transformer Model for IEA-Based Seizure Risk Forecasting. Pacific Symposium on Biocomputing (PSB 2026) — accepted for oral presentation (Hawaii, 2026)."},
            {"citation": "Liu, S.; Gong, S.; Feng, T.; Liu, Z.; Lau, M. S. Y.; Jin, W. Higher-order Interaction Matters: Dynamic Hypergraph Neural Networks for Epidemic Modeling (EpiDHGNN). Pacific Symposium on Biocomputing (PSB 2026)"}
        ]
    }

    pdf_path = None
    temp_docx_path = None
    try:
        pdf_path, temp_docx_path = generate_pdf(context_data)

        # --- Verification Step (Round-trip) ---
        if pdf_path:
            verify_content_via_roundtrip(pdf_path, VERIFICATION_TEXT)

    finally:
        # Clean up all generated temporary files
        if temp_docx_path and os.path.exists(temp_docx_path):
            logging.info(f"Cleaned up temporary DOCX: {temp_docx_path}")
            os.remove(temp_docx_path)
        if pdf_path and os.path.exists(pdf_path):
            logging.info(f"Cleaned up temporary PDF: {pdf_path}")
            os.remove(pdf_path)
    
    logging.info("--- Validation run finished ---")

if __name__ == "__main__":
    main()