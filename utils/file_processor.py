from config import Settings
import io
import re
from typing import List, Dict, Any
from docx import Document
import PyPDF2

"""Description
Supports txt,md,pdf,docs files processing(discard picture)
Provide large text chunks, func "split_to_chunks"
chunk_size ref to "config/settings.py"

Date: 2026-5-25
Created by oldmerman
"""

def extract_text_from_docx(file_bytes: bytes) -> str:
    """从 docx 提取纯文本"""
    doc = Document(io.BytesIO(file_bytes))
    texts = []
    for para in doc.paragraphs:
        if para.text.strip():
            texts.append(para.text)
    return '\n'.join(texts)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """从 pdf 提取纯文本"""
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            texts.append(text)
    return '\n'.join(texts)

def extract_text_from_txt(file_bytes: bytes) -> str:
    """从 txt 提取文本"""
    return file_bytes.decode('utf-8', errors='ignore')

def extract_text_from_md(file_bytes: bytes, remove_images: bool = True) -> str:
    """从 md 提取文本，可选删除图片语法"""
    text = file_bytes.decode('utf-8', errors='ignore')
    if remove_images:
        # 删除 ![alt](url)
        pattern = r'!\[.*?\]\(.*?\)'
        text = re.sub(pattern, '', text)
    return text

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    根据文件类型提取纯文本
    """
    filename_lower = filename.lower()

    if filename_lower.endswith('.txt'):
        return extract_text_from_txt(file_bytes)
    elif filename_lower.endswith('.md'):
        return extract_text_from_md(file_bytes, remove_images=True)
    elif filename_lower.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    elif filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    else:
        raise ValueError(f"不支持的文件类型: {filename}")

def split_to_chunks(file_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    将文件切成 50KB 的块（先提取文本，再按字节切）

    Args:
        file_bytes: 原始文件内容
        filename: 文件名

    Returns:
        块列表，每个块包含 bytes 内容和元数据
    """
    CHUNK_SIZE = Settings.MAX_CHUNK_SIZE  # 50KB

    # 1. 提取纯文本
    text = extract_text(file_bytes, filename)

    # 2. 编码回 bytes（纯文本，体积已减小）
    text_bytes = text.encode('utf-8')

    # 3. 切成 50KB 块
    chunks = []
    total_size = len(text_bytes)

    for i in range(0, total_size, CHUNK_SIZE):
        chunk_bytes = text_bytes[i:i + CHUNK_SIZE]
        chunk_text = chunk_bytes.decode('utf-8', errors='ignore')

        chunks.append({
            "text": chunk_text,  # 字符串格式（方便使用）
            "name": f"{filename}_part_{i // CHUNK_SIZE + 1:03d}",
            "original_name": filename,
        })

    return chunks

if __name__ == "__main__":
    with open(r"C:\Users\asus\Desktop\博客部署\文章\合集之LangChain\agent模块之记忆系统\agent模块之记忆系统.md",
              'rb') as file:
        content = file.read()
        print(extract_text(content, "agent模块之记忆系统.md"))