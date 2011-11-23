from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('sll', 'policy', 'version.txt').strip()

long_description = (
    open("README.txt").read() + "\n" +
    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read() + "\n" +
    open(os.path.join("docs", "CREDITS.txt")).read()
    )

setup(name='sll.policy',
      version=version,
      description="Turns plone site into SLL site.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Taito Horiuchi',
      author_email='taito.horiuchi@abita.fi',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sll'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.browserlayer',
          'setuptools',
          'unittest2',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
