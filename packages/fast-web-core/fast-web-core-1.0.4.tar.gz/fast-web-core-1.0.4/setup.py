from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r', encoding="utf-8") as f:
    long_description = f.read()

# warning!
# for pymongo==4.7.3 and mongo version 7.0
# if you want to use old version, switch branch to mongo4

setup(name='fast-web-core',
      version='1.0.4',
      description='fast web core for zsodata',
      long_description=long_description,
      author='zsodata',
      author_email='team@zso.io',
      url='http://www.zsodata.com',
      install_requires=[
      ],
      python_requires='>=3.7',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
