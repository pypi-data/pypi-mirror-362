from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-jongler",
    version="1.1.0",
    author="Anton Pavlenko",
    description="A middleware utility for calling Google AI APIs (Gemini and Gemma) using multiple API keys to reduce need for paid tiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonpavlenko/api-jongler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1",
        "requests[socks]>=2.25.1",
        "configparser>=5.0.0",
        "colorama>=0.4.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "twine>=3.4",
        ],
    },
    package_data={
        "api_jongler": ["connectors/*.json"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "apijongler=api_jongler.cli:main",
        ],
    },
)
