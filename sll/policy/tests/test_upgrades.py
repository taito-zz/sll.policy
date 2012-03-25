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

    def test_upgrade_3_to_4(self):
        ## Create structure under plone root.
        self.createStructure(self.portal)
        ## Create structure under three folders under plone root.
        folder01 = self.portal['folder01']
        self.createStructure(folder01)
        self.createStructure(self.portal['folder02'])
        self.createStructure(self.portal['folder03'])
        ## Create structure under one folder under a folder under plone root.
        self.createStructure(folder01['folder01'])

        ## Change workflow.
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(
            ['Document', 'Event', 'Folder', 'Link', 'News Item', 'Topic'],
            'two_states_workflow'
        )
        catalog = getToolByName(self.portal, 'portal_catalog')
        uids = [brain.UID for brain in catalog()]
        from sll.policy.upgrades import upgrade_3_to_4
        upgrade_3_to_4(self.portal)
        new_uids = [brain.UID for brain in catalog()]
        for uid in new_uids:
            self.assertFalse(uid in uids)
