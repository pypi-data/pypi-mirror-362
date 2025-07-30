from setuptools import setup, find_packages

setup(
    name="secret_store_gor",
    version="1.0.4",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A secure secret store package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://your-repo-url",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
