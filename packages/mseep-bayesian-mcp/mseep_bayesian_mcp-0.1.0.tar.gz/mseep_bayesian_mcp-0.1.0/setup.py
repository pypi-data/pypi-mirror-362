from setuptools import setup, find_packages

setup(
    name='mseep-bayesian-mcp',
    version='0.1.0',
    description='Bayesian reasoning MCP server for LLMs',
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
    install_requires=['pymc>=5.0.0', 'arviz>=0.14.0', 'numpy>=1.20.0', 'pydantic>=2.0.0', 'mcp>=1.6.0', 'fastapi>=0.100.0', 'matplotlib>=3.5.0'],
    keywords=['mseep'],
)
