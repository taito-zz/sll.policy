from sll.policy.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

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

    def test_upgrade_3_to_4(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory(
            'Folder',
            'removable',
        )
        self.portal.invokeFactory(
            'Folder',
            'copy_of_folder',
        )
        self.failUnless(self.portal['removable'])
        self.failUnless(self.portal['copy_of_folder'])
        from sll.policy.upgrades import upgrade_3_to_4
        upgrade_3_to_4(self.portal)
        self.assertRaises(KeyError, lambda: self.portal['removable'])
        self.assertRaises(KeyError, lambda: self.portal['copy_of_folder'])

    def createStructure(self, folder):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Folder', 'Topic'], 'folder_workflow')
        wftool.setChainForPortalTypes(
            ['Document', 'Event', 'Link', 'News Item'], 'plone_workflow'
        )

        ## Create published Folder01.
        folder01 = folder[
            folder.invokeFactory(
                'Folder',
                'folder01',
            )
        ]
        wftool.doActionFor(folder01, 'publish')
        folder01.reindexObject()
        ## Create visible Folder02.
        folder02 = folder[
            folder.invokeFactory(
                'Folder',
                'folder02',
            )
        ]
        folder02.reindexObject()
        ## Create private Folder03.
        folder03 = folder[
            folder.invokeFactory(
                'Folder',
                'folder03',
            )
        ]
        wftool.doActionFor(folder03, 'hide')
        folder03.reindexObject()

        ## Create published Topic01.
        topic01 = folder[
            folder.invokeFactory(
                'Topic',
                'topic01'
            )
        ]
        wftool.doActionFor(topic01, 'publish')
        topic01.reindexObject()
        ## Create visible Topic02.
        topic02 = folder[
            folder.invokeFactory(
                'Topic',
                'topic02'
            )
        ]
        topic02.reindexObject()
        ## Create private Topic03.
        topic03 = folder[
            folder.invokeFactory(
                'Topic',
                'topic03'
            )
        ]
        wftool.doActionFor(topic03, 'hide')
        topic03.reindexObject()

        ## Create published Document01.
        document01 = folder[
            folder.invokeFactory(
                'Document',
                'document01'
            )
        ]
        wftool.doActionFor(document01, 'publish')
        document01.reindexObject()
        ## Create pending Document02.
        document02 = folder[
            folder.invokeFactory(
                'Document',
                'document02'
            )
        ]
        wftool.doActionFor(document02, 'submit')
        document02.reindexObject()
        ## Create visible Document02.
        document03 = folder[
            folder.invokeFactory(
                'Document',
                'document03'
            )
        ]
        document03.reindexObject()
        ## Create private Document04.
        document04 = folder[
            folder.invokeFactory(
                'Document',
                'document04'
            )
        ]
        wftool.doActionFor(document04, 'hide')
        document04.reindexObject()

        ## Create published Event01.
        event01 = folder[
            folder.invokeFactory(
                'Event',
                'event01'
            )
        ]
        wftool.doActionFor(event01, 'publish')
        event01.reindexObject()
        ## Create pending Event02.
        event02 = folder[
            folder.invokeFactory(
                'Event',
                'event02'
            )
        ]
        wftool.doActionFor(event02, 'submit')
        event02.reindexObject()
        ## Create visible Event02.
        event03 = folder[
            folder.invokeFactory(
                'Event',
                'event03'
            )
        ]
        event03.reindexObject()
        ## Create private Event04.
        event04 = folder[
            folder.invokeFactory(
                'Event',
                'event04'
            )
        ]
        wftool.doActionFor(event04, 'hide')
        event04.reindexObject()

        ## Create published Link01.
        link01 = folder[
            folder.invokeFactory(
                'Link',
                'link01'
            )
        ]
        wftool.doActionFor(link01, 'publish')
        link01.reindexObject()
        ## Create pending Link02.
        link02 = folder[
            folder.invokeFactory(
                'Link',
                'link02'
            )
        ]
        wftool.doActionFor(link02, 'submit')
        link02.reindexObject()
        ## Create visible Link02.
        link03 = folder[
            folder.invokeFactory(
                'Link',
                'link03'
            )
        ]
        link03.reindexObject()
        ## Create private Link04.
        link04 = folder[
            folder.invokeFactory(
                'Link',
                'link04'
            )
        ]
        wftool.doActionFor(link04, 'hide')
        link04.reindexObject()

        ## Create published News Item01.
        news01 = folder[
            folder.invokeFactory(
                'News Item',
                'news01'
            )
        ]
        wftool.doActionFor(news01, 'publish')
        news01.reindexObject()
        ## Create pending News Item02.
        news02 = folder[
            folder.invokeFactory(
                'News Item',
                'news02'
            )
        ]
        wftool.doActionFor(news02, 'submit')
        news02.reindexObject()
        ## Create visible News Item02.
        news03 = folder[
            folder.invokeFactory(
                'News Item',
                'news03'
            )
        ]
        news03.reindexObject()
        ## Create private News Item04.
        news04 = folder[
            folder.invokeFactory(
                'Document',
                'news04'
            )
        ]
        wftool.doActionFor(news04, 'hide')
        news04.reindexObject()

    def test_upgrade_4_to_5__workflow(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ## Change enable_wf_state_filtering.
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        self.assertFalse(navtree_properties.getProperty('enable_wf_state_filtering'))
        navtree_properties._updateProperty('enable_wf_state_filtering', True)
        self.assertTrue(navtree_properties.getProperty('enable_wf_state_filtering'))

        from sll.policy.upgrades import upgrade_4_to_5
        upgrade_4_to_5(self.portal)

        self.assertFalse(navtree_properties.getProperty('enable_wf_state_filtering'))

        wftool = getToolByName(self.portal, 'portal_workflow')
        contents = [
            'Document',
            'Event',
            'File',
            'Folder',
            'FormFolder',
            'Image',
            'Link',
            'News Item',
            'Topic',
        ]
        for content in contents:
            self.assertEqual(
                wftool.getChainForPortalType(content),
                ('two_states_workflow',)
            )

    def test_upgrade_4_to_5__disable_nonfolderish_sections(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        self.assertFalse(site_properties.getProperty('disable_nonfolderish_sections'))
        site_properties._updateProperty('disable_nonfolderish_sections', True)
        self.assertTrue(site_properties.getProperty('disable_nonfolderish_sections'))
        from sll.policy.upgrades import upgrade_4_to_5
        upgrade_4_to_5(self.portal)
        self.assertFalse(site_properties.getProperty('disable_nonfolderish_sections'))

    def test_upgrade_4_to_5__wf_states_to_show(self):

        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        self.assertEqual(
            navtree_properties.getProperty('wf_states_to_show'),
            ()
        )
        navtree_properties._updateProperty('wf_states_to_show', ('published', 'private'))
        self.assertEqual(
            navtree_properties.getProperty('wf_states_to_show'),
            ('published', 'private')
        )
        from sll.policy.upgrades import upgrade_4_to_5
        upgrade_4_to_5(self.portal)
        self.assertEqual(
            navtree_properties.getProperty('wf_states_to_show'),
            ()
        )

    def test_upgrade_5_to_6(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        folder01 = self.portal[
            self.portal.invokeFactory(
                'Folder',
                'folder01',
            )
        ]
        folder01.reindexObject()
        folder02 = folder01[
            folder01.invokeFactory(
                'Folder',
                'folder02',
            )
        ]
        folder02.reindexObject()
        catalog = getToolByName(self.portal, 'portal_catalog')

        uids = [brain.UID for brain in catalog()]

        from sll.policy.upgrades import upgrade_5_to_6
        upgrade_5_to_6(self.portal)

        from Products.ATContentTypes.interfaces.folder import IATFolder
        query = {
            'object_provides': IATFolder.__identifier__,
            'path': {
                'query': '/'.join(self.portal.getPhysicalPath()),
                'depth': 1,
            },
        }

        new_uids = [brain.UID for brain in catalog(query)]
        for uid in new_uids:
            self.assertFalse(uid in uids)
        self.failUnless(self.portal['folder01'])

    def test_upgrade_6_to_7(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        wftool = getToolByName(self.portal, "portal_workflow")

        folder01 = self.portal[
            self.portal.invokeFactory(
                'Folder',
                'folder01',
            )
        ]
        folder01.reindexObject()
        wftool.doActionFor(folder01, 'publish')
        folder01.reindexObject(idxs=['review_state'])

        folder02 = folder01[
            folder01.invokeFactory(
                'Folder',
                'folder02',
            )
        ]
        folder02.reindexObject()
        wftool.doActionFor(folder02, 'publish')
        folder02.reindexObject(idxs=['review_state'])

        folder03 = folder02[
            folder02.invokeFactory(
                'Folder',
                'folder03',
            )
        ]
        folder03.reindexObject()

        catalog = getToolByName(self.portal, 'portal_catalog')
        uids = [brain.UID for brain in catalog()]

        from sll.policy.upgrades import upgrade_6_to_7
        upgrade_6_to_7(self.portal)

        self.assertFalse(self.portal['folder01']['folder02'].UID() in uids)
        self.failUnless(self.portal['folder01']['folder02'])
        self.failUnless(
            wftool.getInfoFor(
                self.portal['folder01'],
                'review_state'
            ),
            'published'
        )
        self.failUnless(
            wftool.getInfoFor(
                self.portal['folder01']['folder02'],
                'review_state'
            ),
            'published'
        )
        self.failUnless(
            wftool.getInfoFor(
                self.portal['folder01']['folder02']['folder03'],
                'review_state'
            ),
            'private'
        )

    def test_copy_paste_remove_others(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        wftool = getToolByName(self.portal, "portal_workflow")

        document01 = self.portal[
            self.portal.invokeFactory(
                'Document',
                'document01',
            )
        ]
        wftool.doActionFor(document01, 'publish')
        document01.reindexObject()

        document02 = self.portal[
            self.portal.invokeFactory(
                'Document',
                'document02',
            )
        ]
        document02.reindexObject()

        catalog = getToolByName(self.portal, 'portal_catalog')
        uids = [brain.UID for brain in catalog()]

        from sll.policy.upgrades import copy_paste_remove_others

        from Products.ATContentTypes.interfaces.document import IATDocument
        copy_paste_remove_others(self.portal, IATDocument.__identifier__)

        self.assertFalse(self.portal['document01'].UID() in uids)
        self.assertFalse(self.portal['document02'].UID() in uids)
        self.failUnless(
            wftool.getInfoFor(
                self.portal['document01'],
                'review_state'
            ),
            'published'
        )
        self.failUnless(
            wftool.getInfoFor(
                self.portal['document02'],
                'review_state'
            ),
            'private'
        )

    def test_upgrade_13_to_14(self):
        portal_properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        self.assertEqual(navtree_properties.getProperty('topLevel'), 0)

        navtree_properties._updateProperty('topLevel', 1)
        self.assertEqual(navtree_properties.getProperty('topLevel'), 1)

        from sll.policy.upgrades import upgrade_13_to_14
        upgrade_13_to_14(self.portal)

        self.assertEqual(navtree_properties.getProperty('topLevel'), 0)

    def test_upgrade_14_to_15__collective_cropimage_ids(self):
        from sll.policy.upgrades import upgrade_14_to_15
        upgrade_14_to_15(self.portal)
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)
        self.assertEqual(
            registry['collective.cropimage.ids'],
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

    def test_upgrades_15_to_16(self):
        portal_skins = getToolByName(self.portal, 'portal_skins')
        custom = portal_skins['custom']
        from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate
        manage_addPageTemplate(custom, 'aaa', text='')
        manage_addPageTemplate(custom, 'portlet_kartta', text='')
        from sll.policy.upgrades import upgrade_15_to_16
        upgrade_15_to_16(self.portal)
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertFalse(installer.isProductInstalled('NewSllSkin'))
        self.assertEqual(portal_skins.default_skin, 'Sunburst Theme')
        self.assertFalse('NewSllSkin' in portal_skins.getSkinSelections())
        self.assertEqual(custom.objectIds(), ['aaa'])

    def test_upgrades_16_to_17(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        storage.setHidden('plone.portaltop', '*', (u'plone.header',))
        self.assertTrue(u'plone.header' in storage.getHidden('plone.portaltop', '*'))
        storage.setHidden('plone.portalheader', '*', (u'plone.logo',))
        self.assertTrue(u'plone.logo' in storage.getHidden('plone.portalheader', '*'))
        from sll.policy.upgrades import upgrade_16_to_17
        upgrade_16_to_17(self.portal)
        self.assertEqual(
            storage.getOrder('plone.portaltop', '*'),
            (
                u'plone.header',
            )
        )
        self.assertFalse(storage.getHidden('plone.portaltop', '*'))
        self.assertEqual(
            storage.getOrder('plone.portalheader', '*'),
            (
                u'plone.skip_links',
                u'plone.personal_bar',
                u'plone.site_actions',
                u'plone.app.i18n.locales.languageselector',
                u'plone.searchbox',
                u'plone.logo',
                u'plone.global_sections',
            )
        )
        self.assertEqual(storage.getHidden('plone.portalheader', '*'), ())

    def test_upgrades_17_to_18(self):
        tausta = self.portal[
            self.portal.invokeFactory('Document', 'ylapalkin-tausta.png')
        ]
        tausta.reindexObject()
        self.failUnless(self.portal['ylapalkin-tausta.png'])
        properties = getToolByName(self.portal, 'portal_properties')
        folder_logo_properties = getattr(properties, 'folder_logo_properties')
        folder_logo_properties.manage_changeProperties(
            background_color='white',
            background_image_id='image',
        )
        self.assertEqual(
            folder_logo_properties.getProperty('background_color'),
            'white'
        )
        self.assertEqual(
            folder_logo_properties.getProperty('background_image_id'),
            'image'
        )
        from sll.policy.upgrades import upgrade_17_to_18
        upgrade_17_to_18(self.portal)
        self.assertRaises(KeyError, lambda: self.portal['ylapalkin-tausta.png'])
        self.assertEqual(
            folder_logo_properties.getProperty('background_color'),
            ''
        )
        self.assertEqual(
            folder_logo_properties.getProperty('background_image_id'),
            ''
        )

    def test_upgrades_18_to_19(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        product = 'plonetheme.classic'
        installer.installProduct(product)
        self.assertTrue(installer.isProductInstalled(product))
        from sll.policy.upgrades import upgrade_18_to_19
        upgrade_18_to_19(self.portal)
        self.assertFalse(installer.isProductInstalled(product))

    def test_upgrades_19_to_20(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        storage.setHidden('plone.portalfooter', '*', (u'plone.footer',))
        self.assertEqual(storage.getHidden('plone.portalfooter', '*'), (u'plone.footer',))
        from sll.policy.upgrades import upgrade_19_to_20
        upgrade_19_to_20(self.portal)
        self.assertEqual(
            storage.getHidden('plone.portalfooter', '*'),
            (
                u'plone.colophon',
                u'plone.site_actions',
            )
        )
        self.assertEqual(
            storage.getOrder('plone.portalheader', '*'),
            (
                u'plone.skip_links',
                u'plone.personal_bar',
                u'plone.site_actions',
                u'plone.app.i18n.locales.languageselector',
                u'plone.searchbox',
                u'plone.logo',
                u'plone.global_sections',
            )
        )

    def test_upgrades_21_to_22(self):
        folder01 = self.portal[
            self.portal.invokeFactory(
                'Folder',
                'folder01',
            )
        ]
        folder01.setExcludeFromNav(False)
        folder01.reindexObject()

        folder02 = folder01[
            folder01.invokeFactory(
                'Folder',
                'folder02',
            )
        ]
        folder02.setExcludeFromNav(False)
        folder02.reindexObject()

        liity = self.portal[
            self.portal.invokeFactory(
                'Folder',
                'liity',
            )
        ]
        liity.setExcludeFromNav(True)
        liity.reindexObject()

        self.assertFalse(folder01.getExcludeFromNav())
        self.assertTrue(liity.getExcludeFromNav())

        from sll.policy.upgrades import upgrade_21_to_22
        upgrade_21_to_22(self.portal)
        self.assertTrue(folder01.getExcludeFromNav())
        self.assertFalse(folder02.getExcludeFromNav())
        self.assertFalse(liity.getExcludeFromNav())

    def test_upgrades_22_to_23(self):
        index_html = self.portal[
            self.portal.invokeFactory(
                'Document',
                'index_html',
            )
        ]
        index_html.reindexObject()
        self.portal.setLayout('index_html')

        from sll.policy.upgrades import upgrade_22_to_23
        upgrade_22_to_23(self.portal)

        self.assertRaises(AttributeError, lambda: self.portal['index_html'])
        self.assertEqual(self.portal.getLayout(), 'sll-view')

    def test_upgrades_23_to_24(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        if installer.isProductInstalled('sll.portlet'):
            installer.uninstallProducts(['sll.portlet'])
        if installer.isProductInstalled('sll.theme'):
            installer.uninstallProducts(['sll.theme'])

        from sll.policy.upgrades import upgrade_23_to_24
        upgrade_23_to_24(self.portal)

        self.assertTrue(installer.isProductInstalled('sll.portlet'))
        self.assertTrue(installer.isProductInstalled('sll.theme'))

    def createContents(self, parent, Type, amount=1):
        objs = set([])
        for num in range(amount, amount + 1):
            oid = '{0}{1:05d}'.format(Type.replace(' ', '').lower(), num)
            cid = oid.capitalize()
            obj = parent[
                parent.invokeFactory(
                        Type,
                        oid,
                        title='Title of {0}'.format(cid),
                        description='Description of {0}'.format(cid),
                    )
            ]
            obj.reindexObject()
            objs.add(obj)
        return objs

    def test_upgrades_24_to_25(self):
        objs = self.createContents(self.portal, 'Folder')
        obj = list(objs)[0]
        from sll.policy.browser.interfaces import ITopPageFeed
        from zope.interface import alsoProvides
        alsoProvides(obj, ITopPageFeed)
        obj.reindexObject(idxs=['object_provides'])
        self.assertTrue(ITopPageFeed.providedBy(obj))
        from sll.templates.browser.interfaces import ITopPageFeed
        self.assertFalse(ITopPageFeed.providedBy(obj))

        from sll.policy.upgrades import upgrade_24_to_25
        upgrade_24_to_25(self.portal)

        from sll.policy.browser.interfaces import ITopPageFeed
        self.assertFalse(ITopPageFeed.providedBy(obj))
        from sll.templates.browser.interfaces import ITopPageFeed
        self.assertTrue(ITopPageFeed.providedBy(obj))

    def test_upgrades_25_to_26(self):
        portal_actions = getToolByName(self.portal, 'portal_actions')
        document_actions = getattr(portal_actions, 'document_actions')
        document_actions.manage_addFolder('addtofavorites')

        self.failUnless(document_actions['addtofavorites'])

        from sll.policy.upgrades import upgrade_25_to_26
        upgrade_25_to_26(self.portal)

        self.assertRaises(KeyError, lambda: document_actions['addtofavorites'])

    def test_upgrades_26_to_27(self):
        portal_properties = getToolByName(self.portal, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        site_properties.manage_changeProperties(mark_special_links="true")

        self.assertEqual(site_properties.getProperty('mark_special_links'), 'true')

        from sll.policy.upgrades import upgrade_26_to_27
        upgrade_26_to_27(self.portal)

        self.assertEqual(site_properties.getProperty('mark_special_links'), 'false')
