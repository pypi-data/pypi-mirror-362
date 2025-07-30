from setuptools import setup, find_packages

setup(
    name='mseep-mcp-feedback-enhanced',
    version='2.6.0',
    description='Enhanced MCP server for interactive user feedback and command execution in AI-assisted development, featuring dual interface support (Web UI and Desktop Application) with intelligent environment de...',
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
    install_requires=['fastmcp>=2.0.0', 'psutil>=7.0.0', 'fastapi>=0.115.0', 'uvicorn>=0.30.0', 'jinja2>=3.1.0', 'websockets>=13.0.0', 'aiohttp>=3.8.0', 'mcp>=1.9.3'],
    keywords=['mseep', 'mcp', 'ai', 'feedback', 'web-ui', 'desktop-app', 'interactive', 'development', 'cross-platform', 'tauri', 'dual-interface'],
)
