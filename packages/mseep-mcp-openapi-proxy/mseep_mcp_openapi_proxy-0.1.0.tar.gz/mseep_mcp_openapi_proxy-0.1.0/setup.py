from setuptools import setup, find_packages

setup(
    name='mseep-mcp-openapi-proxy',
    version='0.1.0',
    description='MCP server for exposing OpenAPI specifications as MCP tools.',
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
    install_requires=['mcp[cli]>=1.2.0', 'python-dotenv>=1.0.1', 'requests>=2.25.0', 'fastapi>=0.100.0', 'pydantic>=2.0', 'prance>=23.6.21.0', 'openapi-spec-validator>=0.7.1', 'jmespath>=1.0.1'],
    keywords=['mseep'],
)
