from setuptools import setup, find_packages

setup(
    name='mseep-mcp-godotrag',
    version='0.1.0',
    description='Add your description here',
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
    install_requires=['accelerate>=1.6.0', 'chromadb>=1.0.0', 'dotenv>=0.9.9', 'fastmcp>=0.4.1', 'httpx[socks]>=0.28.1', 'langchain>=0.3.23', 'mcp[cli]>=1.6.0', 'numpy>=2.2.4', 'openai>=1.70.0', 'pypandoc>=1.15', 'requests>=2.32.3', 'sentence-transformers>=4.0.2', 'socksio>=1.0.0', 'torch>=2.6.0', 'transformers>=4.51.0'],
    keywords=['mseep'],
)
