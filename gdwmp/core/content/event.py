# -*- coding: UTF-8 -*-

from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, \
                                                 ISchemaModifier
from archetypes.schemaextender.field import ExtensionField
from Products.ATContentTypes.content.event import ATEvent
from Products.Archetypes.public import BooleanField, StringField, \
                                       BooleanWidget, StringWidget

from gdwmp.core import GDWMPMessage as _


class CompleteField(ExtensionField, BooleanField):
    """
    """


class PriceField(ExtensionField, StringField):
    """
    """


class EventExtender(object):
    adapts(ATEvent)
    implements(ISchemaExtender)

    fields = [
        CompleteField(
            name='complete',
            required = False,
            languageIndependent = True,
            default = False,
            widget = BooleanWidget(
                description = _(u'help_complete_event',
                                default=u"Cochez la case si l'événement est complet."),
                label = _(u'complete_event', default=u'Complet'))),
        PriceField(
            name='price',
            required = False,
            languageIndependent = True,
            widget = StringWidget(
                description = _(u'help_price',
                                default=u"Détail du prix de l'événement."),
                label = _(u'price', default=u'Tarifs')))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class EventRemover(object):
    adapts(ATEvent)
    implements(ISchemaModifier)

    HIDDEN_FIELDS = ['contactEmail', 'contactPhone', 'contactName',
                     'attendees', 'eventUrl']

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        for field in self.HIDDEN_FIELDS:
            schema[field].widget.visible = {'edit': 'hidden',
                                            'view': 'hidden'}
