from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    description = readme.read()

setup(
    name="NoiseRandom",
    author="Andreas Karageorgos",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "gmpy2"
    ],
    license="MIT",
    long_description=description,
    long_description_content_type="text/markdown"
)