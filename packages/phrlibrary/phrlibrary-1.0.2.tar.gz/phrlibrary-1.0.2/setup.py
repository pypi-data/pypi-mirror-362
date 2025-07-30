from setuptools import setup, find_packages


setup(

    name="phrlibrary",

    version="1.0.2",

    packages=find_packages(),

    install_requires=[open("requirements.txt", "r").read()],
    author="Phr",

    description="A demo library",

    long_description=open("README.md").read(),

    python_requires=">=3.6",
    scripts=["scripts/custom_scripts.py"],
    entry_points={
        "console_scripts": [
            "phrtools=phrlibrary.module:main"
        ]
    }
)