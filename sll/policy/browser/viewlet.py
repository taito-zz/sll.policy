from plone.app.layout.viewlets.common import PathBarViewlet
from Acquisition import aq_inner, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import getMultiAdapter


class HeadViewlet(PathBarViewlet):

    index = ViewPageTemplateFile('viewlets/head.pt')

    def update(self):
        self.request.set('disable_plone.rightcolumn', True)


class PathBarViewlet(PathBarViewlet):

    index = render = ViewPageTemplateFile('viewlets/path_bar.pt')

    @property
    def portal_url(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        return portal_state.portal_url()

    @property
    def root(self):
        context = aq_inner(self.context)
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
        return context

    @property
    def available(self):
        return not IPloneSiteRoot.providedBy(self.root)
