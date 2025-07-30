from setuptools import setup, find_packages

setup(
    name='mseep-arduino-mcp',
    version='0.1.0',
    description='This is an Arduino MCP server',
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
    install_requires=['asyncio>=3.4.3', 'fastmcp>=2.8.1', 'pyfirmata2>=2.5.1'],
    keywords=['mseep'],
)
