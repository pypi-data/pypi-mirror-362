from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apollog",
    version="0.1.1",
    author="Apollog Team",
    author_email="author@example.com",
    description="A monitoring solution for AWS services with log aggregation and error event summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bhavinrathava/Apollog",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "boto3>=1.26.0",
        "botocore",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "apollog=apollog.cli:main",
        ],
    },
    scripts=["apollog_cli.py", "apollog.bat"],
    package_data={
        "apollog": [
            "controlPlane/frontend/index.html",
            "controlPlane/frontend/config.json",
            "cloudformation_template.yaml",
        ],
    },
)
