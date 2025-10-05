import logging
import os
from flask import Flask, render_template, request, jsonify, send_from_directory, after_this_request, send_file
from flask_cors import CORS
from jd_parser import extract_keywords
from dynamic_parser import parse_dynamic_resume
from enhancer import enhance_resume
from pdf_generator import generate_pdf_from_template, generate_pdf_from_html_string
from file_parser import parse_file # <-- New import

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, template_folder='templates')
CORS(app)  # 启用CORS支持

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
        
        # 直接使用前端发送的数据，不使用临时文件缓存
        # 这样可以确保checkbox状态的变化能够立即反映在PDF预览中
        
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

# New API endpoints for temp file management
@app.route('/api/temp-data/<session_id>', methods=['GET'])
def get_temp_data(session_id):
    """获取临时存储的简历数据"""
    try:
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        temp_data_path = os.path.join(temp_dir, f"resume_data_{session_id}.json")
        
        if not os.path.exists(temp_data_path):
            return jsonify({"error": "Session not found"}), 404
        
        import json
        with open(temp_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error reading temp data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/temp-data/<session_id>', methods=['PUT'])
def update_temp_data(session_id):
    """更新临时存储的简历数据"""
    try:
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        temp_data_path = os.path.join(temp_dir, f"resume_data_{session_id}.json")
        
        data = request.json
        
        import json
        with open(temp_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({"success": True})
    except Exception as e:
        logging.error(f"Error updating temp data: {e}")
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

# API v1 端点 - 为LLM提供简历生成服务
@app.route('/api/v1/generate-resume', methods=['POST'])
def generate_resume_api():
    """
    为LLM提供的简历生成API端点
    接受文件、职位描述和模板参数，返回优化后的简历数据
    """
    try:
        # 获取请求数据
        job_description = request.form.get('job_description') or request.json.get('job_description')
        template_name = request.form.get('template', 'default') or request.json.get('template', 'default')
        
        # 处理文件上传
        resume_file = None
        resume_text = None
        
        if 'resume' in request.files:
            resume_file = request.files['resume']
            resume_text = parse_file(resume_file)
        elif 'resume_text' in (request.json or {}):
            resume_text = request.json['resume_text']
        
        # 验证必需参数
        if not job_description:
            return jsonify({"error": "job_description is required"}), 400
        if not resume_text:
            return jsonify({"error": "resume file or resume_text is required"}), 400

        # 提取关键词
        keywords = extract_keywords(job_description)
        keywords_str = ', '.join(keywords)

        # 解析简历结构
        parsed_resume = parse_dynamic_resume(resume_text)
        if not parsed_resume:
            return jsonify({"error": "Failed to parse resume structure"}), 400

        # 增强简历
        enhanced_resume = enhance_resume(parsed_resume, keywords_str)
        if not enhanced_resume:
            return jsonify({"error": "Failed to enhance resume"}), 400

        # 返回结构化数据
        return jsonify({
            "success": True,
            "data": {
                "enhanced_resume": enhanced_resume,
                "template": template_name,
                "keywords": keywords,
                "personal_info": enhanced_resume.get('personal_info', {}),
                "sections": {
                    "summary": enhanced_resume.get('summary', ''),
                    "experience": enhanced_resume.get('experience', []),
                    "projects": enhanced_resume.get('projects', []),
                    "education": enhanced_resume.get('education', []),
                    "skills": enhanced_resume.get('skills', []),
                    "publications": enhanced_resume.get('publications', [])
                }
            }
        })

    except Exception as e:
        logging.error(f"Error in generate_resume_api: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/v1/templates', methods=['GET'])
def get_templates_api():
    """
    返回可用模板列表的API端点
    """
    try:
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        templates = []
        
        if os.path.exists(templates_dir):
            for file in os.listdir(templates_dir):
                if file.endswith('.html'):
                    template_name = file.replace('.html', '')
                    templates.append({
                        "name": template_name,
                        "display_name": template_name.title(),
                        "file": file
                    })
        
        return jsonify({
            "success": True,
            "templates": templates
        })
    
    except Exception as e:
        logging.error(f"Error in get_templates_api: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)