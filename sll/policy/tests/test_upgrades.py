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

    def test_upgrades_35_to_36(self):
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        registry['collective.searchevent.collections'] = []
        self.assertEqual(
            registry['collective.searchevent.collections'], [])

        registry['hexagonit.socialbutton.codes'] = {}
        registry['hexagonit.socialbutton.config'] = {}

        self.assertEqual(registry['hexagonit.socialbutton.codes'], {})
        self.assertEqual(registry['hexagonit.socialbutton.config'], {})

        from sll.policy.upgrades import upgrade_35_to_36
        upgrade_35_to_36(self.portal)

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
                            'sll/pohjois-savo',
                            'sll/satakunta',
                            'sll/uusimaa',
                            'sll/varsinais-suomi',
                        ]
                    ),
                    'tags': ['Kokous', 'Kurssi', 'Retki', 'Talkoot'],
                }
            ]
        )

        self.assertEqual(registry['hexagonit.socialbutton.codes'], {
            u'twitter': {u'code_text': u'<a class="social-button twitter" title="Twitter" href="https://twitter.com/share?text=${title}?url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/twitter.gif" />\n</a>'},
            u'facebook': {u'code_text': u'<a class="social-button facebook" title="Facebook" target="_blank" href="http://www.facebook.com/sharer.php?t=${title}&u=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/facebook.gif" />\n</a>'},
            u'google-plus': {u'code_text': u'<a class="social-button googleplus" title="Google+" href="https://plusone.google.com/_/+1/confirm?hl=${lang}&title=${title}&url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/google-plus.gif" />\n</a>'},
            u'kysely': {u'code_text': u'<script type="text/javascript">\n   var _wt = \'9eb28b\';\n\n   (function () {\n       if (document.cookie.indexOf(\'VISITED_2719\') < 0) {\n           var ws = document.createElement(\'script\'); ws.type = \'text/javascript\'; ws.async = true;\n           ws.src = (\'https:\' == document.location.protocol ? \'https://ssl.\' : \'http://\') + \'survey.webstatus.v2.userneeds.dk/wsi.ashx?t=\' + _wt + (location.href.indexOf(\'wsiNoCookie\') >= 0 ? \'&nc=1\' : \'\');\n           var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ws, s);\n   }})();\n</script>'},
            })
        self.assertEqual(registry['hexagonit.socialbutton.config'], {
            u'twitter': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'facebook': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'google-plus': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'kysely': {u'content_types': u'*', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.abovecontent'},
            })

    def test_upgrade_36_to_37(self):
        atct = getToolByName(self.portal, 'portal_atct')
        atct.manage_changeProperties(
            image_types=(), folder_types=(), album_batch_size=10,
            album_image_scale='small', single_image_scale='thumb')
        self.assertEqual(atct.getProperty('image_types'), ())
        self.assertEqual(atct.getProperty('folder_types'), ())
        self.assertEqual(atct.getProperty('album_batch_size'), 10)
        self.assertEqual(atct.getProperty('album_image_scale'), 'small')
        self.assertEqual(atct.getProperty('single_image_scale'), 'thumb')

        from sll.policy.upgrades import upgrade_36_to_37
        upgrade_36_to_37(self.portal)

        self.assertEqual(atct.getProperty('image_types'), ('Image', 'News Item'))
        self.assertEqual(atct.getProperty('folder_types'), ('Image',))
        self.assertEqual(atct.getProperty('album_batch_size'), 30)
        self.assertEqual(atct.getProperty('album_image_scale'), 'thumb')
        self.assertEqual(atct.getProperty('single_image_scale'), 'preview')
