from setuptools import setup, find_packages

setup(
    name='mseep-mcp-proxy',
    version='0.8.2',
    description='A MCP server which proxies requests to a remote MCP server over SSE transport.',
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
    install_requires=['mcp>=1.8.0,<2.0.0', 'uvicorn>=0.34.0'],
    keywords=['mseep'],
)
