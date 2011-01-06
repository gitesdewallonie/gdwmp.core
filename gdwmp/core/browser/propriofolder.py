# -*- coding: UTF-8 -*-

from zope.interface import alsoProvides

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gdwmp.core.browser.interfaces import IProprioFolder


class ProprioFolder(BrowserView):
    interface = None
    language = ''

    def isConfigured(self):
        obj = self.context
        return IProprioFolder.providedBy(obj)

    def changeStatus(self):
        obj = self.context
        putils = getToolByName(self, 'plone_utils')

        if not self.isConfigured():
            alsoProvides(obj, IProprioFolder)
            obj.reindexObject()
            putils.addPortalMessage(u"Configuration du dossier proprio réussie. \
                                      N'oubliez pas de configurer le partage du dossier au propriétaire ...")
            # XXX do folder creation/configuration here

        self.request.response.redirect(obj.absolute_url())
        return ''
