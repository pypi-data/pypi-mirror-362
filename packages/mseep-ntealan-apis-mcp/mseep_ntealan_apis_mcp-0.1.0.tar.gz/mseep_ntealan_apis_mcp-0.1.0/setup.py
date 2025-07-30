from setuptools import setup, find_packages

setup(
    name='mseep-ntealan-apis-mcp',
    version='0.1.0',
    description='A modular, extensible MCP server for NTeALan REST API dictionaries and contributions. Provides a unified async interface for managing dictionary data, articles, and user contributions.',
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
    install_requires=['pydantic>=1.10.0', 'fastapi>=0.110.0', 'httpx>=0.27.0', 'aiofiles>=23.2.1', 'beautifulsoup4>=4.12.3', 'lxml>=5.4.0', 'fastmcp>=2.2.5', 'setuptools>=79.0.1', 'aiohttp>=3.11.18', 'python-dotenv>=1.1.0', 'aiodns>=3.2.0'],
    keywords=['mseep', 'fastmpc', 'ntealan', 'mcp', 'server', 'python', 'dictionary', 'lexicography', 'sse'],
)
