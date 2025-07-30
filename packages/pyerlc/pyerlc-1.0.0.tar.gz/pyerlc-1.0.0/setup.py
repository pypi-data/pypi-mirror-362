from setuptools import setup, find_packages

setup(
    name="pyerlc",
    version="1.0.0",
    description="Python wrapper for the ERLC PRC API",
    author="epell Development",
    author_email="epell1@epelldevelopment.xyz",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorama"
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
