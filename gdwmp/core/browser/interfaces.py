from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem
from zope.interface import Interface


class IProprioFolder(Interface):
    """Interface for proprio folders
    """


class IGalleryFolder(Interface):
    """Interface for gallery folders
    """


class IEventFolder(Interface):
    """Interface for events folders
    """


class IConfigureProprioFolderMenuItem(IBrowserSubMenuItem):
    """The menu item for setting a proprio folder
    """


class IConfigureProprioFolderMenu(IBrowserMenu):
    """Root menu for setting a proprio folder
    """
