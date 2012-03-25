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
    portal.__ac_roles__ = ('Contributor', 'Member', 'Site Administrator')
    logger.info('Removed unused roles.')


def upgrade_2_to_3(context, logger=None):
    """Remove Reviewers group."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
    groupstool = getToolByName(context, 'portal_groups')
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
            objs = folder.manage_copyObjects([brain.id])
            ## Past objects
            folder.manage_pasteObjects(objs)
            ## Delete objects
            folder.manage_delObjects([brain.id])
            if (
                brain.review_state == 'published'
            ) or (
                brain.review_state == 'visible'
            ):
               will_be_published_paths.append(path)

        wftool = getToolByName(folder, "portal_workflow")

        for brain in catalog(query):
            new_id = brain.id[8:]
            new_path = brain.getPath()
            obj = brain.getObject()
            obj.setId(new_id)
            if new_path in will_be_published_paths:
                wftool.doActionFor(obj, 'publish')
                obj.reindexObject(idxs=['review_state'])
            obj.reindexObject()
            path = '/'.join(obj.getPhysicalPath())

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
        portal.manage_delObjects(['removable'])
        logger.info('Removable Folder Removed.')


def upgrade_4_to_5(context, logger=None):
    """"Update workflow."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    # First import workflow.xml
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow', run_dependencies=False, purge_old=False)
    logger.info('Reimported workflows.xml')

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
    catalog.clearFindAndRebuild()
    logger.info('Whole Contents are now recataloged.')