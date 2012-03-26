from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from sll.policy.config import IDS
from zope.component import getUtility

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
    """"Delete Removable Folder."""
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


def update_contents(context, paths, logger=None):
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

    catalog = getToolByName(context, 'portal_catalog')

    query = {
        'path': {
            'query': paths,
            'depth': 1,
        }
    }

    brains = catalog(query)
    if brains:
        paths = [brain.getPath() for brain in brains]
        will_be_published_paths = []
        for brain in brains:
            obj = brain.getObject()
            folder = aq_parent(obj)
            path = brain.getPath()
            ## exclude_from_nav
            if INavigationRoot.providedBy(folder):
                if brain.review_state != 'published':
                    message = "Start excluding '{0}' from navigation.".format(path)
                    logger.info(message)
                    obj.setExcludeFromNav(True)
                    message = "'{0}' excluded from navigation.".format(path)
                    logger.info(message)

            ## Copy objects
            message = "Start copying '{0}'.".format(path)
            logger.info(message)
            objs = folder.manage_copyObjects([brain.id])
            message = "'{0}' copied.".format(path)
            logger.info(message)
            ## Past objects
            message = "Start pasting '{0}'.".format(path)
            logger.info(message)
            folder.manage_pasteObjects(objs)
            message = "'{0}' pasted.".format(path)
            logger.info(message)
            ## Delete objects
            message = "Start removing '{0}'.".format(path)
            logger.info(message)
            folder.manage_delObjects([brain.id])
            if (
                brain.review_state == 'published'
            ) or (
                brain.review_state == 'visible'
            ):
                will_be_published_paths.append(path)
            message = "'{0}' removed.".format(path)
            logger.info(message)

        wftool = getToolByName(folder, "portal_workflow")

        for brain in catalog(query):
            new_id = brain.id[8:]
            new_path = brain.getPath()
            obj = brain.getObject()
            obj.setId(new_id)
            path = '/'.join(obj.getPhysicalPath())
            if new_path in will_be_published_paths:
                message = "Start publishing '{0}'.".format(path)
                logger.info(message)
                wftool.doActionFor(obj, 'publish')
                message = "'{0}' published.".format(path)
                logger.info(message)

            obj.reindexObject()

            message = "'{0}' updated.".format(path)
            logger.info(message)
        return paths


def upgrade_4_to_5(context, logger=None):
    """"Update workflow."""
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

    # Get portal
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()

    paths = '/'.join(portal.getPhysicalPath())
    while paths:
        paths = update_contents(context, paths, logger=logger)
    logger.info('Whole Contents Updated.')


def upgrade_5_to_6(context, logger=None):
    """"Rebuild catalog."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    catalog = getToolByName(context, 'portal_catalog')

    logger.info('Start recataloging whole contents.')
    catalog.clearFindAndRebuild()
    logger.info('Whole Contents are now recataloged.')


def upgrade_6_to_7(context, logger=None):
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
