from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def exclude_from_nav(context, content):
    if not content.exclude_from_nav():
        log = context.getLogger(__name__)
        content.setExcludeFromNav(True)
        content.reindexObject(idxs=['exclude_from_nav'])
        message = 'Folder "{0}" excluded from navigation.'.format(content.id)
        log.info(message)


def setUpMembersFolder(context):
    portal = context.getSite()
    members = portal.get('Members')
    if members:
        exclude_from_nav(context, members)


def createFolder(context, id):
    portal = context.getSite()
    folder = portal.get(id)
    if not folder:
        folder = portal[
            portal.invokeFactory(
                'Folder',
                id,
                title=id.capitalize(),
            )
        ]
        folder.reindexObject()
        log = context.getLogger(__name__)
        message = 'Folder "{0}" created.'.format(id)
        log.info(message)
        exclude_from_nav(context, folder)


def add_inicie_cropimage_ids(context):
    registry = getUtility(IRegistry)
    ids = registry['inicie.cropimage.ids']
    log = context.getLogger(__name__)
    log.info('')


def setupVarious(context):

    if context.readDataFile('sll.policy_various.txt') is None:
        return

    setUpMembersFolder(context)
    items = ['medialle', 'yhteistiedot', 'english', 'svenska']
    for item in items:
        createFolder(context, item)
    add_inicie_cropimage_ids(context)
