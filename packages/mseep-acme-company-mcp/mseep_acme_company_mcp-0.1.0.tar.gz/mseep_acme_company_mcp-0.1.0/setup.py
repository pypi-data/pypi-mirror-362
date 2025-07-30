from setuptools import setup, find_packages

setup(
    name='mseep-acme-company-mcp',
    version='0.1.0',
    description='Acme Company MCP server',
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
    install_requires=['boto3>=1.38.3', 'mcp[cli]>=1.6.0', 'requests>=2.32.0', 'fastmcp>=2.6.1', 'httpx>=0.28.1', 'python-dotenv>=1.1.0', 'strands-agents>=0.1.6', 'strands-agents-tools>=0.1.4'],
    keywords=['mseep'],
)
