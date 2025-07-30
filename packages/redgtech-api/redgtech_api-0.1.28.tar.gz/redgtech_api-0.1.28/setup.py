from setuptools import setup, find_packages
import os

def get_version():
    """Get version from GitHub tag or default."""
    # Check if we're in GitHub Actions
    github_ref = os.environ.get('GITHUB_REF', '')
    if github_ref.startswith('refs/tags/v'):
        version = github_ref.split('refs/tags/v')[1]
        print(f"Using version from GitHub tag: {version}")
        return version
    
    # Default version for local development
    return "0.1.27"

setup(
    name="redgtech-api",
    version=get_version(),
    description="A Python package to interact with the Redgtech API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/redgtech-automacao/redgtech-python-api",
    author="Jonh Sady",
    author_email="luannnvg@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)