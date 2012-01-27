# -*- coding: utf-8 -*-

# from Products.CMFCore.utils import getToolByName
# from plone.portlets.interfaces import IPortletAssignmentMapping
# from plone.portlets.interfaces import IPortletManager
# from sll.policy.tests.base import TestCase
# from zope.component import getMultiAdapter
# from zope.component import getUtility

# import unittest2 as unittest


# class TestSetup(TestCase):

#     def afterSetUp(self):
#         self.installer = getToolByName(self.portal, 'portal_quickinstaller')
#         self.properties = getToolByName(self.portal, 'portal_properties')
#         self.ccp = getattr(self.properties, 'collective_cart_properties')
#         self.cppp = getattr(self.properties, 'collective_pfg_payment_properties')
#         self.flp = getattr(self.properties, 'folder_logo_properties')

#     def test_sll_policy_installed(self):
#         self.failUnless(self.installer.isProductInstalled('sll.policy'))

#     def test_is_collective_folderlogo_installed(self):
#         self.failUnless(self.installer.isProductInstalled('collective.folderlogo'))

#     def test_is_collective_pfg_payment_installed(self):
#         self.failUnless(self.installer.isProductInstalled('collective.pfg.payment'))

#     def test_is_collective_cart_core_installed(self):
#         self.failUnless(self.installer.isProductInstalled('collective.cart.core'))

#     def test_is_collective_cart_shipping_installed(self):
#         self.failUnless(self.installer.isProductInstalled('collective.cart.shipping'))

#     def test_is_collective_pfg_showrequest_installed(self):
#         self.failUnless(self.installer.isProductInstalled('collective.pfg.showrequest'))

#     def test_is_plone_form_gen_installed(self):
#         self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

#     def test_is_pfg_extended_mail_adapter_installed(self):
#         self.failUnless(self.installer.isProductInstalled('PFGExtendedMailAdapter'))

#     def test_is_pfg_selection_string_field_installed(self):
#         self.failUnless(self.installer.isProductInstalled('PFGSelectionStringField'))

#     # def test_is_new_ssl_skin_installed(self):
#     #     self.failUnless(self.installer.isProductInstalled('NewSllSkin'))

#     ## browserlayer.xml
#     def test_browserlayer(self):
#         from sll.policy.interfaces import ISLLPolicyLayer
#         from plone.browserlayer import utils
#         self.failUnless(ISLLPolicyLayer in utils.registered_layers())

#     ## properties.xml
#     def test_portal_email_from_name(self):
#         self.assertEquals('Luonnonsuojeluliitto', self.portal.getProperty('title'))
#         self.assertEquals('Suomen luonnonsuojeluliitto ry', self.portal.getProperty('description'))
#         self.assertEquals("front-page", self.portal.getProperty('default_page'))
#         self.assertEquals('webmaster@sll.fi', self.portal.getProperty('email_from_address'))
#         self.assertEquals('Suomen luonnonsuojeluliitto ry', self.portal.getProperty('email_from_name'))

#     ## propertiestool.xml
#     def test_collective_cart_properties(self):
#         self.assertEquals('EUR', self.ccp.getProperty('currency'))
#         self.assertEquals('€', self.ccp.getProperty('currency_symbol'))
#         self.assertEquals('Behind', self.ccp.getProperty('symbol_location'))
#         self.assertEquals(('Document',), self.ccp.getProperty('content_types'))
#         self.assertEquals('Select', self.ccp.getProperty('quantity_method'))

#     def test_collective_pfg_payment_properties(self):
#         names = (
#             'MERCHANT_ID',
#             'AMOUNT',
#             'ORDER_NUMBER',
#             'REFERENCE_NUMBER',
#             'ORDER_DESCRIPTION',
#             'CURRENCY',
#             'RETURN_ADDRESS',
#             'CANCEL_ADDRESS',
#             'PENDING_ADDRESS',
#             'NOTIFY_ADDRESS',
#             'TYPE',
#             'CULTURE',
#             'PRESELECTED_METHOD',
#             'MODE',
#             'VISIBLE_METHODS',
#             'GROUP'
#         )
#         self.assertEquals(names, self.cppp.getProperty('fields'))
#         self.assertEquals('6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ', self.cppp.getProperty('mac'))
#         self.assertEquals('|', self.cppp.getProperty('separator'))
#         self.assertEquals(True, self.cppp.getProperty('capital'))

