from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.Five.browser import BrowserView
from sll.policy.browser.interfaces import ITopPageFeed
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class Miscellaneous(BrowserView):

    def feedable_to_top(self):
        return (
            IATDocument.providedBy(
                self.context
            ) or IATEvent.providedBy(
                self.context
            ) or IATNewsItem.providedBy(
                self.context
            )
        ) and not ITopPageFeed.providedBy(
            self.context
        )

    def unfeedable_from_top(self):
       return (
           IATDocument.providedBy(
                self.context
            ) or IATEvent.providedBy(
                self.context
            ) or IATNewsItem.providedBy(
                self.context
            )
        ) and ITopPageFeed.providedBy(
            self.context
        ) 

    def feed_to_top(self):
        alsoProvides(self.context, ITopPageFeed)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def unfeed_from_top(self):
        noLongerProvides(self.context, ITopPageFeed)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
