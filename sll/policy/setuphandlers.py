import logging


def create_folder(context, oid, logger=None):
    """Create folder."""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(__name__)

    portal = context.getSite()
    folder = portal.get(oid)
    if not folder:
        folder = portal[
            portal.invokeFactory(
                'Folder',
                oid,
                title=oid.capitalize(),
            )
        ]
        folder.reindexObject()


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
    create_folder(context, 'tapahtumat')
    portal = context.getSite()
    portal['tapahtumat'].setLayout('search-results')
