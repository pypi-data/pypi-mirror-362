from setuptools import setup, find_packages

setup(
    name="env_show",  # Your package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "python-dotenv"
    ],
    author="test",
    description="FastAPI plugin to expose .env values via an endpoint",
    long_description=open("./README.md ").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License"
    ],
)
