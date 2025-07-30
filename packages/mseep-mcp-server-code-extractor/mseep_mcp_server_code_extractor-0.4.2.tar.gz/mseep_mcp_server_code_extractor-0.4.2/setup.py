from setuptools import setup, find_packages

setup(
    name='mseep-mcp-server-code-extractor',
    version='0.4.2',
    description='A Model Context Protocol (MCP) server that provides precise code extraction tools using tree-sitter parsing',
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
    install_requires=['mcp>=1.11.0', 'tree-sitter-languages>=1.10.2', 'tree-sitter==0.21.3', 'requests>=2.31.0', 'cachetools>=5.3.0'],
    keywords=['mseep', 'mcp', 'model-context-protocol', 'code-extraction', 'tree-sitter', 'ai-tools'],
)
