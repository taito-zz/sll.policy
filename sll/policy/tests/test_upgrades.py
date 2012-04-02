from sll.policy.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone upgrades."""

    def setUp(self):
        self.portal = self.layer['portal']

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
        self.assertRaises(KeyError, lambda:self.portal['removable'])
        self.assertRaises(KeyError, lambda:self.portal['copy_of_folder'])

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

    # def test_upgrade_4_to_5__contents(self):
    #     ## Create structure under plone root.
    #     self.createStructure(self.portal)
    #     ## Create structure under three folders under plone root.
    #     folder01 = self.portal['folder01']
    #     self.createStructure(folder01)
    #     self.createStructure(self.portal['folder02'])
    #     self.createStructure(self.portal['folder03'])
    #     ## Create structure under one folder under a folder under plone root.
    #     self.createStructure(folder01['folder01'])

    #     ## exclude_from_nav
    #     self.assertFalse(folder01.exclude_from_nav())
    #     folder02 = self.portal['folder02']
    #     self.assertFalse(folder02.exclude_from_nav())
    #     link01 = self.portal['link01']
    #     self.assertFalse(link01.exclude_from_nav())

    #     catalog = getToolByName(self.portal, 'portal_catalog')
    #     uids = [brain.UID for brain in catalog()]

    #     from sll.policy.upgrades import upgrade_4_to_5
    #     upgrade_4_to_5(self.portal)

    #     ## exclude_from_nav
    #     self.assertFalse(folder01.exclude_from_nav())
    #     self.assertTrue(folder02.exclude_from_nav())
    #     self.assertFalse(link01.exclude_from_nav())

    #     from Products.ATContentTypes.interfaces.document import IATDocument
    #     from Products.ATContentTypes.interfaces.folder import IATFolder
    #     object_provides = [
    #         IATDocument.__identifier__,
    #         IATFolder.__identifier__,
    #     ]
    #     query = {
    #         'object_provides': object_provides,
    #     }

    #     new_uids = [brain.UID for brain in catalog(query)]
    #     for uid in new_uids:
    #         self.assertFalse(uid in uids)

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

        # from Products.ATContentTypes.interfaces.folder import IATFolder
        # query = {
        #     'object_provides': IATFolder.__identifier__,
        #     'path': {
        #         'query': '/'.join(self.portal.getPhysicalPath()),
        #         'depth': 2,
        #     },
        # }

        # new_uids = [brain.UID for brain in catalog(query)]
        # for uid in new_uids:
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
