// 预览和下载功能模块

function initPreviewAndDownload() {
    // 下载按钮事件
    document.getElementById('download-btn').addEventListener('click', function() {
        if (!enhancedResumeData) {
            alert("Please generate a resume first.");
            return;
        }

        // Send structured resume data instead of HTML
        const sectionOrder = getSectionOrder();
        
        // 收集checkbox状态
        const resumeData = {};
        
        // 检查各个section的checkbox状态
        const toggleSummary = document.getElementById('toggle-summary');
        const toggleExperience = document.getElementById('toggle-experience');
        const toggleProjects = document.getElementById('toggle-projects');
        const toggleEducation = document.getElementById('toggle-education');
        const toggleSkills = document.getElementById('toggle-skills');
        const togglePublications = document.getElementById('toggle-publications');
        
        // 添加基本信息和section顺序
        resumeData.personal_info = {
            name: enhancedResumeData.personal_info?.name || '',
            email: enhancedResumeData.personal_info?.email || '',
            phone: enhancedResumeData.personal_info?.phone || ''
        };
        resumeData.section_order = sectionOrder;
        
        if (toggleSummary && toggleSummary.checked) {
            resumeData.summary = enhancedResumeData.summary || '';
        } else {
            resumeData.summary = ''; // 明确设置为空字符串
        }
        if (toggleExperience && toggleExperience.checked) {
            resumeData.experience = enhancedResumeData.experience || [];
        } else {
            resumeData.experience = []; // 明确设置为空数组
        }
        if (toggleProjects && toggleProjects.checked) {
            resumeData.projects = enhancedResumeData.projects || [];
        } else {
            resumeData.projects = []; // 明确设置为空数组
        }
        if (toggleEducation && toggleEducation.checked) {
            resumeData.education = enhancedResumeData.education || [];
        } else {
            resumeData.education = []; // 明确设置为空数组
        }
        if (toggleSkills && toggleSkills.checked) {
            resumeData.skills = enhancedResumeData.skills || [];
        } else {
            resumeData.skills = []; // 明确设置为空数组
        }
        if (togglePublications && togglePublications.checked) {
            resumeData.publications = enhancedResumeData.publications || [];
        } else {
            resumeData.publications = []; // 明确设置为空数组
        }

        fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.DOWNLOAD}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_data: resumeData,
                template_name: document.getElementById('template-select').value,
                session_id: currentSessionId // 添加会话ID
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'resume.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
    });

    // 预览按钮事件
    document.getElementById('preview-btn').addEventListener('click', function() {
        if (!enhancedResumeData) {
            alert("Please generate a resume first.");
            return;
        }

        // Send structured resume data instead of HTML
        const sectionOrder = getSectionOrder();
        
        // 检查每个checkbox的状态
        const checkboxStates = {};
        ['toggle-summary', 'toggle-experience', 'toggle-projects', 'toggle-education', 'toggle-skills', 'toggle-publications'].forEach(id => {
            const checkbox = document.getElementById(id);
            checkboxStates[id] = checkbox ? checkbox.checked : false;
        });
        
        // 添加调试日志
        console.log('Preview button - Checkbox states:', checkboxStates);
        
        const resumeData = {
            personal_info: {
                name: enhancedResumeData.personal_info?.name || '',
                email: enhancedResumeData.personal_info?.email || '',
                phone: enhancedResumeData.personal_info?.phone || ''
            },
            section_order: sectionOrder, // 添加section顺序信息
            summary: checkboxStates['toggle-summary'] ? (enhancedResumeData.summary || '') : '',
            experience: checkboxStates['toggle-experience'] ? (enhancedResumeData.experience || []) : [],
            projects: checkboxStates['toggle-projects'] ? (enhancedResumeData.projects || []) : [],
            education: checkboxStates['toggle-education'] ? (enhancedResumeData.education || []) : [],
            skills: checkboxStates['toggle-skills'] ? (enhancedResumeData.skills || []) : [],
            publications: checkboxStates['toggle-publications'] ? (enhancedResumeData.publications || []) : []
        };
        
        console.log('Preview button - Final resumeData being sent:', resumeData);

        // 显示更新状态
        const previewBtn = document.getElementById('preview-btn');
        const originalText = previewBtn.textContent;
        previewBtn.textContent = '更新中...';
        previewBtn.disabled = true;

        fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PREVIEW}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_data: resumeData,
                template_name: document.getElementById('template-select').value,
                session_id: currentSessionId // 添加会话ID
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const previewContainer = document.getElementById('pdf-preview-container');
            const previewIframe = document.getElementById('pdf-preview-iframe');
            previewIframe.src = url;
            previewContainer.style.display = 'block';
            
            // 恢复按钮状态
            previewBtn.textContent = originalText;
            previewBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            // 恢复按钮状态
            previewBtn.textContent = originalText;
            previewBtn.disabled = false;
        });
    });
}