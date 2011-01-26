# -*- coding: UTF-8 -*-

from AccessControl import getSecurityManager

from zope.interface import alsoProvides

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.plonetruegallery.interfaces import ISlideShowDisplaySettings
from collective.plonetruegallery.settings import GallerySettings

from gdwmp.core.browser.interfaces import IProprioFolder, IGalleryFolder, \
                                          IEventFolder
from gdwmp.core.setuphandlers import createFolder, changeFolderView, \
                                     createTranslationForObject, publishObject


class ProprioFolder(BrowserView):

    def isConfigured(self):
        obj = self.context
        return IProprioFolder.providedBy(obj)

    def changeStatus(self):
        obj = self.context
        putils = getToolByName(self, 'plone_utils')

        if not self.isConfigured():
            alsoProvides(obj, IProprioFolder)
            self.createContent()
            putils.addPortalMessage(u"Configuration du dossier proprio réussie. \
                                      N'oubliez pas de configurer le partage \
                                      du dossier 'Evénements' au propriétaire ...")
            self.request.response.redirect(obj.absolute_url())
            return ''

    def createContent(self):
        obj = self.context
        obj.setLanguage('fr')
        translatedProprioFolder = createTranslationForObject(obj)
        translatedProprioFolder.setTitle(obj.Title())

        # Dossier 'Recettes'
        recettesFolder = createFolder(obj, 'recettes', 'Recettes')
        recettesFolder.setLanguage('fr')
        translatedFolder = createTranslationForObject(recettesFolder, \
                                                      newId='recepten')
        translatedFolder.setTitle('Recepten')
        restrictFolderTypes(recettesFolder, ['Recette', 'File', 'Image'])
        restrictFolderTypes(translatedFolder, ['Recette', 'File', 'Image'])
        # changeFolderView(recettesFolder, 'folder_full_view')
        # changeFolderView(translatedFolder, 'folder_full_view')
        recettesFolder.reindexObject()
        translatedFolder.reindexObject()

        # Dossier 'Photos'
        galleryFolder = createFolder(obj, 'photos', 'Photos')
        galleryFolder.setLanguage('fr')
        translatedFolder = createTranslationForObject(galleryFolder, \
                                                      newId='fotos')
        translatedFolder.setTitle("Foto's")
        changeFolderView(galleryFolder, 'galleryview')
        changeFolderView(translatedFolder, 'galleryview')
        restrictFolderTypes(galleryFolder, ['Image'])
        restrictFolderTypes(translatedFolder, ['Image'])
        alsoProvides(galleryFolder, IGalleryFolder)
        alsoProvides(translatedFolder, IGalleryFolder)
        configureSlideshow(galleryFolder)
        configureSlideshow(translatedFolder)
        galleryFolder.reindexObject()
        translatedFolder.reindexObject()

        # Dossier 'Evénements'
        eventsFolder = createFolder(obj, 'evenements', 'Evénements')
        eventsFolder.setLanguage('fr')
        translatedFolder = createTranslationForObject(eventsFolder, \
                                                      newId='evenementen')
        translatedFolder.setTitle('Evenementen')
        restrictFolderTypes(eventsFolder, ['Event'])
        restrictFolderTypes(translatedFolder, ['Event'])
        changeFolderView(eventsFolder, 'event_folder_view')
        changeFolderView(translatedFolder, 'event_folder_view')
        alsoProvides(eventsFolder, IEventFolder)
        alsoProvides(translatedFolder, IEventFolder)
        eventsFolder.reindexObject()
        translatedFolder.reindexObject()

        # Page 'Descriptif' de l'hébergement
        obj.invokeFactory('Hebergement', 'descriptif', title='Descriptif')
        descriptif = getattr(obj, 'descriptif')
        descriptif.setLanguage('fr')
        translatedPage = createTranslationForObject(descriptif, \
                                                    newId='beschrijving')
        translatedPage.setTitle('Beschrijving')
        descriptif.setExcludeFromNav(True)
        translatedPage.setExcludeFromNav(True)
        publishObject(descriptif)
        publishObject(translatedPage)
        descriptif.reindexObject()
        translatedPage.reindexObject()

        obj.setDefaultPage('descriptif')
        translatedProprioFolder.setDefaultPage('beschrijving')
        obj.reindexObject()
        translatedProprioFolder.reindexObject()


def restrictFolderTypes(folder, types):
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(types)
    folder.setImmediatelyAddableTypes(types)


def configureSlideshow(context):
    settings = GallerySettings(context, interfaces=[ISlideShowDisplaySettings])
    settings.show_slideshow_infopane = False


def findProprioFolder(context):
    loggedUser = getSecurityManager().getUser()
    roles = list(loggedUser.getRoles())
    if not 'Proprietaire' in roles:
        return None

    login = loggedUser.getId()
    acl_users = getToolByName(context, 'acl_users')
    catalog = getToolByName(context, 'portal_catalog')
    proprioFolders = catalog.searchResults(path={'query': '/', 'depth': 2},
                                           portal_type='ProprioFolder')

    for folderBrain in proprioFolders:
        folder = folderBrain.getObject()
        eventFolder = getattr(folder, 'evenements')
        if not eventFolder:
            continue
        # See if logged user is in folder sharings
        local_roles = acl_users._getAllLocalRoles(eventFolder)
        if login in local_roles:
            putils = getToolByName(context, 'plone_utils')
            putils.addPortalMessage(u"Vous avez été redirigé vers le dossier \
                                      d'événements de votre gîte.")
            return eventFolder.absolute_url()
    return None
