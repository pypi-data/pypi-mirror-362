from setuptools import setup, find_packages

setup(
    name='mseep-mcp-simple-openai-assistant',
    version='0.3.1',
    description='A simple MCP server for interacting with OpenAI assistants',
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
    install_requires=['fastmcp>=2.10.0', 'openai>=1.0.0'],
    keywords=['mseep'],
)
