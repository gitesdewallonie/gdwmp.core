# -*- coding: UTF-8 -*-

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import ManagePortal

from gdwmp.core.browser.interfaces import IMakeProprioFolderMenu, \
                                          IMakeProprioFolderMenuItem, \
                                          IProprioFolder


class MakeProprioFolderMenu(BrowserMenu):
    implements(IMakeProprioFolderMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        menu=[]
        url=context.absolute_url()
        context_state=getMultiAdapter((context, request),
                name="plone_context_state")
        site=getUtility(ISiteRoot)
        mt=getToolByName(context, "portal_membership")
        if mt.checkPermission(ManagePortal, site):
            title = ""
            if not IProprioFolder.providedBy(context):
                title = "Configurer ce dossier proprio"
                icon = 'add_icon.gif'
                menu.append({
                    "title": title,
                    "description": u'',
                    "action": url + "/@@makeProprioFolder",
                    "selected": False,
                    "icon": icon,
                    "extra": {"id": "makeProprioFolder",
                               "separator": None,
                               "class": ""},
                    "submenu": None})
        return menu


class MakeProprioFolderMenuItem(BrowserSubMenuItem):
    implements(IMakeProprioFolderMenuItem)

    title = ""
    description = ""
    submenuId = "plone_contentmenu_propriofolder"

    order = 5
    extra = {"id": "plone-contentmenu-propriofolder"}

    @property
    def action(self):
        # doesn't need to do anything for now
        # because all powerusers should have js activated
        return self.context.absolute_url()

    def available(self):
        # only available in Proprio folders
        return (self.context.portal_type == 'Proprio')

    def disabled(self):
        return False

    def selected(self):
        return False

    @property
    def title(self):
        return u'Dossier proprio'
