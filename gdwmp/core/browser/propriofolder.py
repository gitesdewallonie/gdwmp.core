# -*- coding: UTF-8 -*-

from zope.interface import alsoProvides

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gdwmp.core.browser.interfaces import IProprioFolder
from gdwmp.core.setuphandlers import createFolder, changeFolderView, \
                                     createTranslationForObject


class ProprioFolder(BrowserView):

    def isConfigured(self):
        obj = self.context
        return IProprioFolder.providedBy(obj)

    def changeStatus(self):
        obj = self.context
        putils = getToolByName(self, 'plone_utils')

        if not self.isConfigured():
            alsoProvides(obj, IProprioFolder)

            recettesFolder = createFolder(obj, 'recettes', 'Recettes')
            recettesFolder.setLanguage('fr')
            translatedFolder = createTranslationForObject(recettesFolder, \
                                                          newId='recepten')
            restrictFolderTypes(recettesFolder, ['Recette', 'File', 'Image'])
            restrictFolderTypes(translatedFolder, ['Recette', 'File', 'Image'])

            galleryFolder = createFolder(obj, 'photos', 'Photos')
            galleryFolder.setLanguage('')
            changeFolderView(galleryFolder, 'galleryview')
            restrictFolderTypes(galleryFolder, ['Image'])

            eventsFolder = createFolder(obj, 'evenements', 'Evénements')
            eventsFolder.setLanguage('fr')
            translatedFolder = createTranslationForObject(eventsFolder, \
                                                          newId='evenementen')
            restrictFolderTypes(eventsFolder, ['Event'])
            restrictFolderTypes(translatedFolder, ['Event'])
            changeFolderView(eventsFolder, 'folder_full_view')
            changeFolderView(translatedFolder, 'folder_full_view')

            obj.invokeFactory('Hebergement', 'descriptif', 'Descriptif')
            descriptif = getattr(obj, 'descriptif')
            descriptif.setLanguage('fr')
            translatedPage = createTranslationForObject(descriptif, \
                                                        newId='beschrijving')
            descriptif.setExcludeFromNav(True)
            translatedPage.setExcludeFromNav(True)
            obj.setDefaultPage('descriptif')
            obj.reindexObject()

            putils.addPortalMessage(u"Configuration du dossier proprio réussie. \
                                      N'oubliez pas de configurer le partage \
                                      du dossier 'Evénements' au propriétaire ...")

        self.request.response.redirect(obj.absolute_url())
        return ''


def restrictFolderTypes(folder, types):
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(types)
    folder.setImmediatelyAddableTypes(types)
