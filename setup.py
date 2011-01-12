from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='gdwmp.core',
      version=version,
      description="GDW marmiton & polochon",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='gdw marmiton polochon',
      author='Affinitic Sprl',
      author_email='info@affinitic.be',
      url='http://svn.affinitic.be/plone/gites/gdwmp.core',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gdwmp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'python-ldap',
          'Products.PloneLDAP',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
