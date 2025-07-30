from setuptools import setup, find_packages

setup(
    name="palestine_function_unit",
    version="1.33",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pconvert=punit.cli:main"
        ]
    },
    install_requires=[],
    author="Palestine Equation",
    author_email="1@leat.xyz",
    description="P-Unit Converter based on recursive persistence and geometric scaling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ileathan/punit ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
