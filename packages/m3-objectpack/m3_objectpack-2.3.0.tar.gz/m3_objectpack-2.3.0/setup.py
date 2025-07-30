# coding: utf-8
from os.path import (
    dirname,
    join,
)

from setuptools import (
    find_packages,
    setup,
)


def _read(file_name):
    with open(join(dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='m3-objectpack',
    license='MIT',
    description=_read('DESCRIPTION'),
    author='Alexey Pirogov',
    author_email='pirogov@bars-open.ru',
    url='https://bitbucket.org/barsgroup/objectpack',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    long_description=_read('README'),
    dependency_links=('https://pypi.bars-open.ru/simple/m3-builder',),
    setup_requires=('m3-builder>=1.2,<2',),
    install_requires=(
        'six>=1.11,<2',
        'm3-builder>=1.2,<2',
        'm3-django-compat>=1.10.1,<2',
        'django>=1.4,<5.0',
        'm3-core>=2.2.16,<3',
        'm3-ui>=2.2.87,<3',
    ),
    set_build_info=dirname(__file__),
)
