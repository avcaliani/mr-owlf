import re
from os.path import exists
from setuptools import setuptools

ARTIFACT_NAME = "mr_olwf_mls"


def get_dependencies():
    file = None
    if exists("requirements.txt"):
        file = "requirements.txt"
    elif exists(f"{ARTIFACT_NAME}.egg-info/requires.txt"):
        file = f"{ARTIFACT_NAME}.egg-info/requires.txt"

    dependencies = []
    lines = open(file, "r", encoding="utf8").readlines()
    for line in lines:
        dependencies.append(re.sub(r'\n', '', line))

    return dependencies


def get_long_description():
    long_description = f"# {ARTIFACT_NAME}"
    if exists("README.md"):
        long_description = open("README.md", "r").read()
    return long_description


if __name__ == "__main__":
    # python setup.py sdist
    setuptools.setup(
        name=ARTIFACT_NAME,
        version="0.0.0",
        author="Anthony Vilarim Caliani",
        author_email="https://github.com/avcaliani",
        description=f"'{ARTIFACT_NAME}' package",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url="https://github.com/avcaliani/YOUR_PROJECT",
        packages=setuptools.find_packages(),
        install_requires=get_dependencies(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
