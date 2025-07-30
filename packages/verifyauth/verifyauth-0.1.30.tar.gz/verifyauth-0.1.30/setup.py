from setuptools import setup, find_packages

setup(
    name="verifyauth",
    version="0.1.30",
    description="A decorator for FastAPI to verify authentication and authorization via an external service.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Cosme Sousa",
    author_email="",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests",
        "fastapi"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
