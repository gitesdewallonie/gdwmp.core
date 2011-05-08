# -*- coding: UTF-8 -*-

from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory


GDWMPMessage = MessageFactory("gdwmp")

ModuleSecurityInfo('gdwmp.core.browser.propriofolder').declarePublic('findProprioFolder')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
