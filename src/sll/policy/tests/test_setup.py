# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from sll.policy.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_sll_policy_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.policy'))

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

    def test_jsregistry__popupforms(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        resource = javascripts.getResource('popupforms.js')
        self.assertFalse(resource.getEnabled())

    def test_mailhost__smtp_host(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_host, 'sll.fi')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 25)

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(setup.getVersionForProfile('profile-sll.policy:default'), u'41')

    def test_metadata__dependency__Products_PloneFormGen(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PloneFormGen'))

    def test_metadata__dependency__Products_PFGExtendedMailAdapter(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PFGExtendedMailAdapter'))

    def test_metadata__dependency__Products_PFGSelectionStringField(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('PFGSelectionStringField'))

    def test_metadata__dependency___abita_development(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.development'))

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

    def test_metadata__dependency___hexagonit_socialbutton(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('hexagonit.socialbutton'))

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

    ## properties.xml
    def test_properties__title(self):
        self.assertEqual(
            self.portal.getProperty('title'), 'Luonnonsuojeluliitto')

    def test_properties__description(self):
        self.assertEqual(
            self.portal.getProperty('description'),
            'Suomen luonnonsuojeluliitto ry')

    def test_properties__email_from_address(self):
        self.assertEqual(
            self.portal.getProperty('email_from_address'),
            'webmaster@sll.fi')

    def test_properties__email_from_name(self):
        self.assertEqual(
            self.portal.getProperty('email_from_name'),
            'Suomen luonnonsuojeluliitto ry')

    def test_properties_default_page(self):
        self.assertEqual(
            self.portal.getProperty('default_page'),
            'sll-view')

    def test_properties_validate_email(self):
        self.assertTrue(self.portal.getProperty('validate_email'))

    ## propertiestool.xml
    def test_propertiestool_site_properties__default_editor(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('default_editor'),
            'TinyMCE')

    def test_default_language(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('default_language'), 'fi')

    def test_site_properties__disable_nonfolderish_sections(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertFalse(site_props.getProperty('disable_nonfolderish_sections'))

    def test_enable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    def test_propertiestool_site_properties__external_links_open_new_window(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('external_links_open_new_window'),
            'true')

    def test_propertiestool_site_properties__icon_visibility(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertEqual(
            site_properties.getProperty('icon_visibility'),
            'authenticated')

    def test_propertiestool_site_properties__exposeDCMetaTags(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('exposeDCMetaTags'))

    def test_propertiestool_site_properties__enable_link_integrity_checks(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('enable_link_integrity_checks'))

    def test_propertiestool_site_properties__enable_sitemap(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('enable_sitemap'))

    def test_propertiestool_site_properties__types_not_searched(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        contents = ('Collection', 'Topic')
        for content in contents:
            self.assertIn(content, site_properties.getProperty('types_not_searched'))

    def test_propertiestool_site_properties__visible_ids(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertTrue(site_properties.getProperty('visible_ids'))

    def test_propertiestool_navtree_properties__metaTypesNotToList(self):
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        contents = ('Document', 'Folder', 'FormFolder', 'News Item')
        for content in contents:
            self.assertFalse(content in navtree_properties.getProperty('metaTypesNotToList'))
        contents = ('Collection', 'Event', 'File', 'Image', 'Link', 'Topic')
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
            ('Document', 'Event', 'FormFolder'))

    def get_record(self, name):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        return getUtility(IRegistry).records.get(name)

    def test_registry_record_hexagonit_socialbutton_codes(self):
        record = self.get_record('hexagonit.socialbutton.codes')
        self.assertEqual(record.value, {
            u'twitter': {u'code_text': u'<a class="social-button twitter" title="Twitter" href="https://twitter.com/share?text=${title}?url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/twitter.gif" />\n</a>'},
            u'facebook': {u'code_text': u'<a class="social-button facebook" title="Facebook" target="_blank" href="http://www.facebook.com/sharer.php?t=${title}&u=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/facebook.gif" />\n</a>'},
            u'google-plus': {u'code_text': u'<a class="social-button googleplus" title="Google+" href="https://plusone.google.com/_/+1/confirm?hl=${lang}&title=${title}&url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/google-plus.gif" />\n</a>'},
        })

    def test_registry_record_hexagonit_socialbutton_config(self):
        record = self.get_record('hexagonit.socialbutton.config')
        self.assertEqual(record.value, {
            u'twitter': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'facebook': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'google-plus': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
        })

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
            'CHECKED')

    def setuphanders__set_firstweekday(self):
        calendar = getToolByName(self.portal, 'portal_calendar')
        self.assertEqual(calendar.firstweekday, 0)

    def test_tinymce__link_using_uids(self):
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(tinymce.link_using_uids)

    def get_ctype(self, name):
        """Returns content type info.

        :param name: Name of content type.
        :type name: test_types__Plone_Site__filter_content_types
        """
        types = getToolByName(self.portal, 'portal_types')
        return types.getTypeInfo(name)

    # def test_types__Plone_Site__filter_content_types(self):
    #     ctype = self.get_ctype('Plone Site')
    #     self.assertTrue(ctype.filter_content_types)

    # def test_types__Plone_Site__allowed_content_types(self):
    #     ctype = self.get_ctype('Plone Site')
    #     self.assertEqual(ctype.allowed_content_types, (
    #         'Carousel Banner',
    #         'Collection',
    #         'Document',
    #         'Event',
    #         'File',
    #         'Folder',
    #         'FormFolder',
    #         'Image',
    #         'Link',
    #         'News Item',
    #         'collective.cart.shopping.Shop'))

    def test_portlets__news_removed_from_right_column(self):
        from plone.portlets.interfaces import IPortletAssignmentMapping
        from plone.portlets.interfaces import IPortletManager
        from zope.component import getMultiAdapter
        from zope.component import getUtility
        column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('news' in assignable.keys())

    def test_portlets__events_removed_from_right_column(self):
        from plone.portlets.interfaces import IPortletAssignmentMapping
        from plone.portlets.interfaces import IPortletManager
        from zope.component import getMultiAdapter
        from zope.component import getUtility
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