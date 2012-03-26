from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot

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

    # Remove unnecessary contents
    if portal.get('removable'):
        logger.info('Start removing Removable Folder.')
        portal.manage_delObjects(['removable'])
        logger.info('Removable Folder Removed.')


def update_contents(context, paths, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

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
                # obj.reindexObject(idxs=['review_state'])
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
