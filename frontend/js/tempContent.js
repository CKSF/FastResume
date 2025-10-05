// 临时内容管理模块

function loadTempContent() {
    if (!currentSessionId) {
        currentSessionId = generateSessionId();
    }

    if (!enhancedResumeData) {
        alert("请先生成简历内容");
        return;
    }

    // 显示当前的结构化数据
    displayTempContent(enhancedResumeData);
}

function displayTempContent(data) {
    const container = document.getElementById('temp-content-sections');
    container.innerHTML = '';

    // 为每个section创建可编辑区域
    const sections = ['summary', 'experience', 'projects', 'education', 'skills', 'publications'];
    
    sections.forEach(sectionName => {
        if (data[sectionName]) {
            const sectionDiv = document.createElement('div');
            sectionDiv.style.marginBottom = '15px';
            sectionDiv.style.padding = '10px';
            sectionDiv.style.border = '1px solid #eee';
            sectionDiv.style.borderRadius = '5px';

            const title = document.createElement('h4');
            title.textContent = sectionName.charAt(0).toUpperCase() + sectionName.slice(1);
            title.style.margin = '0 0 10px 0';
            title.style.color = '#333';
            sectionDiv.appendChild(title);

            if (typeof data[sectionName] === 'string') {
                // 简单文本内容 (如 summary)
                const textarea = document.createElement('textarea');
                textarea.value = data[sectionName];
                textarea.style.width = '100%';
                textarea.style.minHeight = '60px';
                textarea.style.border = '1px solid #ccc';
                textarea.style.borderRadius = '3px';
                textarea.style.padding = '5px';
                textarea.dataset.section = sectionName;
                sectionDiv.appendChild(textarea);
            } else if (Array.isArray(data[sectionName])) {
                // 数组内容 (如 experience, projects)
                data[sectionName].forEach((item, index) => {
                    const itemDiv = document.createElement('div');
                    itemDiv.style.marginBottom = '10px';
                    itemDiv.style.padding = '8px';
                    itemDiv.style.backgroundColor = '#f8f9fa';
                    itemDiv.style.borderRadius = '3px';

                    if (typeof item === 'string') {
                        const textarea = document.createElement('textarea');
                        textarea.value = item;
                        textarea.style.width = '100%';
                        textarea.style.minHeight = '40px';
                        textarea.style.border = '1px solid #ccc';
                        textarea.style.borderRadius = '3px';
                        textarea.style.padding = '5px';
                        textarea.dataset.section = sectionName;
                        textarea.dataset.index = index;
                        itemDiv.appendChild(textarea);
                    } else if (typeof item === 'object') {
                        // 对象类型的条目
                        Object.keys(item).forEach(key => {
                            const label = document.createElement('label');
                            label.textContent = key + ': ';
                            label.style.display = 'block';
                            label.style.marginBottom = '5px';
                            label.style.fontWeight = 'bold';
                            label.style.fontSize = '12px';

                            const input = document.createElement('textarea');
                            
                            // 特殊处理description数组字段
                            if (key === 'description' && Array.isArray(item[key])) {
                                input.value = item[key].join('\n• ');
                                if (input.value && !input.value.startsWith('• ')) {
                                    input.value = '• ' + input.value;
                                }
                            } else {
                                input.value = item[key] || '';
                            }
                            
                            input.style.width = '100%';
                            input.style.minHeight = '60px';
                            input.style.border = '1px solid #ccc';
                            input.style.borderRadius = '3px';
                            input.style.padding = '3px';
                            input.dataset.section = sectionName;
                            input.dataset.index = index;
                            input.dataset.key = key;

                            itemDiv.appendChild(label);
                            itemDiv.appendChild(input);
                        });
                    }

                    sectionDiv.appendChild(itemDiv);
                });
            }

            container.appendChild(sectionDiv);
        }
    });
}

