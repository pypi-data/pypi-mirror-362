import re
from setuptools import setup, find_packages

with open("src/PyMCUlib/__init__.py", "r", encoding="utf-8") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name="PyMCUlib",
    version=version,
    description="Material Color Utilities Python Library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Wenkang Li",
    author_email="support@deepblue.cc",
    url="https://github.com/wenkang-deepblue/material-color-utilities-python",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license="Apache-2.0",
    install_requires=[
        "numpy",
        "pillow",
    ],
    python_requires=">=3.12.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics",
    ],
)
