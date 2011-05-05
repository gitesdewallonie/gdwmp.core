from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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
