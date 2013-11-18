from zope.interface import implements
from Products.Five import BrowserView
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs

from rapido.core.interfaces import IDatabase

class PhysicalNavigationBreadcrumbs(BrowserView):
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        base = ({'absolute_url': self.context.url(),
          'Title': self.context.Title(), },
        )
        local_url = self.request.URL.replace(self.context.url(), '')
        if local_url.split('/')[1] == 'document':
            docid = local_url.split('/')[2]
            doc = IDatabase(self.context).get_document(docid)
            base += ({
                'absolute_url': doc.url,
                'Title': doc.get_item('title', doc.id), },)

        return base