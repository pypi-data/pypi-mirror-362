from setuptools import setup, find_packages
install_requires=["numpy", "pandas","pubchempy"]


setup(
    name="metabolomics_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    author="Amirhossein Sakhteman",
    author_email="amirhossein.sakhteman@tume.de",
    description="Tools for preprocessing data for xcms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
)
