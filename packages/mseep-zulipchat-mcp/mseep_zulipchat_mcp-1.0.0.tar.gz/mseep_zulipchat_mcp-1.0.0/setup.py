from setuptools import setup, find_packages

setup(
    name='mseep-zulipchat-mcp',
    version='1.0.0',
    description='MCP server for Zulip Chat integration',
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
    install_requires=['mcp>=1.0.0', 'zulip>=0.9.0', 'pydantic>=2.0', 'httpx>=0.24.0'],
    keywords=['mseep', 'mcp', 'zulip', 'chat', 'ai', 'assistant'],
)
