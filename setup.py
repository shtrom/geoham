from distutils.core import setup

setup(name='geoham',
      version='0.0.1pre',
      description="Library to manipulate geographic data about amateur radio repeaters and frequencies",
      license="GPL",
      author="Olivier Mehani",
      author_email="shtrom+geoham@ssji.net",
      url="http://scm.narf.ssji.net/git/geoham",
      packages=['geoham'],
      install_requires=[
          'Click',
          'folium',
      ],
      entry_points={
          'console_scripts': [
              'geoham = geoham.cli:main'
          ]
      },
      )
