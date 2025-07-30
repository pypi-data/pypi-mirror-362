from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cetus_tools',
    packages=find_packages(exclude=("tests",)),
    version='0.1.8',
    description='Library for python tools used in Cetus developments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Camilo Alaguna',
    author_email='camilo.alaguna@itrmachines.com',
    install_requires=['requests>=2.31.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    keywords=['Cetus', 'Binance', 'Bitso', 'Telegram', 'Public API']
)