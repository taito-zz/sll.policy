from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

import logging


PROFILE_ID = 'profile-sll.policy:default'


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
            member.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
            logger.info(
                "Set wysiwyg_editor to TinyMCE for {}.".format(mid))

    setup = getToolByName(context, 'portal_setup')
    logger.info('Setting available_editor only to TinyMCE.')
    setup.runImportStepFromProfile(
        PROFILE_ID,
        'propertiestool',
        run_dependencies=False,
        purge_old=False)
    logger.info('Set available_editor only to TinyMCE.')


def upgrade_38_to_39(context, logger=None):
    """Reimport typeinfo for updating allowed_content_types for Plone Site"""
    if logger is None:
        logger = logging.getLogger(__name__)

    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting typeinfo.')
    setup.runImportStepFromProfile(
        PROFILE_ID, 'typeinfo', run_dependencies=False, purge_old=False)
    logger.info('Reimported typeinfo.')


def remove_portlet(context, portlet_class, logger):
    """Remove portlet from left and right columns."""

    catalog = getToolByName(context, 'portal_catalog')
    for brain in catalog(Language="all"):
        obj = brain.getObject()
        for col in [u"plone.leftcolumn", u"plone.rightcolumn"]:
            column = getUtility(IPortletManager, name=col)
            assignable = getMultiAdapter((obj, column), IPortletAssignmentMapping)
            for key in assignable.keys():
                if isinstance(assignable[key], portlet_class):
                    del assignable[key]


def upgrade_39_to_40(context, logger=None):
    """Remove fblike portlet"""
    if logger is None:
        logger = logging.getLogger(__name__)

    from collective.portlet.fblikebox.likeboxportlet import Assignment
    remove_portlet(context, Assignment, logger)
