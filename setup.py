from setuptools import setup, find_packages

setup(name='geoham',
      version='0.0.1pre',
      description='Library to manipulate geographic data about amateur radio repeaters and frequencies',
      license='GPL',
      author='Olivier Mehani',
      author_email='shtrom+geoham@ssji.net',
      url='http://scm.narf.ssji.net/git/geoham',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      install_requires=[
          'Click',
          'notebook',
          'folium',
          'pandas',
      ],
      extras_require={
          'tests': [
              'pytest',
              'pytest-runner',
          ],
      },
      entry_points={
          'console_scripts': [
              'geoham = geoham.cli:main',
          ]
      },
      )
