# -*- coding: UTF-8 -*-

from Products.Five import BrowserView
from Products.CMFPlone.browser.ploneview import Plone as PloneBrowserView


class EventFolder(BrowserView):
    pass


class Folder(PloneBrowserView):

    def showEditableBorder(self):
        """
        Determine if the editable border should be shown
        """
        return super(Folder, self).showEditableBorder()
