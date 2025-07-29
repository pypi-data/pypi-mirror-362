# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from nfetoolkit import __version__


def parse_requirements(filename):
    with open(filename, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'Toolkit para manipulação de notas fiscais eletrônicas'

setup(
    name='nfetoolkit',
    version=__version__,
    license='MIT',
    author='Ismael Nascimento',
    author_email='ismaelnjr@icloud.com.br',
    description='Toolkit para manipulação de notas fiscais eletrônicas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ismaelnjr/nfetoolkit-project.git',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'nfetoolkit = nfetoolkit.cli:main',
        ],
    },
)
