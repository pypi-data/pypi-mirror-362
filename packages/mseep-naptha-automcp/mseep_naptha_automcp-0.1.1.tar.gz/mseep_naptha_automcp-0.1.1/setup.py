from setuptools import setup, find_packages

setup(
    name='mseep-naptha-automcp',
    version='0.1.1',
    description='Convert tool, agents and orchestrators from existing agent frameworks to MCP servers',
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
    install_requires=['mcp>=1.6.0', 'pydantic>=2.11.1', 'python-dotenv>=1.0.0', 'toml>=0.10.0'],
    keywords=['mseep'],
)
