from setuptools import setup, find_packages

setup(
    name='mseep-python-mcp',
    version='0.1.0',
    description='A working example to create a FastAPI server with SSE-based MCP support',
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
    install_requires=['cmake>=4.0.0', 'fastapi>=0.115.12', 'mcp[cli]>=1.6.0', 'uvicorn>=0.34.2'],
    keywords=['mseep'],
)
