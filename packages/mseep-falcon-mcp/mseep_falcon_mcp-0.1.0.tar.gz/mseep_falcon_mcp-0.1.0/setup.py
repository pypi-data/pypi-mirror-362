from setuptools import setup, find_packages

setup(
    name='mseep-falcon-mcp',
    version='0.1.0',
    description='CrowdStrike Falcon MCP Server',
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
    install_requires=['crowdstrike-falconpy>=1.3.0', 'mcp>=1.8.0,<2.0.0', 'python-dotenv>=1.0.0'],
    keywords=['mseep'],
)
