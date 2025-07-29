from setuptools import find_packages, setup

setup(
    name="pymlt",
    packages=find_packages(include=["pymlt"]),
    include_package_data=True,
    python_requires=">=3.8",
)
