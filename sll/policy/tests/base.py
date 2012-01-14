# try:
#     from Zope2.App import zcml
# except ImportError:
#     from Products.Five import zcml
# from Products.Five import fiveconfigure
# from Testing import ZopeTestCase as ztc
# from Products.PloneTestCase import PloneTestCase as ptc
# from Products.PloneTestCase.layer import onsetup


# @onsetup
# def setup_product():

#     fiveconfigure.debug_mode = True

#     import Products.PloneFormGen
#     zcml.load_config('configure.zcml', Products.PloneFormGen)
#     import Products.PFGExtendedMailAdapter
#     zcml.load_config('configure.zcml', Products.PFGExtendedMailAdapter)
#     import Products.PFGSelectionStringField
#     zcml.load_config('configure.zcml', Products.PFGSelectionStringField)

#     import collective.folderlogo
#     zcml.load_config('configure.zcml', collective.folderlogo)
#     import collective.pfg.payment
#     zcml.load_config('configure.zcml', collective.pfg.payment)
#     import collective.cart.core
#     zcml.load_config('configure.zcml', collective.cart.core)
#     import collective.cart.shipping
#     zcml.load_config('configure.zcml', collective.cart.shipping)
#     import collective.pfg.showrequest
#     zcml.load_config('configure.zcml', collective.pfg.showrequest)

#     import sll.policy
#     zcml.load_config('configure.zcml', sll.policy)

#     fiveconfigure.debug_mode = False

#     ztc.installPackage('sll.policy')
#     ztc.installPackage('collective.folderlogo')
#     ztc.installPackage('collective.pfg.payment')
#     ztc.installPackage('collective.cart.core')
#     ztc.installPackage('collective.cart.shipping')
#     ztc.installPackage('collective.pfg.showrequest')

#     ztc.installProduct('PloneFormGen')
#     ztc.installProduct('PFGExtendedMailAdapter')
#     ztc.installProduct('PFGSelectionStringField')
#     ztc.installProduct('NewSllSkin')

# setup_product()
# ptc.setupPloneSite(
#     products=[
#         'PloneFormGen',
#         'PFGExtendedMailAdapter',
#         'PFGSelectionStringField',
#         'collective.folderlogo',
#         'collective.pfg.payment',
#         'collective.cart.core',
#         'collective.cart.shipping',
#         'collective.pfg.showrequest',
#         'sll.policy',
#         'NewSllSkin',
#     ]
# )

# class TestCase(ptc.PloneTestCase):
#     """We use this base class for all the tests in this package. If
#     necessary, we can put common utility or setup code in here. This
#     applies to unit test cases.
#     """


# class FunctionalTestCase(ptc.FunctionalTestCase):
#     """We use this class for functional integration tests that use
#     doctest syntax. Again, we can put basic common utility or setup
#     code in here.
#     """

"""Base module for unittesting"""

import unittest2 as unittest

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class SllPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import sll.policy
        self.loadZCML(package=sll.policy)
        z2.installProduct(app, 'sll.policy')
        import sll.theme
        self.loadZCML(package=sll.theme)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'sll.policy:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'sll.policy')


FIXTURE = SllPolicyLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="SllPolicyLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="SllPolicyLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
