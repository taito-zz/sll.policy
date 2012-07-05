from Products.CMFCore.utils import getToolByName
from sll.policy.tests.base import IntegrationTestCase

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

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

    def test_disable_javascript(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        rid = 'jquery-integration.js'
        resource = javascripts.getResource(rid)
        self.assertTrue(resource.getEnabled())

        from sll.policy.upgrades import disable_javascript
        disable_javascript(self.portal, rid)

        self.assertFalse(resource.getEnabled())

    @mock.patch('sll.policy.upgrades.disable_javascript')
    def test_upgrades_33_to_34(self, disable_javascript):
        from sll.policy.upgrades import upgrade_33_to_34
        upgrade_33_to_34(self.portal)
        disable_javascript.assert_called_with(self.portal, '++resource++search.js')


    def test_upgrades_34_to_35(self):
        folder = self.portal[self.portal.invokeFactory('Folder', 'folder')]
        from collective.cart.core.interfaces.marker import IPotentiallyAddableToCart
        from collective.cart.core.interfaces.marker import IAddableToCart
        from collective.cart.core.interfaces.marker import IProductAnnotations
        from collective.cart.core.interfaces.marker import ICartAware
        from zope.interface import alsoProvides
        alsoProvides(folder, (IPotentiallyAddableToCart, IAddableToCart, IProductAnnotations, ICartAware))
        folder.reindexObject(idxs=['object_provides'])
        self.assertTrue(IPotentiallyAddableToCart.providedBy(folder))
        self.assertTrue(IAddableToCart.providedBy(folder))
        self.assertTrue(IProductAnnotations.providedBy(folder))
        self.assertTrue(ICartAware.providedBy(folder))

        from sll.policy.upgrades import upgrade_34_to_35
        upgrade_34_to_35(self.portal)

        self.assertFalse(IPotentiallyAddableToCart.providedBy(folder))
        self.assertFalse(IAddableToCart.providedBy(folder))
        self.assertFalse(IProductAnnotations.providedBy(folder))
        self.assertFalse(ICartAware.providedBy(folder))
