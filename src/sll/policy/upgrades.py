from Products.CMFCore.utils import getToolByName
# from abita.utils.utils import reimport_profile
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from sll.basepolicy.upgrades import set_record_abita_development_rate
from zope.component import getMultiAdapter
from zope.component import getUtility

import logging


logger = logging.getLogger(__name__)


PROFILE_ID = 'profile-sll.policy:default'


def disable_javascript(context, rid):
    """Disable javascript"""
    javascripts = getToolByName(context, 'portal_javascripts')
    resource = javascripts.getResource(rid)
    if resource:
        message = 'Disabling {0}.'.format(rid)
        logger.info(message)
        resource.setEnabled(False)
        message = 'Disabled {0}.'.format(rid)
        logger.info(message)


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
                    logger.info('Removing {} from {} of {}.'.format(key, col, '/'.join(obj.getPhysicalPath())))
                    del assignable[key]


def upgrade_memberdata_properties(context, logger=None):
    """Update memberdata"""
    if logger is None:
        logger = logging.getLogger(__name__)

    setup = getToolByName(context, 'portal_setup')
    logger.info('Updating memberdata-properties.')
    setup.runImportStepFromProfile(PROFILE_ID, 'memberdata-properties', run_dependencies=False, purge_old=False)


def upgrade_40_to_41(context, logger=None):
    """Enable visible_ids for all the registred members."""
    if logger is None:
        logger = logging.getLogger(__name__)

    # First enabale visble_ids for coming members.
    upgrade_memberdata_properties(context, logger)

    membership = getToolByName(context, 'portal_membership')
    for mid in membership.listMemberIds():
        member = membership.getMemberById(mid)
        if not member.getProperty('visible_ids'):
            logger.info(
                "Setting visible_ids True".format(mid))
            member.setMemberProperties({'visible_ids': True})


def reset_record_abita_development_rate(context):
    """Set record: abita.development.rate"""
    set_record_abita_development_rate(5.0)


def unregister_layer_ISLLPolicyLayer(context):
    """Unregister ISLLPolicyLayer"""
    from plone.browserlayer import utils
    utils.unregister_layer('sll.policy')


# def register_layer_ISllPolicyLayer(context):
#     """Register ISllPolicyLayer"""
#     reimport_profile(context, PROFILE_ID, 'browserlayer')
