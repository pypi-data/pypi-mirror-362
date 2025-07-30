from setuptools import setup, find_packages

setup(
    name='mseep-mcp-server-hubspot',
    version='0.2.0',
    description='A simple Hubspot MCP server',
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
    install_requires=['mcp>=1.4.1', 'hubspot-api-client>=11.1.0', 'python-dotenv>=1.0.1', 'faiss-cpu>=1.7.4', 'numpy>=1.24.0', 'sentence-transformers>=2.2.2', 'huggingface-hub==0.14.1'],
    keywords=['mseep'],
)
