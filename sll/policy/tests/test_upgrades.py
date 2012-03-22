from sll.policy.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
# from plone.registry.interfaces import IRegistry
# from zope.component import getUtility


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_upgrade_1_to_2(self):
        from sll.policy.upgrades import upgrade_1_to_2
        upgrade_1_to_2(self.portal)
        self.assertEqual(
            self.portal.userdefined_roles(),
            ('Contributor', 'Member', 'Site Administrator')
        )

    def test_upgrade_2_to_3(self):
        from sll.policy.upgrades import upgrade_2_to_3
        upgrade_2_to_3(self.portal)
        groupstool = getToolByName(self.portal, 'portal_groups')
        self.failIf(groupstool.getGroupById('Reviewers'))
