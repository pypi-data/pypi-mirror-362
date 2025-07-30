
from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="swe-ai-agent",
    version="1.0.0",
    author="Harish SG",
    author_email="harishsg993010@gmail.com",
    description="SWE Agent - Headless Agentic IDE with comprehensive tool support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harishsg993010/SWE-Agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
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
    entry_points={
        "console_scripts": [
            "swe-agent=swe_agent.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "swe_agent": ["**/*.py"],
    },
)
