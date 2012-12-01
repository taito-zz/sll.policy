# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sll.basepolicy.tests.test_setup import get_record
from sll.policy.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package__installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.policy'))

    def test_actions__user__dashboard(self):
        action = getattr(getattr(getToolByName(self.portal, 'portal_actions'), 'user'), 'dashboard')
        self.assertFalse(action.getProperty('visible'))

    def test_actions__user__login(self):
        action = getattr(getattr(getToolByName(self.portal, 'portal_actions'), 'user'), 'login')
        self.assertFalse(action.getProperty('visible'))

    def test_browserlayer(self):
        from sll.policy.browser.interfaces import ISllPolicyLayer
        from plone.browserlayer import utils
        self.failUnless(ISllPolicyLayer in utils.registered_layers())

    def test_metadata__dependency__Products_PloneFormGen(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PloneFormGen'))

    def test_metadata__dependency__Products_PFGExtendedMailAdapter(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PFGExtendedMailAdapter'))

    def test_metadata__dependency__Products_PFGSelectionStringField(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PFGSelectionStringField'))

    def test_metadata__dependency__collective_contentleadimage(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.contentleadimage'))

    def test_metadata__dependency__collective_cropimage(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.cropimage'))

    def test_metadata__dependency__collective_folderlogo(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.folderlogo'))

    def test_metadata__dependency__collective_microsite(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.microsite'))

    def test_metadata__dependency__collective_pfg_payment(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('collective.pfg.payment'))

    def test_metadata__dependency__sll_basepolicy(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.basepolicy'))

    def test_metadata__dependency__sll_carousel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.carousel'))

    def test_metadata__dependency___sll_portlet(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.portlet'))

    def test_metadata__dependency__sll_templates(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('sll.templates'))

    def test_metadata__dependency___sll_theme(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.theme'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(setup.getVersionForProfile('profile-sll.policy:default'), u'43')

    def test_properties_default_page(self):
        self.assertEqual(self.portal.getProperty('default_page'), 'sll-view')

    def test_properties__description(self):
        self.assertEqual(self.portal.getProperty('description'), 'Suomen luonnonsuojeluliitto ry')

    def test_properties__email_from_address(self):
        self.assertEqual(self.portal.getProperty('email_from_address'), 'webmaster@sll.fi')

    def test_properties__email_from_name(self):
        self.assertEqual(self.portal.getProperty('email_from_name'), 'Suomen luonnonsuojeluliitto ry')

    def test_properties__title(self):
        self.assertEqual(self.portal.getProperty('title'), 'Luonnonsuojeluliitto')

    def test_propertiestool__cli_properties__allowed_types(self):
        properties = getToolByName(self.portal, 'portal_properties')
        cli_properties = getattr(properties, 'cli_properties')
        self.assertEqual(cli_properties.getProperty('allowed_types'), ('Document', 'Event', 'FormFolder'))

    def test_registry_record__abita_development_rate__value(self):
        record = get_record('abita.development.rate')
        self.assertEqual(record.value, 5.0)

    def test_registry_record__collective_folderlogo_logo_id__value(self):
        record = get_record('collective.folderlogo.logo_id')
        self.assertEqual(record.value, u'ylapalkin-logo.png')

    def test_security__ISharingPageRole(self):
        from zope.component import getUtilitiesFor
        from plone.app.workflow.interfaces import ISharingPageRole
        roles = sorted([item[0] for item in getUtilitiesFor(ISharingPageRole)])
        self.assertEqual(roles, [u'Contributor', u'Editor', u'Reader', u'Reviewer'])

    def test_security__enable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    def test_uninstall(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.policy'])
        self.assertFalse(installer.isProductInstalled('sll.policy'))
