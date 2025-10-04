import requests
import os

def test_llm_call():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, 'backend')
    resume_path = os.path.join(backend_dir, 'mock_resume.txt')
    jd_path = os.path.join(backend_dir, 'mock_jd.txt')

    with open(resume_path, 'rb') as f:
        resume_content = f.read()

    with open(jd_path, 'r') as f:
        jd_content = f.read()

    files = {'resume': ('mock_resume.txt', resume_content, 'text/plain')}
    data = {'job_description': jd_content}

    response = requests.post('http://127.0.0.1:5000/upload', files=files, data=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(response.json())
    else:
        print("Error:")
        print(response.text)

if __name__ == '__main__':
    test_llm_call()