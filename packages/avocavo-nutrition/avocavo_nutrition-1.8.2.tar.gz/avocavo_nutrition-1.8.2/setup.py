"""
Setup configuration for Avocavo Nutrition API Python SDK
"""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Python SDK for the Avocavo Nutrition API - Fast, accurate nutrition data with USDA verification"

# Read version from package
def get_version():
    version_file = os.path.join("avocavo_nutrition", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "1.0.0"

setup(
    name="avocavo-nutrition",
    version=get_version(),
    author="Avocavo",
    author_email="api-support@avocavo.com",
    description="Python SDK for the Avocavo Nutrition API - Fast, accurate nutrition data with USDA verification",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/avocavo/nutrition-api-python",
    project_urls={
        "Documentation": "https://nutrition.avocavo.app/docs/python",
        "API Dashboard": "https://nutrition.avocavo.app",
        "Bug Tracker": "https://github.com/avocavo/nutrition-api-python/issues",
        "Changelog": "https://github.com/avocavo/nutrition-api-python/blob/main/CHANGELOG.md",
        "Support": "mailto:api-support@avocavo.com",
    },
    classifiers=[
        # Development Status
        "Development Status :: 5 - Production/Stable",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        
        # Topic
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Database :: Front-Ends",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # Operating System
        "Operating System :: OS Independent",
        
        # Natural Language
        "Natural Language :: English",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "keyring>=23.0.0",  # For secure API key storage
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "twine>=3.0",
            "wheel>=0.36",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-mock>=3.0",
            "responses>=0.18.0",
            "pytest-asyncio>=0.18.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.17",
        ],
    },
    keywords=[
        "nutrition", "api", "usda", "food", "recipe", "health", "fitness", 
        "calories", "macros", "nutrients", "fooddata", "fdc", "cooking",
        "meal-planning", "diet", "wellness", "restaurant", "food-tech"
    ],
    include_package_data=True,
    zip_safe=False,
    
    # Package metadata
    platforms=["any"],
    license="MIT",
    
    # Additional metadata for PyPI
    download_url="https://pypi.org/project/avocavo-nutrition/",
)