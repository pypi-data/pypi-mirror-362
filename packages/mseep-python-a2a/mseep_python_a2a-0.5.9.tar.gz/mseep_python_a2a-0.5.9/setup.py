from setuptools import setup, find_packages

setup(
    name='mseep-python-a2a',
    version='0.5.9',
    description="A comprehensive Python library for Google's Agent-to-Agent (A2A) protocol",
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
    install_requires=['requests>=2.25.0', 'flask>=2.0.0', 'aiohttp>=3.8.0', 'openai>=1.0.0', 'anthropic>=0.3.0', 'boto3>=1.26.0', 'botocore>=1.29.0', 'httpx>=0.23.0', 'fastapi>=0.95.0', 'uvicorn>=0.21.0', 'pydantic>=1.10.7', 'langchain>=0.1.0'],
    keywords=['mseep', 'a2a', 'agent', 'ai', 'llm', 'interoperability', 'google', 'protocol', 'chatbot', 'openai', 'anthropic', 'claude', 'huggingface', 'mcp', 'model-context-protocol', 'aws-bedrock', 'langchain'],
)
