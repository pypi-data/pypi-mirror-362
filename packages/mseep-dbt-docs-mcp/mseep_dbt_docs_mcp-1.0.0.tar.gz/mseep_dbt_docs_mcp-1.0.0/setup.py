from setuptools import setup, find_packages

setup(
    name='mseep-dbt-docs-mcp',
    version='1.0.0',
    description='Model Context Protocol (MCP) server for dbt docs',
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
    install_requires=['dbt-core>=1.8', 'mcp[cli]>=1.2.0', 'networkx', 'python-decouple', 'rapidfuzz', 'snowplow-tracker<1.1.0', 'sqlglot>=26.12.0', 'tqdm'],
    keywords=['mseep'],
)
