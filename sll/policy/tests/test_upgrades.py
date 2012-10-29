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

    def test_disable_javascript(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        rid = 'jquery-integration.js'
        resource = javascripts.getResource(rid)
        self.assertTrue(resource.getEnabled())

        from sll.policy.upgrades import disable_javascript
        disable_javascript(self.portal, rid)

        self.assertFalse(resource.getEnabled())

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

    def test_upgrade_37_to_38(self):
        membership = getToolByName(self.portal, 'portal_membership')
        membership.getMemberById('test_user_1_').manage_changeProperties(wysiwyg_editor='Kupu')
        self.assertEqual(membership.getMemberById('test_user_1_').getProperty('wysiwyg_editor'), 'Kupu')

        site_properties = getattr(getToolByName(self.portal, 'portal_properties'), 'site_properties')
        site_properties.manage_changeProperties(available_editors=('TinyMCE', 'Kupu'))
        self.assertEqual(site_properties.available_editors, ('TinyMCE', 'Kupu'))

        from sll.policy.upgrades import upgrade_37_to_38
        upgrade_37_to_38(self.portal)

        self.assertEqual(
            membership.getMemberById('test_user_1_').getProperty('wysiwyg_editor'), 'TinyMCE')

        self.assertEqual(site_properties.available_editors, ('TinyMCE',))

    def test_upgrade_38_to_39(self):
        types = getToolByName(self.portal, 'portal_types')
        ctype = types.getTypeInfo('Plone Site')
        ctype.manage_changeProperties(filter_content_types=False, allowed_content_types=())
        self.assertFalse(ctype.filter_content_types)
        self.assertEqual(ctype.allowed_content_types, ())

        from sll.policy.upgrades import upgrade_38_to_39
        upgrade_38_to_39(self.portal)

        self.assertTrue(ctype.filter_content_types)
        self.assertEqual(ctype.allowed_content_types, (
            'Carousel Banner',
            'Collection',
            'Document',
            'Event',
            'File',
            'Folder',
            'FormFolder',
            'Image',
            'Link',
            'News Item',
            'collective.cart.shopping.Shop'))


    def test_upgrade_40_to_41(self):
        membership = getToolByName(self.portal, 'portal_membership')
        membership.getMemberById('test_user_1_').manage_changeProperties(visible_ids=False)
        self.assertFalse(membership.getMemberById('test_user_1_').getProperty('visible_ids'))

        from sll.policy.upgrades import upgrade_40_to_41
        upgrade_40_to_41(self.portal)

        self.assertTrue(membership.getMemberById('test_user_1_').getProperty('visible_ids'))
