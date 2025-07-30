from setuptools import setup, find_packages

setup(
    name='mseep-mcp-taiga-bridge',
    version='0.1.0',
    description='Taiga integration bridge for MCP',
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
    install_requires=['mcp[cli]>=0.1.0', 'fastapi>=0.104.0', 'uvicorn[standard]>=0.23.0', 'python-dotenv>=0.15.0', 'httpx>=0.25.0', 'pydantic>=2.4.0', 'pydantic-settings>=2.0.0', 'tenacity>=8.2.0', 'pytest>=8.3.5', 'pytaigaclient'],
    keywords=['mseep'],
)
