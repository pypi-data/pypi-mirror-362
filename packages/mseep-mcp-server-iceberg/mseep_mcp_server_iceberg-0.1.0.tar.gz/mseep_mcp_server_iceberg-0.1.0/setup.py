from setuptools import setup, find_packages

setup(
    name='mseep-mcp-server-iceberg',
    version='0.1.0',
    description='MCP server for interacting with an Apache Iceberg catalog and data lake',
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
    install_requires=['mcp>=1.0.0', 'pyiceberg>=0.5.1', 'pyarrow>=14.0.1', 'sqlparse>=0.4.4', 'python-dotenv', 'requests', 'fsspec', 's3fs'],
    keywords=['mseep'],
)
