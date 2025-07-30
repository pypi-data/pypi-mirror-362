from setuptools import setup, find_packages

setup(
    name='yatranslator',
    version='3.0',
    description='Async simple wrapper for Disroot Translate API',
    author='sigmaboy',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.7'
    ],
    python_requires='>=3.7',
)
