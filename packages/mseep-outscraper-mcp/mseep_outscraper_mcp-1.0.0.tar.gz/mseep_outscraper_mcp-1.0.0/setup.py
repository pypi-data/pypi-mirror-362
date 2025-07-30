from setuptools import setup, find_packages

setup(
    name='mseep-outscraper-mcp',
    version='1.0.0',
    description="Streamlined MCP server for Outscraper's Google Maps data extraction services - 2 essential tools for maps search and reviews",
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
    install_requires=['fastmcp>=2.0.0', 'requests>=2.25.0', 'pydantic>=2.0.0', 'typing-extensions>=4.0.0', 'fastapi>=0.104.0', 'uvicorn[standard]>=0.24.0', 'starlette<0.30.0', 'urllib3>=2.4.0'],
    keywords=['mseep', 'mcp', 'outscraper', 'google-maps', 'reviews', 'search', 'data-extraction', 'business-intelligence', 'api', 'claude', 'ai'],
)
