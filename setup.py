from setuptools import find_packages, setup

setup(
    name="AmazonWatcher",
    packages=find_packages(exclude=["Tests", "Tests."])
)
