from setuptools import setup, find_packages

setup(
    name='common_libs',
    version='0.1.0',
    packages=find_packages(),
    description='Shared Services and Models for Trading App',
    author='Sam Fales',
    install_requires=[
        "redis",
        "pydantic"
    ],
)