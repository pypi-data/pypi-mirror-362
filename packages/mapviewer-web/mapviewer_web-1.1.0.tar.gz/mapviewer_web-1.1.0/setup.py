from setuptools import setup, find_packages
import os

def readme():
    with open('README.md') as file:
        return(file.read())

def versionNumber():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Mapviewer_web/_version.py')) as versionFile:
        return(versionFile.readlines()[-1].split()[-1].strip("\"'"))

setup(name='mapviewer-web',
      version=versionNumber(),
      description='MapViewer-Web: Visualizing galaxy properties from the GIST pipeline products',
      long_description_content_type="text/markdown",
      long_description=readme(),
      classifiers=[
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
      ],
      url='https://github.com/purmortal/mapviewer-web',
      author='Zixian Wang (Purmortal)',
      author_email='wang.zixian.astro@gmail.com',
      packages=find_packages(),
      package_data={
          '': ['**/*']
      },
      install_requires=[
          'astropy',
          'numpy',
          'scipy',
          'pandas',
          'dash',
          'dash_iconify',
          'dash-mantine-components==0.12.1',
          'dash_ag_grid',
          'dash_auth',
          'h5py',
      ],
      python_requires='>=3.6',
      entry_points={
          'console_scripts': [
              'Mapviewer-web        = Mapviewer_web.MainProcess:start_app'
          ],
      },
      include_package_data=True,
      zip_safe=False)
