from Products.ATContentTypes.interfaces.file import IATFile
from Products.ATContentTypes.interfaces.image import IATImage
from Products.CMFCore.utils import getToolByName
from sll.policy.setuphandlers import set_collections


import logging


PROFILE_ID = 'profile-sll.policy:default'


# def upgrade_1_to_2(context, logger=None):
#     """Remove unused roles."""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()
#     logger.info('Start removing unused roles.')
#     portal.__ac_roles__ = ('Contributor', 'Member', 'Site Administrator')
#     logger.info('Removed unused roles.')


# def upgrade_2_to_3(context, logger=None):
#     """Remove Reviewers group."""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)
#     groupstool = getToolByName(context, 'portal_groups')
#     logger.info('Start removing Reviewers group.')
#     groupstool.removeGroup('Reviewers')
#     logger.info('Removed Reviewers group.')


# def upgrade_3_to_4(context, logger=None):
#     """"Delete Removable Folder and copy_of_...."""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Update propertiestool.xml
#     properties = getToolByName(context, 'portal_properties')
#     site_properties = getattr(properties, 'site_properties')
#     logger.info('Disabling enable_link_integrity_checks.')
#     site_properties._updateProperty('enable_link_integrity_checks', False)
#     logger.info('Disabled enable_link_integrity_checks.')

#     # Get portal
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()

#     # Remove unnecessary contents
#     if portal.get('removable'):
#         logger.info('Start removing Removable Folder.')
#         portal.manage_delObjects(['removable'])
#         logger.info('Removable Folder Removed.')

#     catalog = getToolByName(context, 'portal_catalog')

#     brains = [brain for brain in catalog() if brain.id.startswith('copy')]
#     for brain in brains:
#         parent = aq_parent(brain.getObject())
#         path = brain.getPath()
#         ## Delete objects
#         message = "Start removing '{0}'.".format(path)
#         logger.info(message)
#         parent.manage_delObjects([brain.id])
#         message = "'{0}' removed.".format(path)
#         logger.info(message)

#     logger.info('All the contents id starting with "copy" removed.')

#     logger.info('Enabling enable_link_integrity_checks.')
#     site_properties._updateProperty('enable_link_integrity_checks', True)
#     logger.info('Enabled enable_link_integrity_checks.')

# def copy_paste_remove_others(context, object_provides, logger=None):
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Update propertiestool.xml
#     properties = getToolByName(context, 'portal_properties')
#     site_properties = getattr(properties, 'site_properties')
#     logger.info('Disabling enable_link_integrity_checks.')
#     site_properties._updateProperty('enable_link_integrity_checks', False)
#     logger.info('Disabled enable_link_integrity_checks.')

#     catalog = getToolByName(context, 'portal_catalog')
#     query = {
#         'object_provides': object_provides,
#     }
#     brains = catalog(query)
#     count = len(brains)
#     message = 'There are {0} {1} to copy, paste and remove.'.format(
#         count,
#         object_provides,
#     )
#     logger.info(message)

#     wftool = getToolByName(context, "portal_workflow")

#     for brain in brains:
#         obj = brain.getObject()
#         parent = aq_parent(obj)
#         path = brain.getPath()
#         bid = brain.id
#         state = brain.review_state
#         ## Copy objects
#         message = "Copying '{0}'.".format(path)
#         logger.info(message)
#         objs = parent.manage_copyObjects([bid])
#         message = "'{0}' copied.".format(path)
#         logger.info(message)
#         ## Past objects
#         message = "Pasting '{0}'.".format(path)
#         logger.info(message)
#         parent.manage_pasteObjects(objs)
#         message = "'{0}' pasted.".format(path)
#         logger.info(message)
#         ## Remove objects
#         message = "Removing '{0}'.".format(path)
#         logger.info(message)
#         parent.manage_delObjects([bid])
#         message = "'{0}' removed.".format(path)
#         logger.info(message)
#         ## Update ID
#         copied_id = 'copy_of_{0}'.format(bid)
#         copied = parent[copied_id]
#         message = 'Updating ID {0} --> {1}.'.format(copied_id, bid)
#         logger.info(message)
#         copied.setId(bid)
#         message = 'ID {0} --> {1} updated.'.format(copied_id, bid)
#         logger.info(message)
#         ## Update state
#         if state == 'published':
#             message = "Publishing '{0}'.".format(path)
#             logger.info(message)
#             wftool.doActionFor(copied, 'publish')
#             copied.reindexObject(idxs=['review_state'])
#             message = "'{0}' published.".format(path)
#             logger.info(message)

