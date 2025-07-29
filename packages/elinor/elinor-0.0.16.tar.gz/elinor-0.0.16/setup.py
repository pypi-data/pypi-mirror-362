from setuptools import find_packages, setup

setup(
    name="elinor",
    version="0.0.16",
    author="Dashvvood",
    author_email="mathismottis@gmail.com",
    description="some util functions",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pillow",
        "matplotlib",
        "pybase64",
        "pyyaml",
        "pandas",
        "dotenv",
        "deprecated",
    ],
)