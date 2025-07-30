from setuptools import setup, find_packages

setup(
    name='mseep-zen-mcp-server',
    version='0.1.0',
    description='AI-powered MCP server with multiple model providers',
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
    install_requires=['mcp>=1.0.0', 'google-genai>=1.19.0', 'openai>=1.55.2', 'pydantic>=2.0.0', 'python-dotenv>=1.0.0'],
    keywords=['mseep'],
)
