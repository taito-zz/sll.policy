from Products.CMFCore.utils import getToolByName
from sll.policy.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    # def test_upgrade_13_to_14(self):
    #     portal_properties = getToolByName(self.portal, 'portal_properties')
    #     navtree_properties = getattr(portal_properties, 'navtree_properties')
    #     self.assertEqual(navtree_properties.getProperty('topLevel'), 0)

    #     navtree_properties._updateProperty('topLevel', 1)
    #     self.assertEqual(navtree_properties.getProperty('topLevel'), 1)

    #     from sll.policy.upgrades import upgrade_13_to_14
    #     upgrade_13_to_14(self.portal)

    #     self.assertEqual(navtree_properties.getProperty('topLevel'), 0)

    # def test_upgrade_14_to_15__collective_cropimage_ids(self):
    #     from sll.policy.upgrades import upgrade_14_to_15
    #     upgrade_14_to_15(self.portal)
    #     from plone.registry.interfaces import IRegistry
    #     from zope.component import getUtility
    #     registry = getUtility(IRegistry)
    #     self.assertEqual(
    #         registry['collective.cropimage.ids'],
    #         [
    #             {
    #                 'ratio_height': 15.0,
    #                 'ratio_width': 17.0,
    #                 'max_width': 170.0,
    #                 'min_height': 150.0,
    #                 'max_height': 150.0,
    #                 'min_width': 170.0,
    #                 'id': 'feed'
    #             }
    #         ]
    #     )

    # def test_upgrades_15_to_16(self):
    #     portal_skins = getToolByName(self.portal, 'portal_skins')
    #     custom = portal_skins['custom']
    #     from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate
    #     manage_addPageTemplate(custom, 'aaa', text='')
    #     manage_addPageTemplate(custom, 'portlet_kartta', text='')
    #     from sll.policy.upgrades import upgrade_15_to_16
    #     upgrade_15_to_16(self.portal)
    #     installer = getToolByName(self.portal, 'portal_quickinstaller')
    #     self.assertFalse(installer.isProductInstalled('NewSllSkin'))
    #     self.assertEqual(portal_skins.default_skin, 'Sunburst Theme')
    #     self.assertFalse('NewSllSkin' in portal_skins.getSkinSelections())
    #     self.assertEqual(custom.objectIds(), ['aaa'])

    # def test_upgrades_16_to_17(self):
    #     from zope.component import getUtility
    #     from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
    #     storage = getUtility(IViewletSettingsStorage)
    #     storage.setHidden('plone.portaltop', '*', (u'plone.header',))
    #     self.assertTrue(u'plone.header' in storage.getHidden('plone.portaltop', '*'))
    #     storage.setHidden('plone.portalheader', '*', (u'plone.logo',))
    #     self.assertTrue(u'plone.logo' in storage.getHidden('plone.portalheader', '*'))
    #     from sll.policy.upgrades import upgrade_16_to_17
    #     upgrade_16_to_17(self.portal)
    #     self.assertEqual(
    #         storage.getOrder('plone.portaltop', '*'),
    #         (
    #             u'plone.header',
    #         )
    #     )
    #     self.assertFalse(storage.getHidden('plone.portaltop', '*'))
    #     self.assertEqual(
    #         storage.getOrder('plone.portalheader', '*'),
    #         (
    #             u'plone.skip_links',
    #             u'plone.personal_bar',
    #             u'plone.site_actions',
    #             u'plone.app.i18n.locales.languageselector',
    #             u'plone.searchbox',
    #             u'plone.logo',
    #             u'plone.global_sections',
    #         )
    #     )
    #     self.assertEqual(storage.getHidden('plone.portalheader', '*'), ())

    # def test_upgrades_17_to_18(self):
    #     tausta = self.portal[
    #         self.portal.invokeFactory('Document', 'ylapalkin-tausta.png')
    #     ]
    #     tausta.reindexObject()
    #     self.failUnless(self.portal['ylapalkin-tausta.png'])
    #     properties = getToolByName(self.portal, 'portal_properties')
    #     folder_logo_properties = getattr(properties, 'folder_logo_properties')
    #     folder_logo_properties.manage_changeProperties(
    #         background_color='white',
    #         background_image_id='image',
    #     )
    #     self.assertEqual(
    #         folder_logo_properties.getProperty('background_color'),
    #         'white'
    #     )
    #     self.assertEqual(
    #         folder_logo_properties.getProperty('background_image_id'),
    #         'image'
    #     )
    #     from sll.policy.upgrades import upgrade_17_to_18
    #     upgrade_17_to_18(self.portal)
    #     self.assertRaises(KeyError, lambda: self.portal['ylapalkin-tausta.png'])
    #     self.assertEqual(
    #         folder_logo_properties.getProperty('background_color'),
    #         ''
    #     )
    #     self.assertEqual(
    #         folder_logo_properties.getProperty('background_image_id'),
    #         ''
    #     )

    # def test_upgrades_18_to_19(self):
    #     installer = getToolByName(self.portal, 'portal_quickinstaller')
    #     product = 'plonetheme.classic'
    #     installer.installProduct(product)
    #     self.assertTrue(installer.isProductInstalled(product))
    #     from sll.policy.upgrades import upgrade_18_to_19
    #     upgrade_18_to_19(self.portal)
    #     self.assertFalse(installer.isProductInstalled(product))

    # def test_upgrades_19_to_20(self):
    #     from zope.component import getUtility
    #     from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
    #     storage = getUtility(IViewletSettingsStorage)
    #     storage.setHidden('plone.portalfooter', '*', (u'plone.footer',))
    #     self.assertEqual(storage.getHidden('plone.portalfooter', '*'), (u'plone.footer',))
    #     from sll.policy.upgrades import upgrade_19_to_20
    #     upgrade_19_to_20(self.portal)
    #     self.assertEqual(
    #         storage.getHidden('plone.portalfooter', '*'),
    #         (
    #             u'plone.colophon',
    #             u'plone.site_actions',
    #         )
    #     )
    #     self.assertEqual(
    #         storage.getOrder('plone.portalheader', '*'),
    #         (
    #             u'plone.skip_links',
    #             u'plone.personal_bar',
    #             u'plone.site_actions',
    #             u'plone.app.i18n.locales.languageselector',
    #             u'plone.searchbox',
    #             u'plone.logo',
    #             u'plone.global_sections',
    #         )
    #     )

    # def test_upgrades_21_to_22(self):
    #     folder01 = self.portal[
    #         self.portal.invokeFactory(
    #             'Folder',
    #             'folder01',
    #         )
    #     ]
    #     folder01.setExcludeFromNav(False)
    #     folder01.reindexObject()

    #     folder02 = folder01[
    #         folder01.invokeFactory(
    #             'Folder',
    #             'folder02',
    #         )
    #     ]
    #     folder02.setExcludeFromNav(False)
    #     folder02.reindexObject()

    #     liity = self.portal[
    #         self.portal.invokeFactory(
    #             'Folder',
    #             'liity-uusi',
    #         )
    #     ]
    #     liity.setExcludeFromNav(True)
    #     liity.reindexObject()

    #     self.assertFalse(folder01.getExcludeFromNav())
    #     self.assertTrue(liity.getExcludeFromNav())

    #     from sll.policy.upgrades import upgrade_21_to_22
    #     upgrade_21_to_22(self.portal)
    #     self.assertTrue(folder01.getExcludeFromNav())
    #     self.assertFalse(folder02.getExcludeFromNav())
    #     self.assertFalse(liity.getExcludeFromNav())

    # def test_upgrades_26_to_27(self):
    #     portal_properties = getToolByName(self.portal, 'portal_properties')
    #     site_properties = getattr(portal_properties, 'site_properties')
    #     site_properties.manage_changeProperties(mark_special_links="true")

    #     self.assertEqual(site_properties.getProperty('mark_special_links'), 'true')

    #     from sll.policy.upgrades import upgrade_26_to_27
    #     upgrade_26_to_27(self.portal)

    #     self.assertEqual(site_properties.getProperty('mark_special_links'), 'false')

    # def test_upgrades_27_to_28(self):
    #     portal_actions = getToolByName(self.portal, 'portal_actions')
    #     actions = getattr(portal_actions, 'user')
    #     action = getattr(actions, 'login')
    #     action.manage_changeProperties(visible=True)
    #     self.assertTrue(action.getProperty('visible'))

    #     from sll.policy.upgrades import upgrade_27_to_28
    #     upgrade_27_to_28(self.portal)

    #     self.assertFalse(action.getProperty('visible'))

    # def test_upgrades_28_to_29(self):
    #     piiri = self.portal[
    #         self.portal.invokeFactory('Folder', 'lappi')
    #     ]
    #     piiri.reindexObject()
    #     ylitornio = piiri[
    #         piiri.invokeFactory('Folder', 'ylitornio')
    #     ]
    #     ylitornio.reindexObject()
    #     aaa = piiri[
    #         piiri.invokeFactory('Folder', 'aaa')
    #     ]
    #     aaa.reindexObject()

    #     from plone.app.layout.navigation.interfaces import INavigationRoot
    #     self.assertFalse(INavigationRoot.providedBy(ylitornio))
    #     self.assertFalse(INavigationRoot.providedBy(aaa))

    #     from sll.policy.upgrades import upgrade_28_to_29
    #     upgrade_28_to_29(self.portal)

    #     self.assertTrue(INavigationRoot.providedBy(ylitornio))
    #     self.assertFalse(INavigationRoot.providedBy(aaa))

    def test_upgrades_30_to_31(self):

        permission = "plone.portlet.collection: Add collection portlet"
        self.portal.manage_permission(permission, roles=['Manager'])
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Manager',
            ]
        )
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            ''
        )

        permission = "plone.portlet.static: Add static portlet"
        self.portal.manage_permission(permission, roles=['Manager'])
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Manager',
            ]
        )
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            ''
        )

        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        site_properties.manage_changeProperties(default_editor=None, external_links_open_new_window='false')
        self.failIf(site_properties.getProperty('default_editor'))
        self.assertEqual(
                site_properties.getProperty('external_links_open_new_window'),
                'false'
        )

        workflow = getToolByName(self.portal, 'portal_workflow')
        workflow.setChainForPortalTypes(('Image', ), 'two_states_workflow')
        image = self.portal[
            self.portal.invokeFactory(
                'Image',
                'image',
            )
        ]
        self.assertEqual(
            workflow.getInfoFor(image, "review_state"),
            'private'
        )

        installer = getToolByName(self.portal, 'portal_quickinstaller')
        packages = ['abita.development', 'collective.searchevent']
        installer.uninstallProducts(['abita.development', 'collective.searchevent'])
        for pac in packages:
            self.failIf(installer.isProductInstalled(pac))

        from sll.policy.upgrades import upgrade_30_to_31
        upgrade_30_to_31(self.portal)

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
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )

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
        self.assertEqual(
            self.portal.acquiredRolesAreUsedBy(permission),
            'CHECKED'
        )
        self.assertEqual(
            site_properties.getProperty('default_editor'),
            'TinyMCE'
        )
        self.assertEqual(
                site_properties.getProperty('external_links_open_new_window'),
                'true'
        )

        from Products.CMFCore.WorkflowCore import WorkflowException
        self.assertRaises(
            WorkflowException,
            lambda: workflow.getInfoFor(image, "review_state")
        )
        workflow.setChainForPortalTypes(('Image', ), 'two_states_workflow')
        self.assertEqual(
            workflow.getInfoFor(image, "review_state"),
            'published'
        )

        for pac in packages:
            self.failUnless(installer.isProductInstalled(pac))

    def test_upgrades_31_to_32(self):

        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        registry['collective.searchevent.collections'] = []
        self.assertEqual(
            registry['collective.searchevent.collections'],
            []
        )

        tapahtumat = self.portal['tapahtumat']
        tapahtumat.setLayout('some-view')
        self.assertEqual(
            tapahtumat.getLayout(),
            'some-view'
        )

        from sll.policy.upgrades import upgrade_31_to_32
        upgrade_31_to_32(self.portal)

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

        self.assertEqual(
            tapahtumat.getLayout(),
            'search-results'
        )

    def test_upgrades_32_to_33(self):
        folder = self.portal[
            self.portal.invokeFactory(
                'Folder',
                'folder',
            )
        ]
        folder.reindexObject()
        subject = folder.schema.get('subject').schemata
        self.assertEqual(subject, 'categorization')
        related_items = folder.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'categorization')
        folder.schema.changeSchemataForField('excludeFromNav', 'categorization')
        exclude_from_nav = folder.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'categorization')

        document = self.portal[
            self.portal.invokeFactory(
                'Document',
                'document',
            )
        ]
        document.reindexObject()
        subject = document.schema.get('subject').schemata
        self.assertEqual(subject, 'categorization')
        document.schema.changeSchemataForField('relatedItems', 'categorization')
        related_items = document.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'categorization')
        document.schema.changeSchemataForField('excludeFromNav', 'categorization')
        exclude_from_nav = document.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'categorization')

        event = self.portal[
            self.portal.invokeFactory(
                'Event',
                'event',
            )
        ]
        event.reindexObject()
        event.schema.changeSchemataForField('subject', 'categorization')
        subject = event.schema.get('subject').schemata
        self.assertEqual(subject, 'categorization')
        event.schema.changeSchemataForField('relatedItems', 'categorization')
        related_items = event.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'categorization')
        event.schema.changeSchemataForField('excludeFromNav', 'categorization')
        exclude_from_nav = event.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'categorization')

        properties = getToolByName(self.portal, 'portal_properties')
        cli_properties = getattr(properties, 'cli_properties')
        cli_properties.manage_changeProperties(allowed_types=('Document', 'Event'))
        self.assertEqual(
            cli_properties.getProperty('allowed_types'),
            ('Document', 'Event')
        )

        from sll.policy.upgrades import upgrade_32_to_33
        upgrade_32_to_33(self.portal)

        subject = folder.schema.get('subject').schemata
        self.assertEqual(subject, 'categorization')
        related_items = folder.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'categorization')
        exclude_from_nav = folder.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'default')

        subject = document.schema.get('subject').schemata
        self.assertEqual(subject, 'categorization')
        related_items = document.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'default')
        exclude_from_nav = document.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'default')

        subject = event.schema.get('subject').schemata
        self.assertEqual(subject, 'default')
        related_items = event.schema.get('relatedItems').schemata
        self.assertEqual(related_items, 'default')
        exclude_from_nav = event.schema.get('excludeFromNav').schemata
        self.assertEqual(exclude_from_nav, 'default')

        self.assertEqual(
            cli_properties.getProperty('allowed_types'),
            ('Document', 'Event', 'FormFolder')
        )
