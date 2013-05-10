from plone.registry.interfaces import IRegistry
from sll.policy.tests.base import IntegrationTestCase
from zope.component import getUtility


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

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

    def test_excludeFromNav(self):
        uusimaa = self.portal[self.portal.invokeFactory('Folder', 'uusimaa')]
        kannanotot = uusimaa[uusimaa.invokeFactory('Folder', 'kannanotot')]
        folder1 = kannanotot[kannanotot.invokeFactory('Folder', 'folder1')]
        folder2 = folder1[folder1.invokeFactory('Folder', 'folder2')]
        self.assertFalse(kannanotot.getExcludeFromNav())
        self.assertFalse(folder1.getExcludeFromNav())
        self.assertFalse(folder2.getExcludeFromNav())

        from sll.policy.upgrades import excludeFromNav
        excludeFromNav(self.portal)

        self.assertFalse(kannanotot.getExcludeFromNav())
        self.assertTrue(folder1.getExcludeFromNav())
        self.assertTrue(folder2.getExcludeFromNav())
