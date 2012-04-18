def remove_folder(context, folder_ids):
    portal = context.getSite()
    ids = [fid for fid in folder_ids if portal.get(fid)]
    if ids:
        portal.manage_delObjects(ids)
        message = 'Folder ID: {0} removed'.format(', '.join(ids))
        log = context.getLogger(__name__)
        log.info(message)


def setupVarious(context):

    if context.readDataFile('sll.policy_various.txt') is None:
        return

    folder_ids = ['Members', 'news', 'events']
    remove_folder(context, folder_ids)
