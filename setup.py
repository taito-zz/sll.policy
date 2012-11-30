from setuptools import find_packages
from setuptools import setup


setup(
    name='sll.policy',
    version='1.3',
    description="Turns plone site into SLL site.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@abita.fi',
    url='https://github.com/taito/sll.policy',
    license='None-free',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['sll'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFPlone>=4.2',
        'Products.PFGExtendedMailAdapter',
        'Products.PFGSelectionStringField',
        'collective.folderlogo',
        'collective.microsite',
        'collective.monkeypatcher',
        'collective.pfg.payment',
        'collective.pfg.showrequest',
        'five.grok',
        'hexagonit.testing',
        'setuptools',
        'sll.basepolicy',
        'sll.carousel',
        'sll.locales',
        'sll.portlet',
        'sll.templates',
        'sll.theme',
        'z3c.jbot'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
