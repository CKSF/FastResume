// 简历生成模块

function initResumeGeneration() {
    document.getElementById('upload-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 显示loading指示器，隐藏按钮
        const optimizeBtn = document.getElementById('optimize-btn');
        const loadingIndicator = document.getElementById('loading-indicator');
        optimizeBtn.style.display = 'none';
        loadingIndicator.style.display = 'block';
        
        var formData = new FormData(this);

        fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.UPLOAD}`, {
            method: 'POST', 
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            enhancedResumeData = data.enhanced_resume; // <-- Correctly access the nested object
            let resumeHTML = '<div class="resume">';

            // Left Column
            resumeHTML += '<div class="left-column">';

            // Personal Info
            if (enhancedResumeData.personal_info) {
                resumeHTML += '<div class="personal-info">';
                resumeHTML += `<h1 class="name">${enhancedResumeData.personal_info.name || ''}</h1>`;
                resumeHTML += `<p class="contact">${enhancedResumeData.personal_info.email || ''} | ${enhancedResumeData.personal_info.phone || ''}</p>`;
                resumeHTML += '</div>';
            }

            // Skills
            if (enhancedResumeData.skills && enhancedResumeData.skills.length > 0) {
                resumeHTML += '<div class="skills-section">';
                resumeHTML += '<h2 class="section-title">Skills</h2>';
                resumeHTML += '<ul class="skills-list">';
                enhancedResumeData.skills.forEach(skill => {
                    resumeHTML += `<li>${skill}</li>`;
                });
                resumeHTML += '</ul>';
                resumeHTML += '</div>';
            }

            // Education
            if (enhancedResumeData.education && enhancedResumeData.education.length > 0) {
                resumeHTML += '<div class="education-section">';
                resumeHTML += '<h2 class="section-title">Education</h2>';
                enhancedResumeData.education.forEach(edu => {
                    resumeHTML += '<div class="education-item">';
                    resumeHTML += `<p><strong>${edu.degree}</strong> in ${edu.major}</p>`;
                    resumeHTML += `<p>${edu.university}, ${edu.year}</p>`;
                    resumeHTML += '</div>';
                });
                resumeHTML += '</div>';
            }

            resumeHTML += '</div>'; // close .left-column

            // Right Column
            resumeHTML += '<div class="right-column">';

            // Summary
            if (enhancedResumeData.summary) {
                resumeHTML += '<div class="summary-section">';
                resumeHTML += '<h2 class="section-title">Summary</h2>';
                resumeHTML += `<p class="summary-text">${enhancedResumeData.summary}</p>`;
                resumeHTML += '</div>';
            }

            // Experience (includes research positions)
            if (enhancedResumeData.experience && enhancedResumeData.experience.length > 0) {
                resumeHTML += '<div class="experience-section">';
                resumeHTML += '<h2 class="section-title">Experience</h2>';
                enhancedResumeData.experience.forEach(job => {
                    resumeHTML += '<div class="job">';
                    resumeHTML += `<h3 class="job-title">${job.title}</h3>`;
                    resumeHTML += `<p class="company-info">${job.company} | ${job.start_date} - ${job.end_date}</p>`;
                    resumeHTML += '<ul class="job-description">';
                    // 检查description是否为数组
                    if (Array.isArray(job.description)) {
                        job.description.forEach(point => {
                            resumeHTML += `<li>${point}</li>`;
                        });
                    } else if (job.description) {
                        // 如果description是字符串，直接显示
                        resumeHTML += `<li>${job.description}</li>`;
                    }
                    resumeHTML += '</ul>';
                    resumeHTML += '</div>';
                });
                resumeHTML += '</div>';
            }

            // Projects
            if (enhancedResumeData.projects && enhancedResumeData.projects.length > 0) {
                resumeHTML += '<div class="projects-section">';
                resumeHTML += '<h2 class="section-title">Projects</h2>';
                enhancedResumeData.projects.forEach(project => {
                    resumeHTML += '<div class="project">';
                    resumeHTML += `<h3 class="project-name">${project.name}</h3>`;
                    if (project.dates || project.date) {
                        resumeHTML += `<p class="project-date">${project.dates || project.date}</p>`;
                    }
                    resumeHTML += '<ul class="project-description">';
                    // 检查description是否为数组
                    if (Array.isArray(project.description)) {
                        project.description.forEach(point => {
                            resumeHTML += `<li>${point}</li>`;
                        });
                    } else if (project.description) {
                        // 如果description是字符串，直接显示
                        resumeHTML += `<li>${project.description}</li>`;
                    }
                    resumeHTML += '</ul>';
                    resumeHTML += '</div>';
                });
                resumeHTML += '</div>';
            }

            resumeHTML += '</div>'; // close .right-column

            resumeHTML += '</div>'; // close .resume

            enhancedResumeData.cleanHTML = resumeHTML; // Store clean HTML
            
            // 自动加载临时内容和预览
            loadTempContent();
            setTimeout(() => {
                syncTempToPreview();
            }, 500); // 稍微延迟以确保临时内容加载完成
            
            // 隐藏loading指示器，显示按钮
            const optimizeBtn = document.getElementById('optimize-btn');
            const loadingIndicator = document.getElementById('loading-indicator');
            loadingIndicator.style.display = 'none';
            optimizeBtn.style.display = 'inline-block';
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('Error optimizing resume. Please check the console for details.');
            
            // 出错时也要隐藏loading指示器，显示按钮
            const optimizeBtn = document.getElementById('optimize-btn');
            const loadingIndicator = document.getElementById('loading-indicator');
            loadingIndicator.style.display = 'none';
            optimizeBtn.style.display = 'inline-block';
        });
    });
}