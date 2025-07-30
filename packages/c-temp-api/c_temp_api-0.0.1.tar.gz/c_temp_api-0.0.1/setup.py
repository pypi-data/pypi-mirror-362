import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "c_temp_api",
    version = "0.0.1",
    author = "Miad Dehghani",
    author_email = "miaddehghani1365@gmail.com",
    description = "A client to collect temperature data from various service providers via API",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/miaddehghani/Python-Current-Temp-API",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)