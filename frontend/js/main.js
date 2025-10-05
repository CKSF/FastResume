// 主初始化模块

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有模块
    initResumeGeneration();
    initPreviewAndDownload();
    initSectionDragAndDrop();
    addSectionToggleListeners();
    initTempContentEditor(); // 初始化临时内容编辑器
    
    // 自动加载临时内容（如果存在）
    loadTempContent();
});