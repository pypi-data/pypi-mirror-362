from setuptools import setup, find_packages

setup(
    name='mseep-ultimate_mcp_server',
    version='0.1.0',
    description='The Ultimate Model Context Protocol (MCP) Server, providing unified access to a wide variety of useful and powerful tools.',
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
    install_requires=['mcp>=0', 'anthropic>=0', 'openai>=0', 'google-genai>=0', 'httpx>=0', 'aiofiles>=0', 'pydantic>=0', 'tenacity>=0', 'diskcache>=0', 'msgpack>=0', 'numpy>=0', 'sentence-transformers>=0', 'chromadb>=0', 'prometheus-client>=0', 'pandas>=0', 'rich>=0', 'jinja2>=0', 'pillow>=0', 'python-slugify>=0', 'colorama>=0', 'tqdm>=0', 'tiktoken>=0', 'python-decouple>=0', 'pydantic-settings>=0', 'jsonschema>=0', 'matplotlib>=0', 'marqo>=0', 'pytest-playwright>=0', 'sqlalchemy>=0', 'aiosqlite>=0', 'pyvis>=0', 'python-docx>=0', 'opencv-python>=0', 'pytesseract>=0', 'pdf2image>=0', 'PyPDF2>=0', 'pdfplumber>=0', 'fitz>=0', 'pymupdf>=0', 'beautifulsoup4>=0', 'xmldiff>=0', 'lxml>=0', 'faster-whisper>=0', 'html2text>=0', 'readability-lxml>=0', 'markdownify>=0', 'trafilatura>=0', 'markdown>=0', 'jsonpatch>=0', 'jsonpointer>=0', 'pygments>=0', 'typer>=0', 'docling>=0', 'aiohttp>=0', 'boto3>=0', 'hvac>=0', 'pandera>=0', 'rapidfuzz>=0', 'magika>=0', 'tabula-py>=0', 'brotli>=0', 'pygments>=0', 'fastapi>=0.115.9', 'uvicorn>=0.34.2', 'networkx>0', 'scipy>0', 'fastmcp>0'],
    keywords=['mseep', 'ultimte', 'mcp', 'server', 'agent', 'ai', 'claude', 'gpt', 'gemini', 'deepseek'],
)
