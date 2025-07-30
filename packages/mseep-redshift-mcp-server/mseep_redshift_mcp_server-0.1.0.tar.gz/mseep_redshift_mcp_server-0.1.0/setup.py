from setuptools import setup, find_packages

setup(
    name='mseep-redshift-mcp-server',
    version='0.1.0',
    description='Model Context Protocol (MCP) server for Amazon Redshift',
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
    install_requires=['mcp[cli]>=1.9.1', 'psycopg2-binary>=2.9.10', 'pydantic>=2.0.0', 'loguru>=0.7.0'],
    keywords=['mseep', 'redshift', 'mcp', 'llm', 'database'],
)
