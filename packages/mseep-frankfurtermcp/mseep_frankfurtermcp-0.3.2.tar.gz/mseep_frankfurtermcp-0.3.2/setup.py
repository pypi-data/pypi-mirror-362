from setuptools import setup, find_packages

setup(
    name='mseep-frankfurtermcp',
    version='0.3.2',
    description='A MCP server for currency exchange rates and currency conversion using the Frankfurter API.',
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
    install_requires=['fastmcp>=2.8.0', 'python-dotenv>=1.1.0', 'typer>=0.16.0'],
    keywords=['mseep', 'finance', 'mcp', 'currency-exchange-rates', 'currency-converter', 'frankfurter-api', 'model-context-protocol', 'mcp-server', 'fastmcp', 'model-context-protocol-server', 'mcp-composition'],
)
