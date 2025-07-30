
from setuptools import setup, find_packages

setup(
    name="swe-ai-agent",
version="1.0.7",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "swe-agent=swe_agent.main:main",
        ],
    },
    install_requires=[
        "anthropic>=0.57.1",
        "langchain-anthropic>=0.3.17",
        "langchain>=0.3.26",
        "langchain-core>=0.3.68",
        "langgraph>=0.5.3",
        "rich>=14.0.0",
        "click>=8.0.0",
        "psutil>=5.8.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0",
        "pydantic>=2.0.0",
        "requests>=2.28.0",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.9",
    author="Harish SG",
    author_email="harishsg993010@gmail.com",
    description="SWE Agent - Headless Agentic IDE",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
