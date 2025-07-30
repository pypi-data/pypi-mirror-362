from setuptools import setup, find_packages

setup(
    name='mseep-mcp-simple-tool',
    version='1.2.0',
    description='MCP工具集合，包含文件处理和网页获取功能',
    long_description="Package managed by MseeP.ai",
    long_description_content_type="text/plain",
    author='mseep',
    author_email='support@skydeck.ai',
    maintainer='mseep',
    maintainer_email='support@skydeck.ai',
    url='https://github.com/mseep',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['anyio>=4.5', 'click>=8.1.0', 'httpx>=0.27', 'mcp', 'PyPDF2>=3.0.0', 'pdf2image>=1.16.0', 'Pillow>=10.0.0', 'pymupdf4llm==0.0.17', 'PyMuPDF>=1.22.0', 'python-docx>=0.8.11', 'pandas>=2.0.0', 'openpyxl>=3.1.0', 'pytesseract>=0.3.10', 'chardet>=5.0.0'],
    keywords=['mseep', 'mcp', 'llm', 'automation', 'web', 'fetch', 'pdf', 'word', 'excel', 'csv'],
)
