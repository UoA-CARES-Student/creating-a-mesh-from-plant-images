from setuptools import setup

with open("README", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="model_processing",
    version="1.0",
    description="Takes multiple points cloud, pre aligned to each other, combines them and applies filtering",
    license="MIT",
    long_description=long_description,
    author="Max Nankivell, Eva Sorensen",
    author_email="maxnankivell1@gmail.com, eva.elaine.sorensen@gmail.com",
    packages=["model_processing"],
)
