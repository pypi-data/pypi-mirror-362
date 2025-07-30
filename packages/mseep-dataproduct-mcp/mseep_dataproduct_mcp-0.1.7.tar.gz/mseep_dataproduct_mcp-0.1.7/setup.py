from setuptools import setup, find_packages

setup(
    name='mseep-dataproduct_mcp',
    version='0.1.7',
    description='A Model Context Protocol (MCP) server for discovering data products, requesting access, and executing queries on the data platform to access business data.',
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.9.4', 'PyYAML>=6.0', 'python-dotenv>=1.0.0', 'pydantic>=2.0.0', 'snowflake-connector-python>=3.0.0', 'databricks-sql-connector>=3.0.0', 'databricks-sdk>=0.20.0', 'google-cloud-bigquery>=3.0.0'],
    keywords=['mseep'],
)
