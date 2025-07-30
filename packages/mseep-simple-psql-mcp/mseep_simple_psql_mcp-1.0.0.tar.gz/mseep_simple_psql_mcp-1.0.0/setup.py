from setuptools import setup, find_packages

setup(
    name='mseep-simple-psql-mcp',
    version='1.0.0',
    description='A PostgreSQL MCP server project',
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
    install_requires=['aiohttp>=3.11.13', 'mcp[cli]>=1.3.0', 'pyyaml>=6.0.2'],
    keywords=['mseep'],
)
