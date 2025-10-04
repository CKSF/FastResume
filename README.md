# GenResume - AI驱动的简历优化工具 🚀

GenResume是一个基于人工智能的简历优化平台，能够根据职位描述智能优化简历内容，提供专业的PDF输出和实时预览功能。

## 🏗️ 项目架构

采用前后端分离架构，结合现代AI技术栈：

```
GenResume/
├── backend/          # Python Flask后端
│   ├── app.py           # 主应用程序
│   ├── dynamic_parser.py # AI简历解析器
│   ├── enhancer.py      # AI内容增强器
│   ├── file_parser.py   # 文件解析器
│   ├── jd_parser.py     # 职位描述解析器
│   ├── pdf_generator.py # PDF生成器
│   └── templates/       # HTML模板
├── frontend/         # HTML/JS前端
├── test/            # 测试模块
│   ├── test_llm.py     # API功能测试
│   └── monitor.py      # 系统监控测试
└── .venv/           # Python虚拟环境
```

## 🔧 技术栈

### 🐍 后端技术栈
- **Flask 3.1.2** - Web框架
- **Google Generative AI (Gemini 2.0)** - 核心AI引擎
- **NLTK 3.9.2** - 自然语言处理
- **WeasyPrint 66.0** - HTML到PDF转换
- **PyPDF2 3.0.1** - PDF文件解析
- **python-docx 1.2.0** - Word文档处理

### 🌐 前端技术栈
- **HTML5/CSS3** - 页面结构和样式
- **Vanilla JavaScript** - 交互逻辑
- **Quill.js 1.3.6** - 富文本编辑器

## 🚀 核心功能

### 1. 智能文件解析
- **支持格式**: PDF、Word (.docx)、纯文本 (.txt)
- **多格式兼容**: 自动识别文件类型并提取内容
- **编码处理**: 智能处理UTF-8和Latin-1编码

### 2. AI驱动的简历解析
- **结构化提取**: 使用Gemini 2.0将非结构化简历转换为JSON格式
- **智能识别**: 自动提取个人信息、工作经历、教育背景、项目经验、技能、研究经历
- **研究经历解析**: 新增对学术研究经历的智能识别，包括实验室、机构信息
- **数据标准化**: 统一数据格式，便于后续处理

### 3. 职位描述分析
- **关键词提取**: 使用NLTK进行智能关键词提取
- **词性分析**: 重点提取名词和形容词
- **频率统计**: 返回最相关的15个关键词

### 4. AI内容增强
- **个性化优化**: 基于职位描述重写简历内容
- **保持结构**: 维持原有JSON数据结构
- **智能匹配**: 突出与职位相关的技能和经验
- **研究经验整合**: 自动将研究经历合并到工作经验中，统一展示格式
- **字段映射优化**: 智能处理实验室/机构名称到公司字段的映射

### 5. 专业PDF生成
- **模板系统**: 使用Jinja2模板引擎
- **专业排版**: 精确控制字体、间距、布局
- **打印优化**: 适配标准8.5英寸页面

## 📡 API接口

### 核心端点

#### `POST /upload`
上传简历和职位描述进行AI优化
- **输入**: `multipart/form-data`
  - `job_description`: 职位描述文本
  - `resume`: 简历文件 (PDF/DOCX/TXT)
- **输出**: JSON格式的增强简历数据

#### `POST /download`
生成并下载优化后的PDF简历
- **输入**: JSON对象
  - `html_content`: HTML格式的简历内容
  - `template`: 模板名称
- **输出**: PDF文件下载

#### `POST /api/preview-pdf`
实时PDF预览功能
- **输入**: 同download接口
- **输出**: PDF预览流

#### `GET /`
前端页面服务
- **输出**: 主页面HTML

## 🎨 模板系统

### 专业简历模板
- **现代设计**: 使用Calibri/Arial字体
- **响应式布局**: 适配不同屏幕尺寸
- **打印友好**: 优化的PDF输出效果
- **可扩展**: 支持多模板切换

### 样式特性
- 精确的排版控制
- 专业的视觉层次
- 清晰的信息结构
- 一致的设计风格

## 🔒 安全特性

- **PII保护**: 自动保护个人身份信息
- **临时文件管理**: 自动清理生成的临时文件
- **错误处理**: 完善的异常处理机制
- **日志记录**: 详细的操作日志

## 🛠️ 安装和运行

### 环境要求
- Python 3.12+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd GenResume
```

2. **创建虚拟环境**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置API密钥**
在 `dynamic_parser.py` 和 `enhancer.py` 中配置Google AI API密钥

5. **运行应用**
```bash
cd backend
python app.py
```

6. **访问应用**
打开浏览器访问 `http://localhost:5000`

## 🧪 测试

### 测试文件
- `test/test_llm.py`: API端点功能测试
- `test/monitor.py`: 内容验证和系统监控

### 运行测试
```bash
python test/test_llm.py
python test/monitor.py
```

## 📁 项目结构详解

### 后端模块

#### `app.py` - 主应用程序
Flask应用的核心，处理所有HTTP请求和响应

#### `dynamic_parser.py` - AI简历解析器
使用Google Gemini AI将非结构化简历文本转换为结构化JSON数据

#### `enhancer.py` - AI内容增强器
基于职位描述使用AI优化简历内容，提高匹配度

#### `file_parser.py` - 文件解析器
支持多种文件格式的文本提取功能

#### `jd_parser.py` - 职位描述解析器
使用NLTK进行自然语言处理，提取关键词

#### `pdf_generator.py` - PDF生成器
使用WeasyPrint将HTML模板转换为专业PDF文档

### 前端组件

#### `frontend/index.html` - 用户界面
- 文件上传界面
- 富文本编辑器
- 实时PDF预览
- 模板选择器

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 🔮 未来规划

- [ ] 支持更多简历模板
- [ ] 添加多语言支持
- [ ] 集成更多AI模型
- [ ] 移动端适配
- [ ] 批量处理功能
- [x] 研究经历智能解析和整合
- [x] AI解析器字段映射优化

---

**GenResume** - 让AI为你的职业生涯加速！ 🎯

## 📝 更新日志

### v1.2.0 (最新)
- ✅ **新增研究经历解析**: AI现在能够智能识别和解析学术研究经历
- ✅ **研究经验整合**: 自动将研究经历合并到工作经验中，统一展示
- ✅ **字段映射优化**: 改进实验室/机构名称到公司字段的智能映射
- ✅ **AI解析增强**: 优化prompt以更好地提取研究相关信息
- ✅ **测试模块重组**: 将测试文件整理到独立的test文件夹

### v1.1.0
- ✅ **AI驱动解析**: 集成Google Gemini 2.0进行智能简历解析
- ✅ **多格式支持**: 支持PDF、Word、TXT格式简历上传
- ✅ **实时PDF预览**: 提供即时的PDF预览功能
- ✅ **专业模板**: 实现现代化的简历模板系统