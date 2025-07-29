"""Setup configuration for CraftX.py package."""

from setuptools import setup, find_packages  # pylint: disable=import-error

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="craftxpy",
    version="0.1.2",
    author="DavidAnderson01",
    author_email="questions@craftx.py",
    description="Python-native intelligence, modular by design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidanderson01/craftxpy",
    project_urls={
        "Documentation": "https://docs.craftx.py",
        "Source": "https://github.com/davidanderson01/craftxpy",
        "Website": "https://craftx.py",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'craftxpy': ['assets/img/*.svg'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "craftx-demo=examples.demo:main",
            "craftx-new-tool=scripts.new_tool:main",
        ],
    },
)
