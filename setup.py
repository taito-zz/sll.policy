from setuptools import find_packages
from setuptools import setup


setup(
    name='sll.policy',
    version='1.0',
    description="Turns plone site into SLL site.",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@abita.fi',
    url='http://sll.fi/',
    license='None-free',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['sll'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PFGExtendedMailAdapter',
        'Products.PFGSelectionStringField',
        'abita.development',
        'collective.folderlogo',
        'collective.monkeypatcher',
        'collective.pfg.payment',
        'collective.pfg.showrequest',
        'collective.portlet.fblikebox',
        'collective.sharerizer',
        'five.grok',
        'hexagonit.testing',
        'plone.browserlayer',
        'setuptools',
        'sll.carousel',
        'sll.portlet',
        'sll.templates',
        'sll.theme',
        'z3c.autoinclude',
        'z3c.jbot',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
