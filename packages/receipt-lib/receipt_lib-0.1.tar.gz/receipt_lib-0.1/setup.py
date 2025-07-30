from setuptools import setup, find_packages

setup(
  name='receipt_lib',
  version='0.1',
  description='This is a python package for generating date of transaction and transaction code.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Bhargavi Gadhepally',
  author_email='x23344440@student.ncirl.ie',
  classifiers=[
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
],
  keywords='receipt_lib', 
  packages=find_packages(),
  python_requires=">=3.6"
)
