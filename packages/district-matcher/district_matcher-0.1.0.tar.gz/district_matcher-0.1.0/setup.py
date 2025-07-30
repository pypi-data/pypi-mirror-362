from setuptools import setup, find_packages

setup(
    name='district-matcher',
    version='0.1.0',
    description='Match historical district names using semantic similarity',
    author='Ishaan',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'torch>=1.9.0',
        'sentence-transformers>=2.2.2',
    ],
    python_requires='>=3.7',
)
