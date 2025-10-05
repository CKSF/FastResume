// API配置
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000',
    ENDPOINTS: {
        UPLOAD: '/upload',
        DOWNLOAD: '/download',
        PREVIEW: '/api/preview-pdf',
        TEMP_DATA: '/api/temp-data'
    }
};

// 全局变量
let enhancedResumeData = null;
let syncTimeout = null;
let currentSessionId = null;