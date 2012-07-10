# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sll.policy.tests.base import IntegrationTestCase
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
        self.failUnless(installer.isProductInstalled('sll.templates'))
        self.failUnless(installer.isProductInstalled('collective.cropimage'))
        self.failUnless(installer.isProductInstalled('collective.contentleadimage'))
        self.failUnless(installer.isProductInstalled('PloneFormGen'))

    def test_installed__sll_carousel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.carousel'))

    def test_abita_development_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.development'))

    def test_sll_portlet_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.portlet'))

    def test_sll_theme_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.theme'))

    def test_actions__dashboard(self):
        tool = getToolByName(self.portal, 'portal_actions')
        actions = getattr(tool, 'user')
        action = getattr(actions, 'dashboard')
        self.assertFalse(action.getProperty('visible'))

    def test_actions__login(self):
        tool = getToolByName(self.portal, 'portal_actions')
        actions = getattr(tool, 'user')
        action = getattr(actions, 'login')
        self.assertFalse(action.getProperty('visible'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-sll.policy:default'),
            u'35'
        )

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

    def test_properties_default_page(self):
        self.assertEqual(
            self.portal.getProperty('default_page'),
            'sll-view'
        )

    ## propertiestool.xml
    def test_propertiestool_site_properties__default_editor(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('default_editor'),
            'TinyMCE'
        )

    def test_default_language(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('default_language'), 'fi')

    def test_enable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    def test_propertiestool_site_properties__external_links_open_new_window(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('external_links_open_new_window'),
            'true'
        )

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
        contents = ('Document', 'Folder', 'FormFolder', 'News Item')
        for content in contents:
            self.assertFalse(content in navtree_properties.getProperty('metaTypesNotToList'))
        contents = ('Event', 'File', 'Image', 'Link', 'Topic')
        for content in contents:
            self.assertTrue(content in navtree_properties.getProperty('metaTypesNotToList'))

    def test_propertiestool_navtree_properties__enable_wf_state_filtering(self):
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        self.assertFalse(navtree_properties.getProperty('enable_wf_state_filtering'))

    def test_propertiestool_cli_properties__allowed_types(self):
        properties = getToolByName(self.portal, 'portal_properties')
        cli_properties = getattr(properties, 'cli_properties')
        self.assertEqual(
            cli_properties.getProperty('allowed_types'),
            ('Document', 'Event', 'FormFolder')
        )

    def test_rolemap__Manage_portlets__rolesOfPermission(self):
        permission = "Portlets: Manage portlets"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Editor',
                'Manager',
                'Site Administrator',
            ]
        )

    def test_rolemap__Manage_portlets__acquiredRolesAreUsedBy(self):
        permission = "Portlets: Manage portlets"
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )

    def test_rolemap__Manage_own_portlets__rolesOfPermission(self):
        permission = "Portlets: Manage own portlets"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Editor',
                'Manager',
                'Site Administrator',
            ]
        )

    def test_rolemap__Manage_own_portlets__acquiredRolesAreUsedBy(self):
        permission = "Portlets: Manage own portlets"
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )

    def test_rolemap__Add_collection_portlet__rolesOfPermission(self):
        permission = "plone.portlet.collection: Add collection portlet"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Editor',
                'Manager',
                'Site Administrator',
            ]
        )

    def test_rolemap__Add_collection_portlet__acquiredRolesAreUsedBy(self):
        permission = "plone.portlet.collection: Add collection portlet"
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )

    def test_rolemap__Add_static_portlet__rolesOfPermission(self):
        permission = "plone.portlet.static: Add static portlet"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Editor',
                'Manager',
                'Site Administrator',
            ]
        )

    def test_rolemap__Add_static_portlet__acquiredRolesAreUsedBy(self):
        permission = "plone.portlet.static: Add static portlet"
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )

    def test_tinymce__link_using_uids(self):
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(tinymce.link_using_uids)

    # def test_tinymce__toolbar_forecolor(self):
    #     tinymce = getToolByName(self.portal, 'portal_tinymce')
    #     self.assertTrue(tinymce.toolbar_forecolor)

    # def test_tinymce__toolbar_backcolor(self):
    #     tinymce = getToolByName(self.portal, 'portal_tinymce')
    #     self.assertTrue(tinymce.toolbar_backcolor)

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

    # def test_theme__enabled(self):
    #     registry = getUtility(IRegistry)
    #     from plone.app.theming.interfaces import IThemeSettings
    #     settings = registry.forInterface(IThemeSettings)
    #     self.assertTrue(settings.enabled)

    # def test_theme__rules(self):
    #     registry = getUtility(IRegistry)
    #     from plone.app.theming.interfaces import IThemeSettings
    #     settings = registry.forInterface(IThemeSettings)
    #     self.assertEqual(
    #         settings.rules,
    #         "/++theme++sll.theme/rules.xml"
    #     )

    # def test_theme__absolutePrefix(self):
    #     registry = getUtility(IRegistry)
    #     from plone.app.theming.interfaces import IThemeSettings
    #     settings = registry.forInterface(IThemeSettings)
    #     self.assertEqual(
    #         settings.absolutePrefix,
    #         "/++theme++sll.theme"
    #     )

    ## rolemap.xml
    def test_content_rule(self):
        items = [
            item['name'] for item in self.portal.rolesOfPermission(
                "Content rules: Manage rules"
            ) if item['selected'] == 'SELECTED'
        ]
        self.assertEqual(len(items), 2)
        permissions = ['Site Administrator', 'Manager']
        for item in items:
            self.assertTrue(item in permissions)
        self.assertFalse(
            self.portal.acquiredRolesAreUsedBy(
                "Content rules: Manage rules"
            )
        )

    def test_ISharingPageRole(self):
        from zope.component import getUtilitiesFor
        from plone.app.workflow.interfaces import ISharingPageRole
        res = []
        for name, utility in getUtilitiesFor(ISharingPageRole):
            res.append(name)
        self.assertEqual(
            res,
            [u'Contributor', u'Reviewer', u'Editor', u'Reader']
        )

    def test_Members_folders_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['Members'])

    def test_news_folders_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['news'])

    def test_events_folders_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['events'])

    def test_setuphandlers__set_collections(self):
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        self.assertEqual(
            registry['collective.searchevent.collections'],
            [
                {
                    'id': 'SLL',
                    'limit': 10,
                    'paths': set(
                        [
                            'sll/etela-hame',
                            'sll/etela-karjala',
                            'sll/etela-savo',
                            'sll/kainuu',
                            'sll/keski-suomi',
                            'sll/kymenlaakso',
                            'sll/lappi',
                            'sll/pirkanmaa',
                            'sll/pohjanmaa',
                            'sll/pohjois-karjala',
                            'sll/pohjois-pohjanmaa',
                            'sll/satakunta',
                            'sll/uusimaa',
                            'sll/varsinais-suomi',
                        ]
                    ),
                    'tags': ['Kokous', 'Kurssi', 'Retki', 'Talkoot'],
                }
            ]
        )

    def test_setuphanlders__folder__tapahtumat__layout(self):
        folder = self.portal['tapahtumat']
        self.assertEqual(
            folder.getLayout(),
            'search-results'
        )

    def test_uninstall(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.policy'])
        self.failIf(installer.isProductInstalled('sll.policy'))
