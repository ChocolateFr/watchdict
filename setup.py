from setuptools import setup, find_packages
import os

def read_readme():
    """Read the contents of the README file."""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name="watch-dict",  # Name of the library
    version="0.1",  # Version of the library
    packages=find_packages(),  # Automatically find packages
    install_requires=[],
    long_description=read_readme(),  # Read and include the README content
    long_description_content_type='text/markdown',  # Specify that it's markdown
    author="Chocolate Loves You",  # Author's name
    author_email="chocolateisfr@gmail.com",  # Author's email address
    description="Please watch my dictionary!",  # Short description
    url="https://github.com/chocolatefr/watchdict",  # URL for your project (e.g., GitHub)
    classifiers=[  # Add classifiers to provide metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",  # The license for your library
    python_requires='>=3.6',  # Specify the required Python version
    include_package_data=True,  # Include non-Python files in your package (e.g., README, LICENSE)
)
