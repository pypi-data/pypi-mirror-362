from setuptools import setup, find_packages

setup(
    name='mseep-jenkins-mcp-enterprise',
    version='1.0.0',
    description='MCP server for Jenkins integration with AI assistants, providing build management, log analysis, and failure diagnostics.',
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
    install_requires=['python-jenkins>=1.8.2', 'requests>=2.31.0', 'sentence-transformers>=2.2.0', 'qdrant-client>=1.14.3', 'tiktoken>=0.5.0', 'APScheduler>=3.11.0', 'modelcontextprotocol>=0.1.0', 'fastapi>=0.100.0', 'uvicorn>=0.23.0', 'httpx>=0.24.0', 'websockets>=11.0', 'sse-starlette>=1.6.0', 'pyyaml>=6.0'],
    keywords=['mseep', 'jenkins', 'mcp', 'ai', 'devops', 'model-context-protocol'],
)
