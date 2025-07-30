# doc2txt

一个用于从Microsoft Word文档中提取文本的Python包，基于antiword工具构建，内置了跨平台的二进制文件和数据文件。

## 功能特性

- 从.doc格式的Microsoft Word文档中提取纯文本
- 跨平台支持（Windows、Linux、macOS ARM64）
- 内置antiword二进制文件，无需额外安装
- 文本格式优化功能，自动处理换行和表格
- 简单易用的Python API

## 支持的平台

- Windows (AMD64)
- Linux (AMD64)  
- macOS (ARM64/Apple Silicon)

> 注意：macOS Intel (x86_64) 暂不支持

## 安装

```bash
pip install doc2txt
```

## 快速开始

### 基本用法

```python
from doc2txt import extract_text

# 从Word文档提取文本
text = extract_text('document.doc')
print(text)
```

### 启用文本格式优化

```python
from doc2txt import extract_text

# 提取文本并优化格式（合并断行，处理表格）
text = extract_text('document.doc', optimize_format=True)
print(text)
```

### 使用文本优化工具

```python
from doc2txt import extract_text, optimize_text

# 先提取原始文本
raw_text = extract_text('document.doc')

# 手动优化文本格式
optimized_text = optimize_text(raw_text)
print(optimized_text)
```

## API 参考

### extract_text(doc_path, optimize_format=False)

从Microsoft Word文档中提取文本。

**参数:**
- `doc_path` (str): .doc文件的路径
- `optimize_format` (bool): 是否优化文本格式，默认为False

**返回:**
- `str`: 从文档中提取的文本内容

**异常:**
- `RuntimeError`: 平台不支持或二进制文件缺失
- `subprocess.CalledProcessError`: antiword执行失败

### optimize_text(text)

优化从文档中提取的文本格式。

**参数:**
- `text` (str): 从文档中提取的原始文本

**返回:**
- `str`: 格式优化后的文本

## 文本优化功能

文本优化功能解决了从Word文档提取文本时常见的格式问题：

- **换行合并**: 自动合并没有缩进的连续行，保持段落的完整性
- **表格处理**: 智能识别表格行（包含`|`分隔符），保持表格格式
- **空格处理**: 移除行首多余空格，保持文档的清洁格式

## 项目结构

```
doc2txt/
├── __init__.py              # 包的主入口
├── antiword_wrapper.py      # antiword工具的Python封装
├── text_optimizer.py       # 文本格式优化工具
├── bin/                     # 跨平台二进制文件
│   ├── darwin-arm64/
│   ├── linux-amd64/
│   └── win-amd64/
└── antiword_share/          # antiword数据文件
    ├── fontnames
    └── *.txt                # 字符编码映射文件
```

## 依赖要求

本包无外部依赖，所有必需的工具和数据文件都已内置。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 更新日志

### 1.0.0
- 初始版本发布
- 支持从.doc文件提取文本
- 内置跨平台antiword二进制文件
- 文本格式优化功能