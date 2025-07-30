from setuptools import setup, find_packages

setup(
    name='cadro',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'flask',
        'numpy',
        'sentence-transformers',
        'faiss-cpu',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'cadro-cli=src.cadro.cli:cli',
            'upkeys-cli=src.cadro.upkeyscli:cli',
        ],
    },
)
