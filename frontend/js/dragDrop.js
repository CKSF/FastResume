// 拖拽排序功能模块

function initSectionDragAndDrop() {
    const sectionOrderList = document.getElementById('section-order-list');
    let draggedElement = null;
    let dropIndicator = null;
    
    // 创建拖拽指示器
    function createDropIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'drop-indicator';
        return indicator;
    }
    
    // 为每个可拖拽项添加事件监听器
    sectionOrderList.addEventListener('dragstart', function(e) {
        draggedElement = e.target.closest('li');
        if (draggedElement) {
            draggedElement.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', draggedElement.outerHTML);
        }
    });
    
    sectionOrderList.addEventListener('dragend', function(e) {
        if (draggedElement) {
            draggedElement.classList.remove('dragging');
            draggedElement = null;
        }
        // 清理所有拖拽相关的样式
        document.querySelectorAll('.section-item').forEach(item => {
            item.classList.remove('drag-over');
        });
        // 移除拖拽指示器
        if (dropIndicator && dropIndicator.parentNode) {
            dropIndicator.parentNode.removeChild(dropIndicator);
            dropIndicator = null;
        }
    });
    
    sectionOrderList.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        
        const targetElement = e.target.closest('li');
        if (targetElement && targetElement !== draggedElement) {
            // 清理之前的样式
            document.querySelectorAll('.section-item').forEach(item => {
                item.classList.remove('drag-over');
            });
            
            // 添加拖拽悬停样式
            targetElement.classList.add('drag-over');
            
            // 显示拖拽指示器
            if (!dropIndicator) {
                dropIndicator = createDropIndicator();
            }
            
            const rect = targetElement.getBoundingClientRect();
            const midpoint = rect.top + rect.height / 2;
            
            if (e.clientY < midpoint) {
                sectionOrderList.insertBefore(dropIndicator, targetElement);
            } else {
                sectionOrderList.insertBefore(dropIndicator, targetElement.nextSibling);
            }
            
            dropIndicator.classList.add('active');
        }
    });
    
    sectionOrderList.addEventListener('drop', function(e) {
        e.preventDefault();
        const targetElement = e.target.closest('li');
        
        if (targetElement && draggedElement && targetElement !== draggedElement) {
            const rect = targetElement.getBoundingClientRect();
            const midpoint = rect.top + rect.height / 2;
            
            if (e.clientY < midpoint) {
                sectionOrderList.insertBefore(draggedElement, targetElement);
            } else {
                sectionOrderList.insertBefore(draggedElement, targetElement.nextSibling);
            }
            
            // 拖拽完成后立即更新PDF预览
            if (enhancedResumeData) {
                clearTimeout(syncTimeout);
                syncTempToPreview(); // 同步到预览
            }
        }
        
        // 清理拖拽状态
        document.querySelectorAll('.section-item').forEach(item => {
            item.classList.remove('drag-over');
        });
        if (dropIndicator && dropIndicator.parentNode) {
            dropIndicator.parentNode.removeChild(dropIndicator);
            dropIndicator = null;
        }
    });
    
    // 阻止checkbox点击时触发拖拽
    sectionOrderList.addEventListener('mousedown', function(e) {
        if (e.target.type === 'checkbox') {
            e.stopPropagation();
        }
    });
}

// 监听section开关变化
function addSectionToggleListeners() {
    // 监听拖拽列表中的checkbox变化
    const sectionOrderList = document.getElementById('section-order-list');
    if (sectionOrderList) {
        sectionOrderList.addEventListener('change', function(e) {
            if (e.target.type === 'checkbox' && enhancedResumeData) {
                console.log('Checkbox changed:', e.target.id, 'checked:', e.target.checked);
                // 立即同步PDF预览
                clearTimeout(syncTimeout);
                syncTempToPreview(); // 同步到预览
            }
        });
    }
    
    // 注意：不再添加独立的checkbox监听器，因为所有checkbox都在section-order-list中
    // 这样可以避免重复触发预览更新
}