from setuptools import setup, find_packages

setup(
    name='mseep-hkopenai.hk_finance_mcp_server',
    version='0.1.7',
    description='Hong Kong Finance MCP Server providing financial data tools',
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
    install_requires=['fastmcp>=2.10.2', 'requests>=2.31.0', 'pytest>=8.2.0', 'pytest-cov>=6.1.1', 'modelcontextprotocol', 'hkopenai_common'],
    keywords=['mseep'],
)
