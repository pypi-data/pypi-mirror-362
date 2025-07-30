from setuptools import setup, find_packages

setup(
    name='mseep-teradata-mcp-server',
    version='0.1.0',
    description='Add your description here',
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
    install_requires=['anthropic>=0.49.0', 'boto3>=1.37.37', 'langchain-core>=0.3.54', 'langchain-mcp-adapters>=0.0.9', 'langchain-openai>=0.3.14', 'langgraph>=0.3.31', 'openai>=1.75.0', 'pip>=25.0.1', 'pydantic>=2.11.3', 'pydantic-ai>=0.1.3', 'requests>=2.32.3', 'tabulate', 'litellm>=1.68.2', 'nest-asyncio>=1.6.0', 'google-adk>=1.3.0', 'mcp[cli]==1.9.3', 'mcp-cli>=0.1.0', 'teradatagenai>=20.0.0.0', 'tdfs4ds==0.2.4.16', 'teradataml>=20.0.0.5', 'teradatasqlalchemy>=20.0.0.0'],
    keywords=['mseep'],
)
