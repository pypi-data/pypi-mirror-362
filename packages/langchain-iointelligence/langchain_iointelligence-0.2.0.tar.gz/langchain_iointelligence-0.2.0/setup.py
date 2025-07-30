"""Setup script for langchain-iointelligence package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-iointelligence",
    version="0.2.0",
    author="SOH",
    author_email="sousohsou1@gmail.com",
    description="LangChain wrapper for io Intelligence LLM API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soh7410/langchain-iointelligence",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "requests>=2.25.0",
        "python-dotenv>=1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "isort>=5.10.0",
            "types-requests>=2.25.0",
        ],
    },
    keywords="langchain llm ai io-intelligence api-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/soh7410/langchain-iointelligence/issues",
        "Source": "https://github.com/soh7410/langchain-iointelligence",
    },
)
