from setuptools import setup, find_packages

setup(
    name='cutflow_compare',
    version='2.0.0',
    author='Ibrahim H.I. ABUSHAWISH',
    author_email='ibrahim.hamed2701@gmail.com',
    description='A package to compare cutflow histograms from ROOT files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ibeuler/cutflow_compare',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0',
        "uncertainties>=3.2.3"
    ],
    entry_points={
    'console_scripts': [
        'cutflow_compare=cutflow_compare.cutflow_compare:main',
    ],
    },
)