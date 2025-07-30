from setuptools import setup, find_packages

setup(
    name="devisay",
    version="0.1.2",
    author="Alwyn Quadras",
    author_email="alwynquad2002@gmail.com",
    description="A small package for funny ASCII prints",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
