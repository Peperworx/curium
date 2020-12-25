import setuptools

with open("docs/source/src/about/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curium",
    version="0.0.0",
    author="Riley Wilton",
    author_email="riley.j.wilton@gmail.com",
    description="A basic, C-like language written in python ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peperworx/curium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)