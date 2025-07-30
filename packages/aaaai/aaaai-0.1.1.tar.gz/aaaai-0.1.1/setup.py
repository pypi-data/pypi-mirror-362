import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aaaai",
    version="0.1.1",
    author="Mahdi Nouri",
    author_email="algo.mahdi.nouri@gmail.com",
    description="all agents and AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/algonouir/aaaai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)