from Acquisition import aq_parent
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.link import IATLink
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from sll.policy.config import IDS
from zope.component import getUtility
from plone.app.blob.interfaces import IATBlob

import logging

PROFILE_ID = 'profile-sll.policy:default'


def upgrade_1_to_2(context, logger=None):
    """Remove unused roles."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    logger.info('Start removing unused roles.')
    portal.__ac_roles__ = ('Contributor', 'Member', 'Site Administrator')
    logger.info('Removed unused roles.')


def upgrade_2_to_3(context, logger=None):
    """Remove Reviewers group."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
    groupstool = getToolByName(context, 'portal_groups')
    logger.info('Start removing Reviewers group.')
    groupstool.removeGroup('Reviewers')
    logger.info('Removed Reviewers group.')


def upgrade_3_to_4(context, logger=None):
    """"Delete Removable Folder and copy_of_...."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # Get portal
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()

    # Monkey patching getIntegrityBreaches method.
    from plone.uuid.interfaces import IUUID
    from plone.app.linkintegrity.info import LinkIntegrityInfo

    def getSLLIntegrityBreaches(self):
        """ return stored information regarding link integrity breaches
            after removing circular references, confirmed items etc """
        uuids_to_delete = [IUUID(obj, None) for obj in self.getDeletedItems()]
        uuids_to_delete = set(filter(None, uuids_to_delete))    # filter `None`
        breaches = dict(self.getIntegrityInfo().get('breaches', {}))
        uuids_to_delete.update([IUUID(obj) for obj in breaches if obj is not None])
        for target, sources in breaches.items():    # first remove deleted sources
            for source in list(sources):
                if IUUID(source) in uuids_to_delete:
                    sources.remove(source)
        for target, sources in breaches.items():    # then remove "empty" targets
            if not sources or self.isConfirmedItem(target):
                del breaches[target]
        return breaches

    LinkIntegrityInfo.getIntegrityBreaches = getSLLIntegrityBreaches

    # Remove unnecessary contents
    if portal.get('removable'):
        logger.info('Start removing Removable Folder.')
        portal.manage_delObjects(['removable'])
        logger.info('Removable Folder Removed.')

    catalog = getToolByName(context, 'portal_catalog')

    brains = [brain for brain in catalog() if brain.id.startswith('copy')]
    for brain in brains:
        parent = aq_parent(brain.getObject())
        path = brain.getPath()
        ## Delete objects
        message = "Start removing '{0}'.".format(path)
        logger.info(message)
        parent.manage_delObjects([brain.id])
        message = "'{0}' removed.".format(path)
        logger.info(message)

    logger.info('All the contents id starting with "copy" removed.')


def upgrade_4_to_5(context, logger=None):
    """"Update Navigation and Wrokflow."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    setup = getToolByName(context, 'portal_setup')

    # Update filtering on workflow state by import propertiestool.xml.
    logger.info('Start reimporting propertiestool.xml.')
    setup.runImportStepFromProfile(PROFILE_ID, 'propertiestool', run_dependencies=False, purge_old=False)
    logger.info('Reimported propertiestool.xml.')

    # Update propertiestool.xml
    properties = getToolByName(context, 'portal_properties')
    navtree_properties = getattr(properties, 'navtree_properties')
    logger.info('Start updating enable_wf_state_filtering into False.')
    navtree_properties._updateProperty('enable_wf_state_filtering', False)
    logger.info('enable_wf_state_filtering updated to False.')

    logger.info('Start emptying  wf_states_to_show.')
    navtree_properties._updateProperty('wf_states_to_show', ())
    logger.info('wf_states_to_show emptied.')

    # First import workflow.xml
    logger.info('Start reimporting workflows.xml.')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow', run_dependencies=False, purge_old=False)
    logger.info('Reimported workflows.xml.')

    # Update contents workflow.
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
    logger.info('Start updating contents workflows to two_states_workflow.')
    wftool = getToolByName(context, 'portal_workflow')
    wftool.setChainForPortalTypes(contents, '(Default)')
    logger.info('contents workflow updated into two_states_workflow.')

    catalog = getToolByName(context, 'portal_catalog')
    query = {'portal_type': contents}
    brains = catalog(query)
    count = len(brains)
    message = 'There are {0} objects to update workflow.'.format(count)
    logger.info(message)

    for brain in brains:
        obj = brain.getObject()
        ## exclude_from_nav
        parent = aq_parent(obj)
        if INavigationRoot.providedBy(parent):
            types = ['Document', 'Folder', 'FormFolder', 'News Item']
            if (brain.portal_type in types) and (brain.review_state != 'published'):
                path = brain.getPath()
                message = "Start excluding '{0}' from navigation.".format(path)
                logger.info(message)
                obj.setExcludeFromNav(True)
                message = "'{0}' excluded from navigation.".format(path)
                logger.info(message)

        state = brain.review_state
        if (
            state == 'publishe'
        ) or (
            state == 'visible'
        ):
            message = "Start publishing '{0}',".format(path)
            logger.info(message)
            wftool.doActionFor(obj, 'publish', wf_id="two_states_workflow")
            obj.reindexObject(idxs=['review_state'])
            message = "'{0}' published.".format(path)
            logger.info(message)
        count -= 1
        message = 'Still {0} objects to update workflow.'.format(count)
        logger.info(message)


