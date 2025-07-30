from setuptools import setup, find_packages

setup(
    name='mseep-mcp-ai-infra-real-time-agent',
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
    install_requires=['black>=25.1.0', 'isort>=6.0.1', 'langchain-mcp-adapters>=0.0.7', 'langchain-openai>=0.3.12', 'langgraph>=0.3.29', 'python-dotenv>=1.1.0'],
    keywords=['mseep'],
)
