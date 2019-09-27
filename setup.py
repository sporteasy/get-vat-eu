#
# setup.py
#

from setuptools import setup, find_packages

setup(
    name='get_vat_eu',
    version='0.0.1',
    packages=find_packages(exclude=['*tests*']),
    license='TODO',
    description='A utility that is able to get and parse EU EC VATs.',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@live.com',
    keywords='vat ec eu',
    url='https://github.com/frnmst/TODO',
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'get_vat_eu=get_vat_eu.__main__:main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[''],
)

