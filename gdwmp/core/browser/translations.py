# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView


class Translate(BrowserView):
    """
    Translate object
    """

    def getTranslatedObjectUrl(self, path):
        """
        """
        # XXX quick translate. Use real locales after production deadline
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        lang = portal_state.language()

        if lang == 'fr':
            return path

        elif lang == 'nl':
            if path == 'recettes':
                return 'recepten'
            if path == 'evenements':
                return 'evenementen'

        # obj = self.context.restrictedTraverse(path)
        # translatedObject = obj.getTranslation()
        # if translatedObject:
        #     url = translatedObject.absolute_url()
        # else:
        #     url = obj.absolute_url()
        # return url
