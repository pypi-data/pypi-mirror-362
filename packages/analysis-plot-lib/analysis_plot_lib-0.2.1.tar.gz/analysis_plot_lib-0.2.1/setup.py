from setuptools import setup, find_packages

setup(
  name='analysis_plot_lib',
  version='0.2.1',
  description='This is a simple Python package for creating pie chart.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Vamshi',
  author_email=' X23289635@student.ncirl.ie',
  license='MIT',
  classifiers=[
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Programming Language :: Python :: 3'
],
  keywords='analysis_plot_lib', 
  packages=find_packages(),
  python_requires=">=3.6"
)
