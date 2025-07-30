from setuptools import setup, find_packages

setup(
    name='mseep-mcp-goodnews',
    version='0.1.0',
    description='An MCP application that delivers curated positive and uplifting news stories.',
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
    install_requires=['asyncio>=3.4.3', 'cohere>=5.14.0', 'mcp[cli]>=1.4.1', 'pydantic>=2.10.6'],
    keywords=['mseep'],
)
