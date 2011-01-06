from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.app.component.interfaces import ISite
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite

LANGUAGES = ['fr', 'nl']


def install(context):
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    setupLanguages(portal)
    clearPortlets(portal)
    setupNavigationPortlet(portal)


def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 1


def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')


def setupNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager, ), IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=0,
                                       bottomLevel=2)
    assignments['navtree'] = assignment


def clearColumnPortlets(folder, column):
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager, ), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]


def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn', context=folder)
    return manager
