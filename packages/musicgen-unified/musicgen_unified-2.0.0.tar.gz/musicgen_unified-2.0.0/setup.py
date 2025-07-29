"""
Setup script for MusicGen Unified.
"""

from setuptools import setup, find_packages

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="musicgen-unified",
    version="2.0.0",
    author="Bright Liu",
    author_email="brightliu@college.harvard.edu",
    description="Simple, clean instrumental music generation with MusicGen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bright-L01/musicgen-unified",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "scipy>=1.7.0",
        "numpy>=1.21.0",
        "soundfile>=0.12.0",
        "librosa>=0.10.0",
        "pydub>=0.25.0",
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "api": [
            "fastapi>=0.100.0",
            "uvicorn[standard]>=0.23.0",
            "python-multipart>=0.0.6",
        ],
        "web": [
            "fastapi>=0.100.0",
            "uvicorn[standard]>=0.23.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
        "gpu": [
            "flash-attn>=2.0.0",
            "xformers>=0.0.20",
        ],
    },
    entry_points={
        "console_scripts": [
            "musicgen=musicgen.cli:main",
            "musicgen-api=musicgen.api:main",
            "musicgen-web=musicgen.web:main",
        ],
    },
    package_data={
        "musicgen": ["../static/*"],
    },
    include_package_data=True,
)