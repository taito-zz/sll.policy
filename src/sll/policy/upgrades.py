from Products.CMFCore.utils import getToolByName
from sll.basepolicy.upgrades import set_record_abita_development_rate

import logging


logger = logging.getLogger(__name__)


PROFILE_ID = 'profile-sll.policy:default'


def reset_record_abita_development_rate(context):
    """Set record: abita.development.rate"""
    set_record_abita_development_rate(5.0)


def unregister_layer_ISLLPolicyLayer(context):
    """Unregister ISLLPolicyLayer"""
    from plone.browserlayer import utils
    utils.unregister_layer('sll.policy')


def excludeFromNav(context, logger=None):
    """Exclude from navigation"""
    if logger is None:
        logger = logging.getLogger(__name__)

    paths = [
        '/uusimaa/kannanotot',
        '/uusimaa/tiedotus',
        '/uusimaa/toiminta',
        '/etela-karjala/tiedotus',
        '/pohjois-savo/kannanotot',
        '/pohjois-savo/toiminta',
        '/satakunta/toiminta',
        '/satakunta/kannanotot',
        '/pohjois-pohjanmaa/kannanotot',
        '/pohjois-pohjanmaa/tiedotteet',
        '/lappi/tiedotteet',
        '/lappi/edunvalvonta',
        '/lappi/kolumnit',
    ]
    portal = getToolByName(context, 'portal_url').getPortalObject()
    catalog = getToolByName(context, 'portal_catalog')
    for path in paths:
        path = '{}{}'.format('/'.join(portal.getPhysicalPath()), path)
        for brain in catalog(path=path):
            obj = brain.getObject()
            obj.setExcludeFromNav(True)
            obj.reindexObject(idxs=['exclude_from_nav'])
        for brain in catalog(path={'query': path, 'depth': 0}):
            obj = brain.getObject()
            obj.setExcludeFromNav(False)
            obj.reindexObject(idxs=['exclude_from_nav'])


def set_view_for_tapahtumat(context, logger=None):
    """Set view: @@search-event-results for folder: tapahtumat"""
    if logger is None:
        logger = logging.getLogger(__name__)

    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal['tapahtumat'].setLayout('search-event-results')
