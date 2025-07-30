from setuptools import setup, find_packages

setup(
    name="rabbit-bq-job-optimizer",
    version="0.1.12",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0"
    ],
    author="Rabbit Team",
    author_email="success@followrabbit.ai",
    description="Python client for Rabbit BigQuery Job Optimizer API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/followrabbit-ai/python-bq-job-optimizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 