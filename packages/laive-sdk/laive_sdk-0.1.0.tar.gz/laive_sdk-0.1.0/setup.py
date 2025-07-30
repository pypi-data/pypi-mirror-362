from setuptools import setup, find_packages
import os

# Read version from __init__.py
def get_version():
    init_py = os.path.join(os.path.dirname(__file__), '__init__.py')
    try:
        with open(init_py) as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"').strip("'")
    except (FileNotFoundError, Exception):
        pass
    return "0.1.0"

# Read README for long description
def get_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Python SDK for the Laive RAG API"

setup(
    name="laive-sdk",
    version=get_version(),
    description="Python SDK for the Laive RAG API",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Laive",
    author_email="contact@laive.ai",
    url="https://github.com/laiveai/Python-SDK",
    project_urls={
        "Bug Reports": "https://github.com/laiveai/Python-SDK/issues",
        "Source": "https://github.com/laiveai/Python-SDK",
        "Documentation": "https://github.com/laiveai/Python-SDK#readme",
    },
    packages=find_packages(exclude=["tests", "notebooks"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "rich>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
            "requests>=2.25.0",
        ],
    },
    python_requires=">=3.7",
    keywords="laive, rag, retrieval, augmented, generation, ai, nlp, sdk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
) 