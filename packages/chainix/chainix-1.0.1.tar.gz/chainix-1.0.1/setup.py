from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='chainix',
    version='1.0.1',
    author='Chainix',
    author_email='jack@chainix.ai',
    description='A client library for executing asynchronous chains on chainix.ai with custom function callbacks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChainixDev/chainix-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        'requests>=2.25.0',
    ],
)