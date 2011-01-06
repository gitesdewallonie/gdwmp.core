from zope.app.component.interfaces import ISite
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite

LANGUAGES = ['fr', 'nl']


def install(context):
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    setupLanguages(portal)


def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 1
