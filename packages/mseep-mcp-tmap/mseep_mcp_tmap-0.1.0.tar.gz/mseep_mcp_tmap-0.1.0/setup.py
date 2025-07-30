from setuptools import setup, find_packages

setup(
    name='mseep-mcp-tmap',
    version='0.1.0',
    description='MCP for TMAP API',
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
    install_requires=['httpx[http2]>=0.28.1', 'mcp[cli]>=1.7.1', 'python-dotenv>=1.1.0'],
    keywords=['mseep'],
)