#     def test_folder_logo_properties(self):
#         self.assertEquals('ylapalkin-logo.png', self.flp.getProperty('logo_id'))
#         self.assertEquals('#5b905b', self.flp.getProperty('background_color'))
#         self.assertEquals('ylapalkin-tausta.png', self.flp.getProperty('background_image_id'))


#     def test_left_portlet(self):
#         column = getUtility(IPortletManager, name=u"plone.leftcolumn")
#         assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
#         self.failIf(u'Cart' in assignable.keys())

#     def test_right_portlet(self):
#         column = getUtility(IPortletManager, name=u"plone.rightcolumn")
#         assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
#         self.failUnless(u'Cart' in assignable.keys())

#     ## Uninstalling
#     def test_uninstall(self):
# #        self.installer.uninstallProducts(['sll.policy'])
# #        self.failUnless(not self.installer.isProductInstalled('sll.policy'))
# #        ids = [action.id for action in self.controlpanel.listActions()]
# #        self.failUnless('collective_pfg_payment_config' not in ids)
# #        self.failIf(hasattr(self.actions.object_buttons, 'make_order_number_aware'))
# #        self.failIf(hasattr(self.actions.object_buttons, 'make_order_number_unaware'))
# #        self.failIf(hasattr(self.actions.object, 'edit_order_number'))
#         pass

