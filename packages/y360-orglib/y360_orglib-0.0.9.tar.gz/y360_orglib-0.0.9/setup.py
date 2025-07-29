from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="y360-orglib",
    version="0.0.9",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Anton Bugrin",
    description="Unofficial Collection library for Y360 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abugrin/y360_orglib",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.28.1",
        "pydantic>=2.10.6",
        "python-dotenv>=1.0.1"
    ],
)