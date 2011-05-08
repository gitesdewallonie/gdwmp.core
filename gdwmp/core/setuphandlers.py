from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.app.component.interfaces import ISite
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from Products.LinguaPlone.I18NBaseObject import AlreadyTranslated
from Products.PloneLDAP.factory import genericPluginCreation
from Products.PloneLDAP.plugins.ldap import PloneLDAPMultiPlugin

LANGUAGES = ['fr', 'nl']


def install(context):
    portal = context.getSite()
    if not 'fr' in portal.objectIds():
        raise Warning("You must first go to .../plone/@@language-setup-folders")
    if not ISite.providedBy(portal):
        enableSite(portal)
    deleteFolder(portal, 'news')
    deleteFolder(portal, 'events')
    deleteFolder(portal, 'Members')
    setupLanguages(portal)
    clearPortlets(portal)
    setupNavigationPortlet(portal)
    setupNavigation(portal)
    setupLinkIntegrityCheck(portal)
    addRoles(portal)
    activatePloneLDAPPlugin(portal)
    addMemberProperty(portal)


def deleteFolder(portal, folderId):
    folder = getattr(portal, folderId, None)
    if folder is not None:
        portal.manage_delObjects(folderId)


def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 0


def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')


def setupLinkIntegrityCheck(portal):
    pp = getToolByName(portal, 'portal_properties')
    siteProps = pp['navtree_properties']
    siteProps.enable_link_integrity_checks = False


def setupNavigation(portal):
    pp = getToolByName(portal, 'portal_properties')
    navProps = pp['navtree_properties']
    if not 'Image' in navProps.metaTypesNotToList:
        navProps.metaTypesNotToList = navProps.metaTypesNotToList + ('Image', )


def setupNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager, ), IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=0,
                                       bottomLevel=1)
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


def changeFolderView(folder, viewname):
    if folder.getLayout() != viewname:
        folder.setLayout(viewname)


def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible', 'private']:
        portal_workflow.doActionFor(obj, 'publish')
    return


def createFolder(parentFolder, folderId, folderTitle):
    if folderId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Folder', folderId, title=folderTitle)
    createdFolder = getattr(parentFolder, folderId)
    publishObject(createdFolder)
    createdFolder.reindexObject()
    # createdFolder.reindexObjectSecurity()
    return createdFolder


def createTranslationForObject(baseObject, lang='nl', newId=None):
    try:
        if newId is not None:
            baseObject.addTranslation(lang, id=newId)
        else:
            baseObject.addTranslation(lang)
    except AlreadyTranslated:
        pass
    translated = baseObject.getTranslation(lang)
    publishObject(translated)
    translated.reindexObject()
    return translated


def addMemberProperty(portal):
    """
    Add the property which is mapped between ldap & plone
    """
    md = getToolByName(portal, 'portal_memberdata')
    if not md.hasProperty('pk'):
        md.manage_addProperty('pk', '', 'string')


def addRoles(portal):
    """
    Add the default roles
    """
    portalrolemgr = portal.acl_users.portal_role_manager
    roleIds = portalrolemgr.listRoleIds()
    if 'Proprietaire' not in roleIds:
        portalrolemgr.addRole('Proprietaire')
    data = list(portal.__ac_roles__)
    for role in ['Proprietaire']:
        if not role in data:
            data.append(role)
    portal.__ac_roles__ = tuple(data)


def activatePloneLDAPPlugin(portal):
    """
    Go in the acl and active our plugin
    """
    acl = portal.acl_users
    if 'ldap' not in acl.objectIds():
        luf=genericPluginCreation(acl, PloneLDAPMultiPlugin, id='ldap',
                title='LDAP Connexion', login_attr='cn', uid_attr='cn',
                users_base="dc=gitesdewallonie,dc=net",
                users_scope=2, roles="Member",
                groups_base="ou=groups,dc=gitesdewallonie,dc=net",
                groups_scope=2, binduid="cn=admin,dc=gitesdewallonie,dc=net",
                bindpwd='phoneph0ne',
                binduid_usage=1, rdn_attr='cn',
                obj_classes='person,organizationalPerson,gites-proprietaire',
                local_groups=0, use_ssl=0, encryption='SHA',
                read_only=0, LDAP_server="clavius.affinitic.be", REQUEST=None)

        luf.manage_addLDAPSchemaItem("registeredAddress", "email",
                                     public_name="email")
        luf.manage_addLDAPSchemaItem("title", "fullname",
                                     public_name="fullname")
        luf.manage_addLDAPSchemaItem("pk", "pk", public_name="pk")

        luf.manage_addGroupMapping("Proprietaire", "Proprietaire")

    interfaces = ['IAuthenticationPlugin',
                  'ICredentialsResetPlugin',
                  'IGroupEnumerationPlugin',
                  'IGroupIntrospection',
                  'IGroupManagement',
                  'IGroupsPlugin',
                  'IPropertiesPlugin',
                  'IRoleEnumerationPlugin',
                  'IRolesPlugin',
                  'IUserAdderPlugin',
                  'IUserEnumerationPlugin',
                  'IUserManagement']
    ldap = getattr(acl, 'ldap')
    ldap.manage_activateInterfaces(interfaces)
    for interface in interfaces:
        interface_object = acl.plugins._getInterfaceFromName(interface)
        acl.plugins.movePluginsUp(interface_object, ['ldap'])
