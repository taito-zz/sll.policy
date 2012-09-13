from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.file import IATFile
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


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


def upgrade_34_to_35(context, logger=None):
    """Disable Marker Interfaces."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)
    from collective.cart.core.interfaces.marker import IPotentiallyAddableToCart
    from collective.cart.core.interfaces.marker import IAddableToCart
    from collective.cart.core.interfaces.marker import IProductAnnotations
    from collective.cart.core.interfaces.marker import ICartAware
    from zope.interface import noLongerProvides
    catalog = getToolByName(context, 'portal_catalog')
    query = {
        'object_provides': [
            IPotentiallyAddableToCart.__identifier__,
            IAddableToCart.__identifier__,
            IProductAnnotations.__identifier__,
            ICartAware.__identifier__]
    }
    for brain in catalog(query):
        bid = brain.id
        obj = brain.getObject()
        message = 'Disabling marker interfaces from {0}.'.format(bid)
        logger.info(message)
        noLongerProvides(obj, IPotentiallyAddableToCart)
        noLongerProvides(obj, IAddableToCart)
        noLongerProvides(obj, IProductAnnotations)
        noLongerProvides(obj, ICartAware)
        message = 'Disabled marker interfaces from {0}.'.format(bid)
        logger.info(message)
        obj.reindexObject(idxs=['object_provides'])


def upgrade_36_to_37(context, logger=None):
    """Reimport atcttool."""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting atcttool')
    setup.runImportStepFromProfile(
        'profile-Products.CMFPlone:plone', 'atcttool', run_dependencies=False, purge_old=True)
    logger.info('Reimported atcttool')

    registry = getUtility(IRegistry)
    for record in registry.records:
        rec = registry.records.get(record)
        obj = rec.field
        message = "Setting attribute 'defaultFactory' to record: '{0}'.".format(record)
        logger.info(message)
        loop = True
        while loop:
            if not hasattr(obj, 'defaultFactory'):
                setattr(obj, 'defaultFactory', None)
            if getattr(obj, 'key_type', None) is not None:
                if not hasattr(obj.key_type, 'defaultFactory'):
                    setattr(obj.key_type, 'defaultFactory', None)
            if getattr(obj, 'value_type', None) is not None:
                if not hasattr(obj.value_type, 'defaultFactory'):
                    setattr(obj.value_type, 'defaultFactory', None)
                    obj = obj.value_type
                else:
                    loop = False
            else:
                loop = False
        message = "Set attribute 'defaultFactory' to record: '{0}'.".format(record)
        logger.info(message)


def upgrade_37_to_38(context, logger=None):
    """Update users wysiwyg_editor to TinyMCE."""
    if logger is None:
        logger = logging.getLogger(__name__)

    membership = getToolByName(context, 'portal_membership')
    for mid in membership.listMemberIds():
        member = membership.getMemberById(mid)
        if member.getProperty('wysiwyg_editor') != 'TinyMCE':
            logger.info(
                "Setting wysiwyg_editor to TinyMCE for {}.".format(mid))
            member.manage_changeProperties(wysiwyg_editor='TinyMCE')
            logger.info(
                "Set wysiwyg_editor to TinyMCE for {}.".format(mid))
