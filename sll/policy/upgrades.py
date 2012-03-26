from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

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
            new_id = '_'.join(brain.id.split('_')[2:])
            new_path = brain.getPath()
            obj = brain.getObject()
            obj.setId(new_id)
            message = "Path: '{0}' --> '{1}'".format(new_path, path)
            logger.info(message)
            path = '/'.join(obj.getPhysicalPath())
            if path in will_be_published_paths:
                message = "Start publishing '{0}'.".format(path)
                logger.info(message)
                wftool.doActionFor(obj, 'publish')
                message = "'{0}' published.".format(path)
                logger.info(message)

            obj.reindexObject()

            message = "'{0}' updated.".format(path)
            logger.info(message)
        return paths


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


def upgrade_4_to_5(context, logger=None):
    """Remove all id starting from copy_of..."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

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


def upgrade_5_to_6(context, logger=None):
    """"Update workflow."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # First import workflow.xml
    setup = getToolByName(context, 'portal_setup')

    logger.info('Start reimporting workflows.xml.')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow', run_dependencies=False, purge_old=False)
    logger.info('Reimported workflows.xml.')

    # Get portal
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()

    paths = '/'.join(portal.getPhysicalPath())
    while paths:
        paths = update_contents(context, paths, logger=logger)
    logger.info('Whole Contents Updated.')


def upgrade_6_to_7(context, logger=None):
    """"Rebuild catalog."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    catalog = getToolByName(context, 'portal_catalog')

    logger.info('Start recataloging whole contents.')
    catalog.clearFindAndRebuild()
    logger.info('Whole Contents are now recataloged.')
