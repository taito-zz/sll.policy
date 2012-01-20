def setUpMembersFolder(portal):
    members = portal.get('Members')
    if members and not members.exclude_from_nav():
        members.setExcludeFromNav(True)
        members.reindexObject(idxs=['exclude_from_nav'])


def setupVarious(context):

    if context.readDataFile('sll.policy_various.txt') is None:
        return

    portal = context.getSite()
    setUpMembersFolder(portal)
