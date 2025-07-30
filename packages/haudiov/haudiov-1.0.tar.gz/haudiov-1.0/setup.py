from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='haudiov',
    version='1.0',
    description='haudiov',
    long_description=long_description,
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=find_packages(),
    package_dir={'haudiov': 'haudiov'},
    package_data={"haudiov": ["**"]},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        "pyaudio",
        "numpy",
        "pyfiglet",
    ],
)