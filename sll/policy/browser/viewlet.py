from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.viewlets.common import PathBarViewlet
from zope.component import getMultiAdapter


class HeadViewlet(PathBarViewlet):

    index = ViewPageTemplateFile('viewlets/head.pt')

    def update(self):
        if not IPloneSiteRoot.providedBy(self.context):
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
