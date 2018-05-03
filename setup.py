from distutils.core import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='geoham',
      version='0.0.1pre',
      description="Library to manipulate geographic data about amateur radio repeaters and frequencies",
      license="GPL",
      author="Olivier Mehani",
      author_email="shtrom+geoham@ssji.net",
      url="http://scm.narf.ssji.net/git/geoham",
      packages=['geoham'],
      install_requires=reqs,
      entry_points={
          'console_scripts'; [
              'geoham = geoham.cli:main'
          ]
      },
      )