#         count -= 1
#         message = "{0} {1} left to update.".format(count, object_provides)
#         logger.info(message)

#     message = 'Update completed for {0}.'.format(
#         object_provides,
#     )
#     logger.info(message)
#     logger.info('Enabling enable_link_integrity_checks.')
#     site_properties._updateProperty('enable_link_integrity_checks', True)
#     logger.info('Enabled enable_link_integrity_checks.')


# def upgrade_12_to_13(context, logger=None):
#     """Copy paste and remove Content Types below:

#     """
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     object_provides = [
#         IATDocument.__identifier__,
#         IATEvent.__identifier__,
#         IATLink.__identifier__,
#         IATNewsItem.__identifier__,
#         IATTopic.__identifier__,
#         IPloneFormGenForm.__identifier__,
#     ]
#     copy_paste_remove_others(context, object_provides, logger=logger)


# def upgrade_13_to_14(context, logger=None):
#     """Update default topLevel to zero for navigation portlet.

#     """
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     portal_properties = getToolByName(context, 'portal_properties')
#     navtree_properties = getattr(portal_properties, 'navtree_properties')
#     logger.info('Setting topLevel to zero for navigation portlet.')
#     navtree_properties._updateProperty('topLevel', 0)
#     logger.info('Set topLevel to zero for navigation portlet.')


# def set_cropimage(context, logger):
#     """Setup collective.cropimage."""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     setup = getToolByName(context, 'portal_setup')
#     logger.info('Start installing collective.cropimage.')
#     setup.runAllImportStepsFromProfile('profile-collective.cropimage:default', purge_old=False)
#     logger.info('Installed collective.cropimage.')

#     registry = getUtility(IRegistry)
#     registry['collective.cropimage.ids'] = IDS
#     keys = [item['id'] for item in IDS]
#     for key in keys:
#         message = 'collective.cropimage.ids updated with ID: "{0}"'.format(key)
#         logger.info(message)


# def upgrade_16_to_17(context, logger=None):
#     """Update plone.portaltop"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     from zope.component import getUtility
#     from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
#     storage = getUtility(IViewletSettingsStorage)
#     logger.info('Unhiding plone.portalheader.')
#     storage.setHidden('plone.portaltop', '*', ())
#     logger.info('Unhid plone.portalheader.')

#     logger.info('Ordering plone.portalheader.')
#     storage.setOrder(
#         'plone.portalheader',
#         '*',
#         (
#             u'plone.skip_links',
#             u'plone.personal_bar',
#             u'plone.site_actions',
#             u'plone.app.i18n.locales.languageselector',
#             u'plone.searchbox',
#             u'plone.logo',
#             u'plone.global_sections',
#         )
#     )
#     storage.setHidden('plone.portalheader', '*', ())
#     logger.info('Ordered plone.portalheader.')


# def upgrade_17_to_18(context, logger=None):
#     """Remove log background"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Get portal
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()

#     oid = 'ylapalkin-tausta.png'
#     if portal.get(oid):
#         message = 'Removing {0}'.format(oid)
#         logger.info(message)
#         portal.manage_delObjects([oid])
#         message = 'Removed {0}'.format(oid)
#         logger.info(message)

#     properties = getToolByName(context, 'portal_properties')
#     folder_logo_properties = getattr(properties, 'folder_logo_properties')
#     logger.info('Removing backgroud.')
#     folder_logo_properties.manage_changeProperties(
#         background_color='',
#         background_image_id='',
#     )
#     logger.info('Removed background.')


# def upgrade_18_to_19(context, logger=None):
#     """Uninstall plonetheme.classic"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     installer = getToolByName(context, 'portal_quickinstaller')
#     product = 'plonetheme.classic'
#     if installer.isProductInstalled('plonetheme.classic'):
#         message = 'Uninstalling {0}.'.format(product)
#         logger.info(message)
#         installer.uninstallProducts(['plonetheme.classic'])
#         message = 'Uninstalled {0}.'.format(product)
#         logger.info(message)


# def upgrade_19_to_20(context, logger=None):
#     """Hide colophon and show site_actions"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     from zope.component import getUtility
#     from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
#     storage = getUtility(IViewletSettingsStorage)
#     logger.info('Hiding plone.colophon.')
#     storage.setHidden('plone.portalfooter', '*', (u'plone.colophon', u'plone.site_actions'))
#     logger.info('Hid plone.colophon.')

#     logger.info('Hiding plone.site_actions.')
#     storage.setOrder(
#         'plone.portalheader',
#         '*',
#         (
#             u'plone.skip_links',
#             u'plone.personal_bar',
#             u'plone.site_actions',
#             u'plone.app.i18n.locales.languageselector',
#             u'plone.searchbox',
#             u'plone.logo',
#             u'plone.global_sections',
#         )
#     )
#     logger.info('Hid plone.site_actions.')


# def upgrade_20_to_21(context, logger=None):
#     """Clean up browserlayer"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     from plone.browserlayer import utils
#     names = [item.getName() for item in utils.registered_layers()]
#     if 'IInicieCropimage' in names:
#         logger.info('Unregistering inicie.cropimage')
#         utils.unregister_layer('inicie.cropimage')
#         logger.info('Unregistered inicie.cropimage')


# def upgrade_21_to_22(context, logger=None):
#     """Update tabs"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Get portal
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()
#     catalog = getToolByName(context, 'portal_catalog')
#     query = {
#         'path': {
#             'query': '/'.join(portal.getPhysicalPath()),
#             'depth': 1,
#         }
#     }

#     # First exclude_from_nav all  onject under portal.
#     for brain in catalog(query):
#         if not brain.exclude_from_nav:
#             oid = brain.id
#             obj = brain.getObject()
#             message = "Excluding '{0}' from navigation.".format(oid)
#             logger.info(message)
#             obj.setExcludeFromNav(True)
#             obj.reindexObject(idxs=['exclude_from_nav'])
#             message = "Excluded '{0}' from navigation.".format(oid)
#             logger.info(message)

#     ids = [
#         'ajankohtaista',
#         'tapahtumat',
#         'mita-me-teemme',
#         'mita-sina-voit-tehda',
#         'liity-uusi',
#         'lahjoita-uusi',
#         'jarjesto',
#     ]
#     for oid in ids:
#         obj = portal.get(oid)
#         if obj:
#             message = "Including '{0}' to navigation.".format(oid)
#             logger.info(message)
#             obj.setExcludeFromNav(False)
#             obj.reindexObject(idxs=['exclude_from_nav'])
#             message = "Included '{0}' to navigation.".format(oid)
#             logger.info(message)


# def upgrade_22_to_23(context, logger=None):
#     """Setting front page to sll-view"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Get portal
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()

#     oid = 'index_html'
#     obj = portal.get(oid)
#     if obj:
#         logger.info('Moving index_html to copy_of_index_html.')
#         objs = portal.manage_copyObjects([oid])
#         portal.manage_pasteObjects(objs)
#         portal.manage_delObjects([oid])
#         logger.info('Moved index_html to copy_of_index_html.')

#     logger.info('Reinstalling sll.templates.')
#     installer = getToolByName(context, 'portal_quickinstaller')
#     installer.reinstallProducts(['sll.templates'])
#     logger.info('Reinstalled sll.templates.')

#     logger.info('Setting view to sll-view.')
#     portal.setLayout('sll-view')
#     logger.info('Set view to sll-view.')


# def upgrade_23_to_24(context, logger=None):
#     """Installs sll.portlet and sll.theme"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     installer = getToolByName(context, 'portal_quickinstaller')

#     if not installer.isProductInstalled('sll.portlet'):
#         logger.info('Reinstalling sll.portlet.')
#         installer.installProducts(['sll.portlet'])
#         setup = getToolByName(context, 'portal_setup')
#         setup.runImportStepFromProfile(PROFILE_ID, 'portlets', run_dependencies=False, purge_old=False)
#         logger.info('Reinstalled sll.portlet.')

#     if not installer.isProductInstalled('sll.theme'):
#         logger.info('Reinstalling sll.templates.')
#         installer.installProducts(['sll.theme'])
#         logger.info('Reinstalled sll.theme.')


# def upgrade_24_to_25(context, logger=None):
#     """Update ITopPageFeed"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     catalog = getToolByName(context, 'portal_catalog')
#     query = {'object_provides': IBaseTopPageFeed.__identifier__}
#     for brain in catalog(query):
#         bid = brain.id
#         obj = brain.getObject()
#         message = 'Getting rid of sll.policy.browser.interfaces.ITopPageFeed from {0}'.format(bid)
#         logger.info(message)
#         noLongerProvides(obj, IBaseTopPageFeed)
#         message = 'Got rid of sll.policy.browser.interfaces.ITopPageFeed from {0}'.format(bid)
#         logger.info(message)

#         message = 'Applying sll.templates.browser.interfaces.ITopPageFeed to {0}'.format(bid)
#         logger.info(message)
#         alsoProvides(obj, ITopPageFeed)
#         message = 'Applied sll.templates.browser.interfaces.ITopPageFeed to {0}'.format(bid)
#         obj.reindexObject(idxs=['object_provides'])
#         logger.info(message)


# def upgrade_25_to_26(context, logger=None):
#     """Remove twitter button"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     portal_actions = getToolByName(context, 'portal_actions')
#     document_actions = getattr(portal_actions, 'document_actions')
#     if hasattr(document_actions, 'addtofavorites'):
#         logger.info('Removing addtofavorites.')
#         document_actions.manage_delObjects(['addtofavorites'])
#         logger.info('Removed addtofavorites.')


# def upgrade_26_to_27(context, logger=None):
#     """Make mark_special_links to false"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     setup = getToolByName(context, 'portal_setup')
#     # Update filtering on workflow state by import propertiestool.xml.
#     logger.info('Start reimporting propertiestool.xml.')
#     setup.runImportStepFromProfile(
#         PROFILE_ID,
#         'propertiestool',
#         run_dependencies=False,
#         purge_old=False
#     )
#     logger.info('Reimported propertiestool.xml.')


# def upgrade_27_to_28(context, logger=None):
#     """Make login unvisible"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     logger.info('Making login unvisible.')
#     setup = getToolByName(context, 'portal_setup')
#     setup.runImportStepFromProfile(PROFILE_ID, 'actions', run_dependencies=False, purge_old=False)
#     logger.info('Made login unvisible.')


# def upgrade_28_to_29(context, logger=None):
#     """Make yhdistykset navigation root"""
#     if logger is None:
#         # Called as upgrade step: define our own logger.
#         logger = logging.getLogger(__name__)

#     # Get portal
#     portal_url = getToolByName(context, 'portal_url')
#     portal = portal_url.getPortalObject()

#     for piiri in YHDISTYKSET.keys():
#         parent = portal.get(piiri)
#         if parent is not None:
#             for oid in YHDISTYKSET[piiri]:
#                 obj = parent.get(oid)
#                 if obj:
#                     message = 'Making {0} navigation root.'.format(oid)
#                     logger.info(message)
#                     alsoProvides(obj, INavigationRoot)
#                     obj.reindexObject(idxs=['object_provides'])
#                     message = 'Made {0} navigation root.'.format(oid)
#                     logger.info(message)

#     set_cropimage(context, logger)


def upgrade_30_to_31(context, logger=None):
    """Reimport rolemap.xml for portlets."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    logger.info('Setting roles for portlet permissions.')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap', run_dependencies=False, purge_old=False)
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

    set_collections(context, logger=logger)