def copy_paste_remove(context, object_provides, depth, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # Monkey patch insertForwardIndexEntry method
    from Products.PluginIndexes.UUIDIndex.UUIDIndex import UUIDIndex
    from Products.PluginIndexes.common.UnIndex import _marker

    def insertSLLForwardIndexEntry(self, entry, documentId):
        """Take the entry provided and put it in the correct place
        in the forward index.
        """
        if entry is None:
            return

        old_docid = self._index.get(entry, _marker)
        if old_docid is _marker:
            self._index[entry] = documentId
            self._length.change(1)
        elif old_docid != documentId:
            self.removeForwardIndexEntry(entry, documentId)
            # logger.error("A different document with value '%s' already "
            #     "exists in the index.'" % entry)

    UUIDIndex.insertForwardIndexEntry = insertSLLForwardIndexEntry

    # Update propertiestool.xml
    properties = getToolByName(context, 'portal_properties')
    site_properties = getattr(properties, 'site_properties')
    logger.info('Disabling enable_link_integrity_checks.')
    site_properties._updateProperty('enable_link_integrity_checks', False)
    logger.info('Disabled enable_link_integrity_checks.')

    catalog = getToolByName(context, 'portal_catalog')

    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    paths = '/'.join(portal.getPhysicalPath())

    old_query = {
        'object_provides': object_provides,
        'path': {
            'query': paths,
            'depth': depth-1,
        },
    }

    new_query = {
        'object_provides': object_provides,
        'path': {
            'query': paths,
            'depth': depth,
        },
    }
    old_brains = set(catalog(old_query))
    old_uids = set([brain.UID for brain in old_brains])
    new_brains = set(catalog(new_query))
    brains = [brain for brain in new_brains if brain.UID not in old_uids]
    count = len(brains)
    message = 'There are {0} {1} left in depth {2} to copy, paste and remove.'.format(
        count,
        object_provides,
        depth
    )
    logger.info(message)

    wftool = getToolByName(context, "portal_workflow")

    for brain in brains:
        obj = brain.getObject()
        parent = aq_parent(obj)
        path = brain.getPath()
        bid = brain.id
        query = {
            'path': path,
            'review_state': ['published', 'visible'],
        }
        publishing_paths = [brain.getPath() for brain in catalog(query)]

        ## Copy objects
        message = "Copying '{0}'.".format(path)
        logger.info(message)
        objs = parent.manage_copyObjects([bid])
        message = "'{0}' copied.".format(path)
        logger.info(message)
        ## Past objects
        message = "Pasting '{0}'.".format(path)
        logger.info(message)
        parent.manage_pasteObjects(objs)
        message = "'{0}' pasted.".format(path)
        logger.info(message)
        ## Remove objects
        message = "Removing '{0}'.".format(path)
        logger.info(message)
        parent.manage_delObjects([bid])
        message = "'{0}' removed.".format(path)
        logger.info(message)
        ## Update ID
        copied_id = 'copy_of_{0}'.format(bid)
        copied = parent[copied_id]
        message = 'Updating ID {0} --> {1}.'.format(copied_id, bid)
        logger.info(message)
        copied.setId(bid)
        message = 'ID {0} --> {1} updated.'.format(copied_id, bid)
        logger.info(message)

        query = {
            'path': path,
        }
        for brain in catalog(query):
            bpath = brain.getPath()
            if bpath in publishing_paths:
                obj = brain.getObject()
                message = "Publishing '{0}'.".format(bpath)
                logger.info(message)
                wftool.doActionFor(obj, 'publish')
                obj.reindexObject(idxs=['review_state'])
                message = "'{0}' published.".format(bpath)
                logger.info(message)

        count -= 1
        message = "{0} {1} left to update.".format(count, object_provides)
        logger.info(message)

    message = 'Update completed for {0} in depth {1}.'.format(
        object_provides,
        depth
    )
    logger.info(message)
    logger.info('Enabling enable_link_integrity_checks.')
    site_properties._updateProperty('enable_link_integrity_checks', True)
    logger.info('Enabled enable_link_integrity_checks.')


def upgrade_folders(context, depth):
    """"Copy, paste and remove folders in depth."""
    object_provides = IATFolder.__identifier__
    copy_paste_remove(context, object_provides, depth)


def upgrade_5_to_6(context, logger=None):
    """"Copy, paste and remove folders in depth 1."""
    upgrade_folders(context, 1)


def upgrade_6_to_7(context, logger=None):
    """"Copy, paste and remove folders in depth 2."""
    upgrade_folders(context, 2)


def upgrade_7_to_8(context, logger=None):
    """"Copy, paste and remove folders in depth 3."""
    upgrade_folders(context, 3)


def upgrade_8_to_9(context, logger=None):
    """"Copy, paste and remove folders in depth 4."""
    upgrade_folders(context, 4)


def upgrade_9_to_10(context, logger=None):
    """"Copy, paste and remove folders in depth 5."""
    upgrade_folders(context, 5)


def upgrade_10_to_11(context, logger=None):
    """"Copy, paste and remove folders in depth 6."""
    upgrade_folders(context, 6)


def upgrade_11_to_12(context, logger=None):
    """"Copy, paste and remove folders in depth 7."""
    upgrade_folders(context, 7)


def copy_paste_remove_others(context, object_provides, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # Update propertiestool.xml
    properties = getToolByName(context, 'portal_properties')
    site_properties = getattr(properties, 'site_properties')
    logger.info('Disabling enable_link_integrity_checks.')
    site_properties._updateProperty('enable_link_integrity_checks', False)
    logger.info('Disabled enable_link_integrity_checks.')

    catalog = getToolByName(context, 'portal_catalog')
    query = {
        'object_provides': object_provides,
    }
    brains = catalog(query)
    count = len(brains)
    message = 'There are {0} {1} to copy, paste and remove.'.format(
        count,
        object_provides,
    )
    logger.info(message)

    wftool = getToolByName(context, "portal_workflow")

    for brain in brains:
        obj = brain.getObject()
        parent = aq_parent(obj)
        path = brain.getPath()
        bid = brain.id
        state = brain.review_state
        ## Copy objects
        message = "Copying '{0}'.".format(path)
        logger.info(message)
        objs = parent.manage_copyObjects([bid])
        message = "'{0}' copied.".format(path)
        logger.info(message)
        ## Past objects
        message = "Pasting '{0}'.".format(path)
        logger.info(message)
        parent.manage_pasteObjects(objs)
        message = "'{0}' pasted.".format(path)
        logger.info(message)
        ## Remove objects
        message = "Removing '{0}'.".format(path)
        logger.info(message)
        parent.manage_delObjects([bid])
        message = "'{0}' removed.".format(path)
        logger.info(message)
        ## Update ID
        copied_id = 'copy_of_{0}'.format(bid)
        copied = parent[copied_id]
        message = 'Updating ID {0} --> {1}.'.format(copied_id, bid)
        logger.info(message)
        copied.setId(bid)
        message = 'ID {0} --> {1} updated.'.format(copied_id, bid)
        logger.info(message)
        ## Update state
        if state == 'published':
            message = "Publishing '{0}'.".format(path)
            logger.info(message)
            wftool.doActionFor(copied, 'publish')
            copied.reindexObject(idxs=['review_state'])
            message = "'{0}' published.".format(path)
            logger.info(message)

        count -= 1
        message = "{0} {1} left to update.".format(count, object_provides)
        logger.info(message)

    message = 'Update completed for {0}.'.format(
        object_provides,
    )
    logger.info(message)
    logger.info('Enabling enable_link_integrity_checks.')
    site_properties._updateProperty('enable_link_integrity_checks', True)
    logger.info('Enabled enable_link_integrity_checks.')


def upgrade_12_to_13(context, logger=None):
    """Copy paste and remove Content Types below:

    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    object_provides = [
        IATDocument.__identifier__,
        IATEvent.__identifier__,
        IATLink.__identifier__,
        IATNewsItem.__identifier__,
        IATTopic.__identifier__,
        IPloneFormGenForm.__identifier__,
    ]
    copy_paste_remove_others(context, object_provides, logger=logger)


def upgrade_13_to_14(context, logger=None):
    """Update default topLevel to zero for navigation portlet.

    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    portal_properties = getToolByName(context, 'portal_properties')
    navtree_properties = getattr(portal_properties, 'navtree_properties')
    logger.info('Setting topLevel to zero for navigation portlet.')
    navtree_properties._updateProperty('topLevel', 0)
    logger.info('Set topLevel to zero for navigation portlet.')


# def upgrade_14_to_15(context, logger=None):
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     object_provides = IATBlob.__identifier__
#     copy_paste_remove_others(context, object_provides, logger=logger)


def upgrade_14_to_15(context, logger=None):
    """"Setup collective.cropimage."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    setup = getToolByName(context, 'portal_setup')
    logger.info('Start installing collective.cropimage.')
    setup.runAllImportStepsFromProfile('profile-collective.cropimage:default', purge_old=False)
    logger.info('Installed collective.cropimage.')

    registry = getUtility(IRegistry)
    registry['collective.cropimage.ids'] = IDS
    keys = [item['id'] for item in IDS]
    for key in keys:
        message='collective.cropimage.ids updated with ID: "{0}"'.format(key)
        logger.info(message)
