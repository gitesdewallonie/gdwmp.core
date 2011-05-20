# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView


def translateId(strId, lang):
    if lang == 'fr':
        return strId

    elif lang == 'nl':
        if strId == 'recettes':
            return 'recepten'
        if strId == 'evenements':
            return 'evenementen'
        if strId == 'photos':
            return 'fotos'
        if strId == 'ateliers':
            return 'atelieren'


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
        return translateId(path, lang)

        # obj = self.context.restrictedTraverse(path)
        # translatedObject = obj.getTranslation()
        # if translatedObject:
        #     url = translatedObject.absolute_url()
        # else:
        #     url = obj.absolute_url()
        # return url
