from setuptools import setup, find_packages

setup(
    name='mseep-futu-stock-mcp-server',
    version='0.1.0',
    description='A Model Context Protocol (MCP) server for accessing Futu OpenAPI functionality',
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
    install_requires=['futu-api', 'fastapi', 'uvicorn', 'pydantic', 'python-dotenv', 'websockets', 'aiohttp', 'loguru', 'mcp[cli]>=1.6.0', 'psutil'],
    keywords=['mseep'],
)
