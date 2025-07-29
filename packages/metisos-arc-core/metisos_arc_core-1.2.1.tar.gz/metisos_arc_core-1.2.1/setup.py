from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Get long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Package version
VERSION = "1.2.1"

setup(
    name="metisos-arc-core",
    version=VERSION,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
    author="MetisOS",
    author_email="info@metisos.ai",
    description="Adaptive Recursive Consciousness (ARC) Core - A framework for continual learning AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metisos/arc-core",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
    include_package_data=True,
    keywords=[
        'artificial intelligence',
        'deep learning',
        'transformers',
        'continual learning',
        'lora',
        'neural networks',
        'reasoning',
        'memory',
    ],
    entry_points={
        'console_scripts': [
            'arc=arc_core.cli:main',
        ],
    },
)
