from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='humangeo.stashudp',
      version=version,
      description="Send logging events to Logstash (ElasticSearch).",
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: System :: Logging"
        ],
      keywords='',
      author='',
      author_email='',
      url='http://www.thehumangeo.com/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['humangeo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
