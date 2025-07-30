from setuptools import setup, find_packages

setup(
    name='mseep-pylib2mcp',
    version='1.0.0',
    description='Expose Python library functions as MCP server tools',
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
    install_requires=['fastmcp==2.8.1', 'pydantic>=2.11.7', 'typer>=0.16.0'],
    keywords=['mseep'],
)
