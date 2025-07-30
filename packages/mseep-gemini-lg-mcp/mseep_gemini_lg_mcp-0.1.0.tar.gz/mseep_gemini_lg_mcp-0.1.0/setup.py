from setuptools import setup, find_packages

setup(
    name='mseep-gemini-lg-mcp',
    version='0.1.0',
    description='Gemini-powered research agent MCP server',
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
    install_requires=['mcp[cli]>=1.0.0', 'google-genai>=0.3.0', 'langchain-google-genai>=2.0.0', 'langchain-core>=0.3.0', 'langchain>=0.3.0', 'langgraph>=0.2.0', 'pydantic>=2.0.0', 'python-dotenv>=1.0.0', 'requests>=2.31.0'],
    keywords=['mseep', 'mcp', 'gemini', 'research', 'ai', 'search'],
)
