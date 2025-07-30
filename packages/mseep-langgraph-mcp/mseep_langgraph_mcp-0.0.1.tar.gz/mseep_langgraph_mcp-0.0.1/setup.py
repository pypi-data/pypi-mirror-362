from setuptools import setup, find_packages

setup(
    name='mseep-langgraph-mcp',
    version='0.0.1',
    description='LangGraph solution template for MCP',
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
    install_requires=['asyncio>=3.4.3', 'langchain>=0.2.17', 'langchain-core>=0.3.21', 'langchain-milvus>=0.1.7', 'langchain-openai>=0.2.11', 'langgraph>=0.2.56', 'mcp>=1.0.0', 'openai>=1.57.0', 'python-dotenv>=1.0.1'],
    keywords=['mseep'],
)
