# -*- coding: UTF-8 -*-

from AccessControl import getSecurityManager
from Products.Five import BrowserView
from Products.CMFPlone.browser.ploneview import Plone as PloneBrowserView


class EventFolder(BrowserView):
    pass


class Folder(PloneBrowserView):

    def showEditableBorder(self):
        """
        Determine if the editable border should be shown
        It should never be shown to Proprietaires
        """
        loggedUser = getSecurityManager().getUser()
        roles = list(loggedUser.getRoles())
        if 'Proprietaire' in roles:
            return False
        else:
            return super(Folder, self).showEditableBorder()
