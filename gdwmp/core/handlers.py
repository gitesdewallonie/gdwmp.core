# -*- coding: UTF-8 -*-

from Acquisition import aq_parent

from gdwmp.core.browser.interfaces import IGalleryFolder, IEventFolder
from gdwmp.core.mailer import Mailer


def photoAddedHandler(obj, event):
    parentFolder = aq_parent(obj)
    if not IGalleryFolder.providedBy(parentFolder):
        return
    copyObjectToTranslatedFolder(parentFolder, obj)


def photoDeletedHandler(obj, event):
    parentFolder = aq_parent(obj)
    if not IGalleryFolder.providedBy(parentFolder):
        return
    removeObjectFromTranslatedFolder(parentFolder, obj)


def eventAddedHandler(obj, event):
    parentFolder = aq_parent(obj)
    if not IEventFolder.providedBy(parentFolder):
        return
    mailToTranslator(obj, 'add')


def eventModifiedHandler(obj, event):
    parentFolder = aq_parent(obj)
    if not IEventFolder.providedBy(parentFolder):
        return
    mailToTranslator(obj, 'modify')


def copyObjectToTranslatedFolder(folder, obj):
    destFolder = folder.getTranslation('nl')
    if destFolder.hasObject(obj.id):
        destFolder.manage_delObjects(obj.id)

    copiedObject = folder.manage_copyObjects(obj.id)
    copyInfos = destFolder.manage_pasteObjects(copiedObject)
    pastedObject = getattr(destFolder, copyInfos[0]['new_id'])
    pastedObject.setLanguage('nl')
    pastedObject.addTranslationReference(obj.getCanonical())
    pastedObject.reindexObject()


def removeObjectFromTranslatedFolder(folder, obj):
    translatedFolder = folder.getTranslation('nl')
    translatedObject = obj.getTranslation('nl')

    if translatedObject is not None and \
       translatedObject.id in translatedFolder.objectIds():
        translatedObject.removeTranslationReference(obj.getCanonical())
        translatedFolder.manage_delObjects(translatedObject.id)
        translatedFolder.reindexObject()


def mailToTranslator(obj, eventType):
    fromMail = "info@gitesdewallonie.be"
    mailer = Mailer("localhost", fromMail)
    if eventType == 'add':
        mailer.setSubject("[MARMITON ET POLOCHON - Ajout d'un événement]")
    else:
        mailer.setSubject("[MARMITON ET POLOCHON - Modification d'un événement]")
    mailer.setRecipients("info@gitesdewallonie.be")
    if eventType == 'add':
        mail = u""":: MARMITON ET POLOCHON - Ajout d'un événement ::

    Un événement vient d'être créé et devrait être traduit :

        * Lien : %s
    """ \
           % obj.absolute_url()
    else:
        mail = u""":: MARMITON ET POLOCHON - Modification d'un événement ::

    Un événement vient d'être modifié et devrait être (re)traduit :

        * Lien : %s
    """ \
           % obj.absolute_url()
    mailer.sendAllMail(mail.encode('utf-8'), plaintext=True)
