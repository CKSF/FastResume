// 工具函数模块

// 生成会话ID
function generateSessionId() {
    return Math.random().toString(36).substr(2, 9);
}

// 获取当前section顺序
function getSectionOrder() {
    const orderList = document.getElementById('section-order-list');
    const items = orderList.querySelectorAll('li[data-section]');
    return Array.from(items).map(item => item.getAttribute('data-section'));
}

// 智能解析编辑器内容的函数
function parseEditorContent(content) {
    const lines = content.split('\n').filter(line => line.trim());
    const parsedData = {};
    let currentSection = null;
    let currentItem = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // 识别section标题
        if (line.toLowerCase().includes('summary') || line.toLowerCase().includes('个人总结')) {
            currentSection = 'summary';
            continue;
        } else if (line.toLowerCase().includes('experience') || line.toLowerCase().includes('工作经历')) {
            currentSection = 'experience';
            parsedData.experience = [];
            currentItem = null;
            continue;
        } else if (line.toLowerCase().includes('projects') || line.toLowerCase().includes('项目经历')) {
            currentSection = 'projects';
            parsedData.projects = [];
            currentItem = null;
            continue;
        } else if (line.toLowerCase().includes('education') || line.toLowerCase().includes('教育背景')) {
            currentSection = 'education';
            parsedData.education = [];
            currentItem = null;
            continue;
        } else if (line.toLowerCase().includes('skills') || line.toLowerCase().includes('技能专长')) {
            currentSection = 'skills';
            parsedData.skills = [];
            currentItem = null;
            continue;
        } else if (line.toLowerCase().includes('publications') || line.toLowerCase().includes('发表论文')) {
            currentSection = 'publications';
            parsedData.publications = [];
            currentItem = null;
            continue;
        }
        
        // 根据当前section处理内容
        if (currentSection === 'summary') {
            if (!parsedData.summary) parsedData.summary = '';
            parsedData.summary += (parsedData.summary ? ' ' : '') + line;
        } else if (currentSection === 'experience') {
            // 检测日期格式 (如 "Sep 2024 – Present", "Jan 2024 – Jan 2025")
            const datePattern = /\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})\s*[–-]\s*(Present|\d{4}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i;
            
            if (datePattern.test(line)) {
                // 这是日期行，应该属于当前项目
                if (currentItem) {
                    const dates = line.split(/[–-]/).map(d => d.trim());
                    currentItem.start_date = dates[0] || '';
                    currentItem.end_date = dates[1] || '';
                }
            } else if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*') || line.startsWith('◦')) {
                // 这是描述项
                if (currentItem) {
                    currentItem.description.push(line.replace(/^[•\-*◦]\s*/, ''));
                }
            } else if (line && !line.match(/^\s*$/)) {
                // 这可能是新的工作项目标题
                currentItem = {
                    company: line,
                    title: '',
                    start_date: '',
                    end_date: '',
                    description: []
                };
                parsedData.experience.push(currentItem);
            }
        } else if (currentSection === 'projects') {
            // 检测日期格式
            const datePattern = /\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})\s*[–-]\s*(Present|\d{4}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/i;
            
            if (datePattern.test(line)) {
                // 这是日期行
                if (currentItem) {
                    currentItem.date = line;
                    const dates = line.split(/[–-]/).map(d => d.trim());
                    currentItem.start_date = dates[0] || '';
                    currentItem.end_date = dates[1] || '';
                }
            } else if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*') || line.startsWith('◦')) {
                // 这是描述项
                if (currentItem) {
                    currentItem.description.push(line.replace(/^[•\-*◦]\s*/, ''));
                }
            } else if (line && !line.match(/^\s*$/)) {
                // 这可能是新的项目标题
                currentItem = {
                    name: line,
                    date: '',
                    start_date: '',
                    end_date: '',
                    description: []
                };
                parsedData.projects.push(currentItem);
            }
        } else if (currentSection === 'skills') {
            if (line.startsWith('•') || line.startsWith('-') || line.startsWith('*')) {
                parsedData.skills.push(line.substring(1).trim());
            } else if (line) {
                parsedData.skills.push(line);
            }
        }
    }
    
    return parsedData;
}