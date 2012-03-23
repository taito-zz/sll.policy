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


def update_contents(folder):
    catalog = getToolByName(folder, 'portal_catalog')
    # if paths is None:
    path = '/'.join(folder.getPhysicalPath())
    query = {
        'path': {
            'query': path,
            'depth': 1,
        }
    }
    brains = catalog(query)
    ids = [brain.id for brain in brains]
    # paths = [brain.getPath() for brain in brains]
    ## Copy objects
    objs = folder.manage_copyObjects(ids)
    ## Past objects
    folder.manage_pasteObjects(objs)
    ## Delete objects
    folder.manage_delObjects(ids)
    will_be_published_ids = [
        brain.id for brain in brains if (
            brain.review_state == 'published' or brain.review_state == 'visible'
        )
    ]
    wftool = getToolByName(folder, "portal_workflow")
    for brain in catalog(query):
        new_id = brain.id[8:]
        obj = brain.getObject()
        obj.setId(new_id)
        if new_id in will_be_published_ids:
            wftool.doActionFor(obj, 'publish')
            obj.reindexObject(idxs=['review_state'])
        obj.reindexObject(idxs=['getId', 'id'])
    return catalog(query)


def upgrade_3_to_4(context, logger=None):
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

    update_contents(portal)

    # catalog = getToolByName(context, 'portal_catalog')

    # wftool = getToolByName(context, "portal_workflow")

# def upgrade_1_to_2(context, logger=None):
#     """Update worlflow"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()
#     kuvia = portal['kuvia']
#     info = portal['info']
#     workflowTool = getToolByName(context, "portal_workflow")
#     # chain = workflowTool.getChainFor(kuvia)
#     # workflowTool.getWorkflowsFor(kuvia)
#     # workflowTool.getWorkflowsFor(info)
#     # workflowTool.getInfoFor(kuvia, "review_state")
#     # workflowTool.getInfoFor(info, "review_state")
#     # workflowTool.doActionFor(kuvia, 'publish', id='sll_default_workflow')
#     import pdb; pdb.set_trace()

# def upgrade_2_to_3(context, logger=None):
#     """Install hexagonit.foldercontents."""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     installer = getToolByName(context, 'portal_quickinstaller')
#     installer.uninstallProducts(['NewSllSkin'])

#     setup = getToolByName(context, 'portal_setup')
#     setup.runAllImportStepsFromProfile('profile-sll.theme:default', purge_old=False)
#     logger.info('Installed sll.theme')
