import logging
import os
from flask import Flask, render_template, request, jsonify, send_from_directory, after_this_request, send_file
from jd_parser import extract_keywords
from dynamic_parser import parse_dynamic_resume
from enhancer import enhance_resume
from pdf_generator import generate_pdf_from_template, generate_pdf_from_html_string
from file_parser import parse_file # <-- New import

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    job_description = request.form.get('job_description')
    resume_file = request.files.get('resume')

    if not job_description or not resume_file:
        return jsonify({"error": "Job description and resume file are required."}), 400

    # Parse the resume file
    resume_text = parse_file(resume_file)
    if not resume_text:
        return jsonify({"error": "Failed to parse resume file."}), 400

    # Extract keywords from job description
    keywords = extract_keywords(job_description)
    keywords_str = ', '.join(keywords)

    # Parse resume into structured format
    parsed_resume = parse_dynamic_resume(resume_text)
    if not parsed_resume:
        return jsonify({"error": "Failed to parse resume structure."}), 400

    # Enhance the resume with job description keywords
    enhanced_resume = enhance_resume(parsed_resume, keywords_str)
    if not enhanced_resume:
        return jsonify({"error": "Failed to enhance resume."}), 400

    return jsonify({
        "enhanced_resume": enhanced_resume,
        "email": enhanced_resume.get('personal_info', {}).get('email', ''),
        "phone": enhanced_resume.get('personal_info', {}).get('phone', '')
    })

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    
    # Check if we're receiving structured resume data or HTML content
    if 'resume_data' in data:
        # New approach: use structured data with templates
        resume_data = data.get('resume_data')
        template_name = data.get("template", "default")
        
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        pdf_path = os.path.join(temp_dir, f"resume_{os.urandom(8).hex()}.pdf")
        
        success = generate_pdf_from_template(resume_data, template_name, pdf_path)
        
    else:
        # Legacy approach: use HTML content directly
        html_content = data.get('html_content')
        template_name = data.get("template", "default.html")
        
        if not html_content:
            return jsonify({"error": "No HTML content provided"}), 400
        
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        pdf_path = os.path.join(temp_dir, f"resume_{os.urandom(8).hex()}.pdf")
        
        success = generate_pdf_from_html_string(html_content, template_name, pdf_path)

    if not success:
        return jsonify({"error": "Failed to generate PDF."}), 500

    @after_this_request
    def cleanup(response):
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            logging.error(f"Error cleaning up file {pdf_path}: {e}")
        return response

    return send_from_directory(os.path.dirname(pdf_path), os.path.basename(pdf_path), as_attachment=True)

@app.route('/api/preview-pdf', methods=['POST'])
def preview_pdf():
    data = request.json
    
    # Check if we're receiving structured resume data or HTML content
    if 'resume_data' in data:
        # New approach: use structured data with templates
        resume_data = data.get('resume_data')
        template_name = data.get('template', 'default')
        
        try:
            pdf_file = generate_pdf_from_template(resume_data, template_name)
            return send_file(
                pdf_file,
                as_attachment=False,
                mimetype='application/pdf'
            )
        except Exception as e:
            logging.error(f"Error generating PDF preview: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        # Legacy approach: use HTML content directly
        html_content = data.get('html_content')
        template_name = data.get('template', 'default')

        if not html_content:
            return jsonify({"error": "No HTML content provided"}), 400

        try:
            # Create temporary file for legacy mode
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            pdf_path = os.path.join(temp_dir, f"preview_{os.urandom(8).hex()}.pdf")
            success = generate_pdf_from_html_string(html_content, template_name, pdf_path)
            
            if not success:
                return jsonify({"error": "Failed to generate PDF preview"}), 500
            
            @after_this_request
            def cleanup(response):
                try:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                except Exception as e:
                    logging.error(f"Error cleaning up preview file {pdf_path}: {e}")
                return response
            
            return send_from_directory(os.path.dirname(pdf_path), os.path.basename(pdf_path), as_attachment=False, mimetype='application/pdf')
            
        except Exception as e:
            logging.error(f"Error generating PDF preview: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)