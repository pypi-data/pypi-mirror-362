from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wav-loo",
    version="1.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-tool: find WAV files, plus kgn/gp/uv alias commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wav-loo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "urllib3>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "wav-loo=wav_loo.cli:main",
        ],
    },
) 