from setuptools import setup, find_packages


setup(

    name="phrlibrary",

    version="1.0.0",

    packages=find_packages(),

    install_requires=[open("requirements.txt", "r").read()],  # 依赖项

    author="Phr",

    description="A demo library",

    long_description=open("README.md").read(),

    python_requires=">=3.6"

)