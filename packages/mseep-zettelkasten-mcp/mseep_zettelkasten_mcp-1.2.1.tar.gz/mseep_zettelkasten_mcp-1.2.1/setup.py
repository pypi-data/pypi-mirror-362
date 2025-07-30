from setuptools import setup, find_packages

setup(
    name='mseep-zettelkasten-mcp',
    version='1.2.1',
    description='A Zettelkasten knowledge management system as an MCP server',
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
    install_requires=['mcp[cli]>=1.2.0', 'sqlalchemy>=2.0.0', 'pydantic>=2.0.0', 'python-frontmatter>=1.0.0', 'markdown>=3.4.0', 'python-dotenv>=1.0.0'],
    keywords=['mseep'],
)
