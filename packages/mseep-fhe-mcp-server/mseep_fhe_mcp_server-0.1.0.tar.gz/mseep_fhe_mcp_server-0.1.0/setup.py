from setuptools import setup, find_packages

setup(
    name='mseep-fhe-mcp-server',
    version='0.1.0',
    description='FHE MCP Server',
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
    install_requires=['concrete-ml==1.9.0', 'fastapi>=0.115.12', 'mcp[cli]>=1.6.0', 'numpy>=1.26.4', 'pillow>=11.2.1', 'python-multipart>=0.0.20', 'setuptools==75.3.0', 'uvicorn>=0.34.2', 'wheel>=0.45.1'],
    keywords=['mseep'],
)
