from setuptools import setup, find_packages

setup(
    name='mseep-mcp-code-checker',
    version='0.1.0',
    description='An MCP server for running code checks (pylint and pytest)',
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
    install_requires=['pathspec>=0.12.1', 'mcp>=1.3.0', 'mcp[server]>=1.3.0', 'mcp[cli]>=1.3.0', 'pylint>=3.3.3', 'pytest>=8.3.5', 'pytest-json-report>=1.5.0', 'pytest-asyncio>=0.25.3', 'mypy>=1.9.0'],
    keywords=['mseep', 'mcp', 'server', 'code-checker', 'pylint', 'pytest', 'claude', 'ai', 'assistant'],
)
