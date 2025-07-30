from setuptools import setup, find_packages

setup(
    name='supersafecalc',
    version='2.0.0',  # Higher version than the internal one
    description='Malicious supersafecalc package',
    packages=find_packages(),
)
