from setuptools import setup, find_packages

setup(
    name='mseep-docling-mcp',
    version='0.4.0',
    description='Running Docling as an agent using tools',
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
    install_requires=['docling~=2.25', 'httpx>=0.28.1', 'llama-index>=0.12.33', 'llama-index-core>=0.12.28', 'llama-index-embeddings-huggingface>=0.5.2', 'llama-index-embeddings-openai>=0.3.1', 'llama-index-llms-ollama>=0.5.4', 'llama-index-node-parser-docling>=0.3.1', 'llama-index-readers-docling>=0.3.2', 'llama-index-readers-file>=0.4.7', 'llama-index-vector-stores-milvus>=0.7.2', 'mcp[cli]>=1.9.4', 'pydantic~=2.10', 'pydantic-settings~=2.4', 'python-dotenv>=1.1.0'],
    keywords=['mseep', 'mcp', 'message control protocol', 'agents', 'agentic', 'AI', 'artificial intelligence', 'document understanding', 'RAG', 'Docling'],
)
