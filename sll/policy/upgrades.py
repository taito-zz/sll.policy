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


def upgrade_3_to_4(context, logger=None):
    """"Update workflow."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
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