from sll.policy.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_sll_policy_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.policy'))

    def test_dependencies_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.theme'))
        self.failUnless(installer.isProductInstalled('inicie.cropimage'))
        self.failUnless(installer.isProductInstalled('collective.contentleadimage'))
        self.failUnless(installer.isProductInstalled('PloneFormGen'))

    ## actions.xml
    def test_dashboard(self):
        tool = getToolByName(self.portal, 'portal_actions')
        actions = getattr(tool, 'user')
        action = getattr(actions, 'dashboard')
        self.assertFalse(action.getProperty('visible'))

    ## properties.xml
    def test_properties__title(self):
        self.assertEqual(
            self.portal.getProperty('title'),
            'Luonnonsuojeluliitto'
        )

    def test_properties__description(self):
        self.assertEqual(
            self.portal.getProperty('description'),
            'Suomen luonnonsuojeluliitto ry'
        )

    def test_properties__email_from_address(self):
        self.assertEqual(
            self.portal.getProperty('email_from_address'),
            'webmaster@sll.fi'
        )

    def test_properties__email_from_name(self):
        self.assertEqual(
            self.portal.getProperty('email_from_name'),
            'Suomen luonnonsuojeluliitto ry'
        )

    ## propertiestool.xml
    def test_disable_nonfolderish_sections(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertTrue(site_props.getProperty('disable_nonfolderish_sections'))

    def test_default_language(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('default_language'), 'fi')

    def test_enable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    # def test_propertiestool_site_properties__disable_nonfolderish_sections(self):
    #     properties = getToolByName(self.portal, 'portal_properties')
    #     site_properties = getattr(properties, 'site_properties')
    #     self.assertTrue(site_properties.getProperty('disable_nonfolderish_sections'))

    # def test_propertiestool_site_properties__use_email_as_login(self):
    #     properties = getToolByName(self.portal, 'portal_properties')
    #     site_properties = getattr(properties, 'site_properties')
    #     self.assertTrue(site_properties.getProperty('use_email_as_login'))

    def test_propertiestool_site_properties__icon_visibility(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('icon_visibility'),
            'authenticated'
        )

    def test_propertiestool_site_properties__exposeDCMetaTags(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('exposeDCMetaTags'))

    def test_propertiestool_site_properties__enable_sitemap(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('enable_sitemap'))

    def test_propertiestool_navtree_properties__metaTypesNotToList(self):
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        contents = ('Image', 'Event', 'Document', 'Topic', 'Link', 'File', 'News Item')
        for content in contents:
            self.assertTrue(content in navtree_properties.getProperty('metaTypesNotToList'))

    def test_propertiestool_cli_properties__allowed_types(self):
        properties = getToolByName(self.portal, 'portal_properties')
        cli_properties = getattr(properties, 'cli_properties')
        self.assertEqual(
            cli_properties.getProperty('allowed_types'),
            ('Document', 'Event')
        )

    # def test_tinymce__autoresize(self):
    #     tinymce = getToolByName(self.portal, 'portal_tinymce')
    #     self.assertTrue(tinymce.autoresize)

    def test_tinymce__link_using_uids(self):
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(tinymce.link_using_uids)

    # def test_tinymce__toolbar_forecolor(self):
    #     tinymce = getToolByName(self.portal, 'portal_tinymce')
    #     self.assertTrue(tinymce.toolbar_forecolor)

    # def test_tinymce__toolbar_backcolor(self):
    #     tinymce = getToolByName(self.portal, 'portal_tinymce')
    #     self.assertTrue(tinymce.toolbar_backcolor)

    # def test_jsregistry__kukit(self):
    #     javascripts = getToolByName(self.portal, 'portal_javascripts')
    #     self.assertFalse(javascripts.getResource("++resource++kukit.js").getAuthenticated())

    ## portlets.xml
    def test_portlets__navigation_removed_from_left_column(self):
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('navigation' in assignable.keys())

    def test_portlets__news_removed_from_right_column(self):
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('news' in assignable.keys())

    def test_portlets__events_removed_from_right_column(self):
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('events' in assignable.keys())

    ## browserlayer.xml
    def test_browserlayer(self):
        from sll.policy.browser.interfaces import ISllPolicyLayer
        from plone.browserlayer import utils
        self.failUnless(ISllPolicyLayer in utils.registered_layers())

    def test_disable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    def test_theme__enabled(self):
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertTrue(settings.enabled)

    def test_theme__rules(self):
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(
            settings.rules,
            "/++theme++sll.theme/rules.xml"
        )

    def test_theme__absolutePrefix(self):
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(
            settings.absolutePrefix,
            "/++theme++sll.theme"
        )

    def test_ajankohtaista_folder_created(self):
        folder = self.portal['ajankohtaista']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Ajankohtaista')

    def test_tapahtumat_folder_created(self):
        folder = self.portal['tapahtumat']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Tapahtumat')

    def test_mita_me_teemme_folder_created(self):
        folder = self.portal['mita-me-teemme']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Mitä me teemme')

    def test_mita_sina_voit_tehda_folder_created(self):
        folder = self.portal['mita-sina-voit-tehda']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Mitä sinä voit tehdä')

    def test_liity_folder_created(self):
        folder = self.portal['liity']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Liity')

    def test_lahjoita_folder_created(self):
        folder = self.portal['lahjoita']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Lahjoita')

    def test_jarjesto_folder_created(self):
        folder = self.portal['jarjesto']
        self.assertFalse(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Järjestö')

    def test_medialle_folder_created(self):
        folder = self.portal['medialle']
        self.assertTrue(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Medialle')

    def test_yhteistiedot_folder_created(self):
        folder = self.portal['yhteistiedot']
        self.assertTrue(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Yhteistiedot')

    def test_english_folder_created(self):
        folder = self.portal['english']
        self.assertTrue(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'English')

    def test_svenska_folder_created(self):
        folder = self.portal['svenska']
        self.assertTrue(folder.exclude_from_nav())
        self.assertEqual(folder.Title(), 'Svenska')

    def test_Member_folder_exclude_from_nav(self):
        folder = self.portal['Members']
        self.assertTrue(folder.exclude_from_nav())

    def test_news_folder_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['news'])

    def test_events_folder_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['events'])

    def test_inicie_cropimage_ids(self):
        registry = getUtility(IRegistry)
        self.assertEqual(
            registry['inicie.cropimage.ids'],
            [
                {
                    'ratio_height': 15.0,
                    'ratio_width': 17.0,
                    'max_width': 170.0,
                    'min_height': 150.0,
                    'max_height': 150.0,
                    'min_width': 170.0,
                    'id': 'feed'
                }
            ]
        )

    def test_uninstall(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.policy'])
        self.failIf(installer.isProductInstalled('sll.policy'))
