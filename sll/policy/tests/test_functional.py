try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest
from Testing import ZopeTestCase as ztc

from Acquisition import aq_base
from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from sll.policy.tests import base

class TestSetup(base.FunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)

        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def beforeTearDown(self):
        portal = self.portal
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost), provided=IMailHost)


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/browser.txt',
            package='sll.policy',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
