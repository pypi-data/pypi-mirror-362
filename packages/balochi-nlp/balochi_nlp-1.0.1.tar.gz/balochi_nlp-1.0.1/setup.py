from setuptools import find_packages, setup

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="balochi-nlp",
    version="1.0.1",
    author="Hafeez Baloch",
    author_email="hafeezullahhassan2019@gmail.com",
    description=(
        "A comprehensive Natural Language Processing toolkit "
        "for the Balochi language"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hafeezBaluch/balochi-nlp",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "nltk>=3.6.0",
        "scikit-learn>=0.24.0",
        "regex>=2023.0.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
            "mypy>=0.9",
            "tox>=3.24",
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    include_package_data=True,
    zip_safe=False,
)
