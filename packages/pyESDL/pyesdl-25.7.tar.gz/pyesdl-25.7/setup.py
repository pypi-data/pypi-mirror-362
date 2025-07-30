# from distutils.core import setup
import itertools
import sys
import unittest

import versioneer
import setuptools

version = tuple(sys.version_info[:2])

if version < (3, 7):
    sys.exit('pyESDL requires at least Python >= 3.7')


# def my_test_suite():
#     test_loader = unittest.TestLoader()
#     test_suite = test_loader.discover('tests', pattern='*_test.py')
#     return test_suite


extras_require = {
    "profiles": ["influxdb==5.3.1", "openpyxl==3.1.2"],
    "geometry": ["shapely==2.0.1", "geojson==3.1.0", "pyproj==3.6.1"],
}
extras_require['all'] = list(itertools.chain.from_iterable(extras_require.values()))

setuptools.setup(
    name='pyESDL',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="https://energytransition.gitbook.io/esdl/",
    packages=setuptools.find_packages(),
    package_data={'': ['README.md', 'LICENSE.md']},
    include_package_data=True,
    license='Apache 2.0',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    description="Python implementation of the Energy System Description Language (ESDL) for modelling energy systems",
    author='Ewoud Werkman',
    author_email='ewoud.werkman@tno.nl',
    python_requires='>=3.7',
    install_requires=[
        'pyecore==0.13.2'
    ],
    extras_require=extras_require,
    # test_suite='setup.my_test_suite',
    tests_require = ["pytest"]
)
