from setuptools import setup, find_packages
import os

# Read the README for a detailed project description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="syntaxmatrix",
    version="1.4",
    author="Bob Nti",
    author_email="bob.nti@syntaxmatrix.com",
    description="SyntaxMUI: A customizable UI framework for Python AI Assistant Projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobganti/SimpleRAG",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "syntaxmatrix": [
            "static/js/*.js",
            "static/icons/*.svg",
            "static/icons/*.png",
            "static/icons/*.jpg",
            "static/icons/*.jpeg",
        ]
    },
    install_requires=[
        "Flask>=3.0.3",
        "requests>=2.32.3",
        "Markdown>=3.7",
        "pypdf>=5.4.0",          
        "nest-asyncio>=1.6.0",   
        "python-dotenv>=1.1.0",  
        "openai>=1.84.0",
        "google-genai>=1.19.0",
    ],
    extras_require={
        "analysis": [
            "pandas>=2.2.3",
            "numpy>=2.0.2",
            "matplotlib>=3.9.4",
            "plotly>=6.0.0",
            "seaborn>=0.13.2",
            "scikit-learn>=1.6.1",
            "jupyter_client>=8.6.3",
            "ipykernel>=6.29.5",
        ],
        "auth": [
             "sqlalchemy>=2.0.41",
             "cryptography>=45.0.5",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)