# -*- coding: utf-8 -*-
# from plone.registry.interfaces import IRegistry
# from sll.policy.config import IDS
# from zope.component import getUtility


# def exclude_from_nav(context, content):
#     if not content.exclude_from_nav():
#         log = context.getLogger(__name__)
#         content.setExcludeFromNav(True)
#         content.reindexObject(idxs=['exclude_from_nav'])
#         message = 'Folder "{0}" excluded from navigation.'.format(content.id)
#         log.info(message)


# def setUpMembersFolder(context):
#     portal = context.getSite()
#     members = portal.get('Members')
#     if members:
#         exclude_from_nav(context, members)


# def createFolder(context, id, title=None, exclude=True, Subject=None, View=None):
#     portal = context.getSite()
#     folder = portal.get(id)
#     if not folder:
#         title = title or id.capitalize()
#         folder = portal[
#             portal.invokeFactory(
#                 'Folder',
#                 id,
#                 title=title,
#             )
#         ]
#         log = context.getLogger(__name__)
#         message = 'Folder "{0}" created.'.format(id)
#         log.info(message)
#         if exclude:
#             exclude_from_nav(context, folder)
#         if Subject:
#             folder.setSubject(Subject)
#             message = 'Subject: "{0}" added to Folder: "{1}"'.format(Subject, id)
#             log.info(message)
#         if View:
#             folder.setLayout(View)
#             message = 'default_view for Folder: "{0}" set to Folder: "{1}"'.format(id, View)
#             log.info(message)
#         folder.reindexObject()


# def remove_folder(context, folder_id):
#     portal = context.getSite()
#     folder = portal.get(folder_id)
#     if folder:
#         log = context.getLogger(__name__)
#         folder.unindexObject()
#         del portal[folder_id]
#         message = 'Folder "{0}" removed'.format(folder_id)
#         log.info(message)


# def add_collective_cropimage_ids(context):
#     registry = getUtility(IRegistry)
#     registry['collective.cropimage.ids'] = IDS
#     keys = [item['id'] for item in IDS]
#     log = context.getLogger(__name__)
#     for key in keys:
#         message='collective.cropimage.ids updated with ID: "{0}"'.format(key)
#         log.info(message)


def setupVarious(context):

    if context.readDataFile('sll.policy_various.txt') is None:
        return

    # add_collective_cropimage_ids(context)
