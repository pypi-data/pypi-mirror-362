# coding: utf-8

import os

from setuptools import (
    find_packages,
    setup,
)


requirements_filename = 'REQUIREMENTS'

requirements = []

with open(requirements_filename, 'r') as requirements_file:
    for rawline in requirements_file:
        line = rawline.strip()

        if not line.startswith('#'):
            requirements.append(line)

setup(
    name='datatransfer_client',
    author='BARS Group',
    dependency_links=('http://pypi.bars-open.ru/simple/m3-builder',),
    setup_requires=('m3-builder>=1.0.1',),
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    include_package_data=True,
    set_build_info=os.path.join(os.path.dirname(__file__), 'src', 'datatransfer'),
)
