from setuptools import setup, find_packages

setup(
    name='mseep-yfinance-trader',
    version='0.1.0',
    description='YFinance Trader MCP Tool for Claude Desktop',
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
    install_requires=['yfinance>=0.2.36', 'fastapi>=0.103.1', 'uvicorn>=0.23.2', 'pydantic>=2.4.2', 'requests>=2.31.0', 'pandas>=2.1.0'],
    keywords=['mseep'],
)