function saveTempContent() {
    if (!currentSessionId) {
        alert("没有活动的会话");
        return;
    }

    // 收集所有编辑的内容
    const updatedData = { ...enhancedResumeData };
    const container = document.getElementById('temp-content-sections');
    
    // 收集简单文本字段
    container.querySelectorAll('textarea[data-section]').forEach(textarea => {
        const section = textarea.dataset.section;
        const index = textarea.dataset.index;
        const key = textarea.dataset.key;

        if (index !== undefined && key !== undefined) {
            // 对象数组中的字段
            if (!updatedData[section][index]) {
                updatedData[section][index] = {};
            }
            
            // 特殊处理description字段，将文本转换回数组
            if (key === 'description') {
                const descriptionText = textarea.value.trim();
                if (descriptionText) {
                    // 按行分割，并清理bullet points
                    updatedData[section][index][key] = descriptionText
                        .split('\n')
                        .map(line => line.trim())
                        .filter(line => line.length > 0)
                        .map(line => line.replace(/^[•\-*◦]\s*/, ''));
                } else {
                    updatedData[section][index][key] = [];
                }
            } else {
                updatedData[section][index][key] = textarea.value;
            }
        } else if (index !== undefined) {
            // 简单数组中的项目
            updatedData[section][index] = textarea.value;
        } else {
            // 简单字符串字段
            updatedData[section] = textarea.value;
        }
    });

    // 保存到后端
    fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.TEMP_DATA}/${currentSessionId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            enhancedResumeData = updatedData; // 更新本地数据
            // 静默保存成功，自动刷新预览
            syncTempToPreview();
        } else {
            console.error("保存失败:", data.error || "未知错误");
        }
    })
    .catch(error => {
        console.error('Error saving temp content:', error);
    });
}

function syncTempToPreview() {
    if (!enhancedResumeData) {
        alert("没有可同步的内容");
        return;
    }

    // 收集当前编辑器中的内容更新到 enhancedResumeData
    const container = document.getElementById('temp-content-sections');
    if (container && container.children.length > 0) {
        // 如果有编辑器内容，先更新数据
        const updatedData = { ...enhancedResumeData };
        
        container.querySelectorAll('textarea[data-section]').forEach(textarea => {
            const section = textarea.dataset.section;
            const index = textarea.dataset.index;
            const key = textarea.dataset.key;

            if (index !== undefined && key !== undefined) {
                // 对象数组中的字段
                if (!updatedData[section][index]) {
                    updatedData[section][index] = {};
                }
                
                // 特殊处理description字段，将文本转换回数组
                if (key === 'description') {
                    const descriptionText = textarea.value.trim();
                    if (descriptionText) {
                        updatedData[section][index][key] = descriptionText
                            .split('\n')
                            .map(line => line.trim())
                            .filter(line => line.length > 0)
                            .map(line => line.replace(/^[•\-*◦]\s*/, ''));
                    } else {
                        updatedData[section][index][key] = [];
                    }
                } else {
                    updatedData[section][index][key] = textarea.value;
                }
            } else if (index !== undefined) {
                // 简单数组中的项目
                updatedData[section][index] = textarea.value;
            } else {
                // 简单字符串字段
                updatedData[section] = textarea.value;
            }
        });
        
        // 更新全局数据
        enhancedResumeData = updatedData;
    }

    // 获取当前的section顺序并更新到enhancedResumeData
    const currentSectionOrder = getSectionOrder();
    enhancedResumeData.section_order = currentSectionOrder;

    // 保存更新后的数据到临时文件
    if (currentSessionId) {
        const updatedDataForSave = { ...enhancedResumeData };
        
        fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.TEMP_DATA}/${currentSessionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedDataForSave)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 静默保存成功后，触发预览更新
                document.getElementById('preview-btn').click();
            } else {
                console.error("同步临时数据失败:", data.error || "未知错误");
                // 即使保存失败，也尝试更新预览
                document.getElementById('preview-btn').click();
            }
        })
        .catch(error => {
            console.error('Error syncing temp data:', error);
            // 即使保存失败，也尝试更新预览
            document.getElementById('preview-btn').click();
        });
    } else {
        // 没有session ID，直接触发预览
        document.getElementById('preview-btn').click();
    }
}

// 初始化临时内容编辑器的事件监听器
function initTempContentEditor() {
    // 保存按钮事件监听器
    const saveTempBtn = document.getElementById('save-temp-btn');
    if (saveTempBtn) {
        saveTempBtn.addEventListener('click', function() {
            saveTempContent();
        });
    }
}