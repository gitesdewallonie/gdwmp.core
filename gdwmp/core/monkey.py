from Acquisition import aq_inner
from zope.component import queryUtility, getMultiAdapter
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from gdwmp.core.browser.translations import translateId


def bodyClass(self, template, view):
    """Returns the CSS class to be used on the body tag.
    """
    context = self.context
    url = getToolByName(context, "portal_url")

    # template class (required)
    name = ''
    if isinstance(template, ViewPageTemplateFile):
        # Browser view
        name = view.__name__
    else:
        name = template.getId()
    body_class = 'template-%s' % name

    # portal type class (optional)
    normalizer = queryUtility(IIDNormalizer)
    portal_type = normalizer.normalize(context.portal_type)
    if portal_type:
        body_class += " portaltype-%s" % portal_type

    # section class (optional)
    contentPath = url.getRelativeContentPath(context)
    # due to LinguaPlone creating language sections, we can no longer refer
    # to contentPath[0], contentPath[1] should be used (ex URL /fr/front-page)
    if contentPath and len(contentPath) > 1:
        body_class += " section-%s" % contentPath[1]

    # class for hiding icons (optional)
    if self.icons_visible():
        body_class += ' icons-on'

    return body_class


def all_events_link(self):
    context = aq_inner(self.context)
    portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
    lang = portal_state.language()
    return translateId('ateliers', lang)
