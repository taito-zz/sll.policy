def setUpMembersFolder(context):
    portal = context.getSite()
    members = portal.get('Members')
    if members and not members.exclude_from_nav():
        log = context.getLogger(__name__)
        members.setExcludeFromNav(True)
        members.reindexObject(idxs=['exclude_from_nav'])
        log.info('Member folder excluded from navigation.')


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


def setupVarious(context):

    if context.readDataFile('sll.policy_various.txt') is None:
        return

    setUpMembersFolder(context)
    items = ['medialle', 'yhteistiedot', 'english', 'svenska']
    for item in items:
        createFolder(context, item)

