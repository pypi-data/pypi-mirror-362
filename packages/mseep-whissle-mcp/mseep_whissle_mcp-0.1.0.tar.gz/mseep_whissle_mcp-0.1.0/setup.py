from setuptools import setup, find_packages

setup(
    name='mseep-whissle-mcp',
    version='0.1.0',
    description='Whissle MCP Server',
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
    install_requires=['mcp[cli]>=1.6.0', 'fastapi==0.109.2', 'uvicorn==0.27.1', 'python-dotenv==1.0.1', 'pydantic>=2.6.1', 'httpx==0.28.1', 'whissle>=0.0.1'],
    keywords=['mseep', 'whissle', 'mcp', 'speech-to-text', 'translation', 'summarization'],
)
