from setuptools import setup, find_packages

setup(
    name="mseep-claude-desktop-memory-bank",
    
    long_description="Package managed by MseeP.ai",
    long_description_content_type="text/plain",version="0.1.0",
    description="Memory Bank MCP Server for Claude Desktop",
    author="mseep",
    packages=find_packages(),
    install_requires=[
        "mcp==1.6.0",
        "httpx>=0.20.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "memory-bank-server=memory_bank_server:main",
        ],
    },
    python_requires='>=3.8',
)
