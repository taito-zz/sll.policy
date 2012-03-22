from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.workflow.browser.sharing import SharingView

import inspect


class SLLSharingView(SharingView):

    prefix = '/'.join(
        inspect.getsourcefile(SharingView).split('/')[:-1]
    )
    template = ViewPageTemplateFile('sharing.pt', _prefix=prefix)

    @memoize
    def roles(self):
        """Get a list of roles that can be managed.

        Returns a list of dicts with keys:

            - id
            - title
        """
        pairs = super(SLLSharingView, self).roles()
        ids = [u'Reader', u'Reviewer']
        return [
            pair for pair in pairs if pair['id'] not in ids
        ]
