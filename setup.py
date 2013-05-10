from setuptools import find_packages
from setuptools import setup


setup(
    name='sll.policy',
    version='1.6',
    description="Turns plone site into SLL site.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
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
        'Products.PFGExtendedMailAdapter',
        'Products.PFGSelectionStringField',
        'collective.folderlogo',
        'collective.microsite',
        'collective.monkeypatcher',
        'collective.pfg.payment',
        'collective.pfg.showrequest',
        'setuptools',
        'sll.basepolicy',
        'sll.locales',
        'sll.portlet',
        'sll.theme'],
    extras_require={'test': ['hexagonit.testing']},
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
