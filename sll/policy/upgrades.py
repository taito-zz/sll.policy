from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.file import IATFile
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from sll.policy.setuphandlers import set_collections


import logging


PROFILE_ID = 'profile-sll.policy:default'


def upgrade_30_to_31(context, logger=None):
    """Reimport rolemap.xml for portlets."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    logger.info('Setting roles for portlet permissions.')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(
        PROFILE_ID,
        'rolemap',
        run_dependencies=False,
        purge_old=False
    )
    logger.info('Set roles for portlet permissions.')

    logger.info('Setting default editor to TinyMCE.')
    setup.runImportStepFromProfile(
        PROFILE_ID,
        'propertiestool',
        run_dependencies=False,
        purge_old=False
    )
    logger.info('Set default editor to TinyMCE.')

    workflow = getToolByName(context, 'portal_workflow')
    workflow.setChainForPortalTypes(('File', 'Image', ), 'two_states_workflow')
    catalog = getToolByName(context, 'portal_catalog')
    query = {
        'object_provides': [
            IATFile.__identifier__,
            IATImage.__identifier__,
        ],
    }
    brains = catalog(query)
    for brain in brains:
        bid = brain.id
        obj = brain.getObject()
        if workflow.getInfoFor(obj, "review_state") == 'private':
            message = 'Publishing {0}'.format(bid)
            logger.info(message)
            workflow.doActionFor(obj, 'publish')
            message = 'Published {0}'.format(bid)
            logger.info(message)
    workflow.setChainForPortalTypes(('File', 'Image', ), '')

    installer = getToolByName(context, 'portal_quickinstaller')
    packages = ['abita.development', 'collective.searchevent']
    pacs = []
    for pac in packages:
        if not installer.isProductInstalled(pac):
            pacs.append(pac)
    message = 'Installing {0}.'.format(', '.join(pacs))
    logger.info(message)
    installer.installProducts(pacs)
    message = 'Installed {0}.'.format(', '.join(pacs))
    logger.info(message)


def upgrade_31_to_32(context, logger=None):
    """Set collections, search-result to tapahtumat default view."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    set_collections(context, logger=logger)

    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    folder = portal.get('tapahtumat')
    if folder:
        folder.setLayout('search-results')


def upgrade_32_to_33(context, logger=None):
    """Update schemata for subject, excludeFromNav and relatedItems."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    catalog = getToolByName(context, 'portal_catalog')
    query = {
        'object_provides': [
            IATFolder.__identifier__,
            IPloneFormGenForm.__identifier__
        ]
    }
    for brain in catalog(query):
        obj = brain.getObject()
        bid = brain.id
        message = 'Updating excludeFromNav to default schemata for {0}'.format(
            bid
        )
        logger.info(message)
        obj.schema.changeSchemataForField('excludeFromNav', 'default')
        message = 'Updated excludeFromNav to default schemata for {0}'.format(
            bid
        )
        logger.info(message)

    query = {
        'object_provides': [
            IATDocument.__identifier__,
            IATNewsItem.__identifier__
        ]
    }
    for brain in catalog(query):
        obj = brain.getObject()
        bid = brain.id
        schema = obj.schema
        message = 'Updating excludeFromNav and relatedItems to default schemata for {0}'.format(bid)
        logger.info(message)
        schema.changeSchemataForField('excludeFromNav', 'default')
        schema.changeSchemataForField('relatedItems', 'default')
        message = 'Updated excludeFromNav and relatedItems to default schemata for {0}'.format(bid)
        logger.info(message)

    query = {
        'object_provides': [
            IATEvent.__identifier__
        ]
    }
    for brain in catalog(query):
        obj = brain.getObject()
        bid = brain.id
        schema = obj.schema
        message = 'Updating subject, excludeFromNav and relatedItems to default schemata for {0}'.format(bid)
        logger.info(message)
        schema.changeSchemataForField('excludeFromNav', 'default')
        schema.changeSchemataForField('relatedItems', 'default')
        schema.changeSchemataForField('subject', 'default')
        message = 'Updated subject, excludeFromNav and relatedItems to default schemata for {0}'.format(bid)
        logger.info(message)

    setup = getToolByName(context, 'portal_setup')
    logger.info('Setting FormFolder to content.leadimage.')
    setup.runImportStepFromProfile(
        PROFILE_ID,
        'propertiestool',
        run_dependencies=False,
        purge_old=False
    )
    logger.info('Set FormFolder to content.leadimage.')


def disable_javascript(context, rid, logger=None):
    """Disable javascript"""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    javascripts = getToolByName(context, 'portal_javascripts')
    resource = javascripts.getResource(rid)
    if resource:
        message = 'Disabling {0}.'.format(rid)
        logger.info(message)
        resource.setEnabled(False)
        message = 'Disabled {0}.'.format(rid)
        logger.info(message)


def upgrade_33_to_34(context, logger=None):
    """Disable ++resource++search.js"""
    disable_javascript(context, '++resource++search.js')
