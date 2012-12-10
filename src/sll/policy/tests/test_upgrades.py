from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from sll.policy.tests.base import IntegrationTestCase
from zope.component import getUtility


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_disable_javascript(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        rid = 'jquery-integration.js'
        resource = javascripts.getResource(rid)
        self.assertTrue(resource.getEnabled())

        from sll.policy.upgrades import disable_javascript
        disable_javascript(self.portal, rid)

        self.assertFalse(resource.getEnabled())

    def test_upgrade_40_to_41(self):
        membership = getToolByName(self.portal, 'portal_membership')
        membership.getMemberById('test_user_1_').manage_changeProperties(visible_ids=False)
        self.assertFalse(membership.getMemberById('test_user_1_').getProperty('visible_ids'))

        from sll.policy.upgrades import upgrade_40_to_41
        upgrade_40_to_41(self.portal)

        self.assertTrue(membership.getMemberById('test_user_1_').getProperty('visible_ids'))

    def test_reset_record_abita_development_rate(self):
        record = getUtility(IRegistry)
        record['abita.development.rate'] = 2.0
        self.assertEqual(record['abita.development.rate'], 2.0)

        from sll.policy.upgrades import reset_record_abita_development_rate
        reset_record_abita_development_rate(self.portal)

        self.assertEqual(record['abita.development.rate'], 5.0)

    def test_unregister_layer_ISLLPolicyLayer__and__register_layer_ISllPolicyLayer(self):
        from sll.policy.browser.interfaces import ISllPolicyLayer
        from plone.browserlayer import utils
        self.assertIn(ISllPolicyLayer, utils.registered_layers())
        from sll.policy.upgrades import unregister_layer_ISLLPolicyLayer
        unregister_layer_ISLLPolicyLayer(self.portal)
        self.assertNotIn(ISllPolicyLayer, utils.registered_layers())
        from sll.policy.upgrades import register_layer_ISllPolicyLayer
        register_layer_ISllPolicyLayer(self.portal)
        self.assertIn(ISllPolicyLayer, utils.registered_layers())
