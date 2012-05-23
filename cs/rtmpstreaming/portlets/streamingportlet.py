from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from cs.rtmpstreaming import rtmpstreamingMessageFactory as _

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")

class IStreamingPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    protocol = schema.TextLine(title=_(u"Protocol"),
                             description=_(u"Write the protocol of the server. Usualy RTMP"),
                             default=u'rtmp',
                             required=True)


    server = schema.TextLine(title=_(u"RTMP server address"),
                             description=_(u"Write the address of the RTMP server"),
                             required=True)

    streaming_file = schema.TextLine(title=_(u"Streaming file"),
                                     description=_(u"Usualy the last part of the URL"),
                                     required=True)

    image_url = schema.TextLine(title=_(u'Image URL'),
                                description=_(u'Enter the URL of the splash image'),
                                required=False)

    width = schema.Int(title=_(u'Width'),
                       default=480,
                       required=True,
                       )

    height = schema.Int(title=_(u'Height'),
                       default=270,
                       required=True,
                       )

    extra_text = schema.TextLine(title=_(u'Extra text'),
                                 description=_(u'Extra text to show after the video'),
                                 default=u'',
                                 required=False)

    extra_link = schema.TextLine(title=_(u'Extra info link'),
                                 description=_(u'URL of the extra information site'),
                                 default=u'',
                                 required=False)



class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IStreamingPortlet)    

    def __init__(self, server=u'',
                       protocol=u'',
                       streaming_file=u'',
                       image_url=u'',
                       width=480,
                       height=270, 
                       extra_text=u'',
                       extra_link=u''):
        self.server = server
        self.protocol = protocol
        self.streaming_file = streaming_file
        self.image_url = image_url
        self.width = width
        self.height = height
        self.extra_text = extra_text
        self.extra_link = extra_link


    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Streaming Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('streamingportlet.pt')


    def script_code(self):
        """ It's hard to get correct JavaScript without errors in ZPT
            so the JS code will be generated here
        """
        TEMPLATE = '''
      jwplayer('mediaplayer').setup({
        'id': 'playerID',
        'width': '%(width)s',
        'height': '%(height)s',
        'provider': '%(protocol)s',
        'streamer': '%(server)s',
        'file': '%(file)s',
        'image': '%(image_url)s',
        'modes': [
            {type: 'flash', src: '/++resource++streaming/player.swf'}
        ]
      });
    '''
        return TEMPLATE % {'width': self.data.width,
                           'height': self.data.height,
                           'protocol': self.data.protocol,
                           'server': self.data.server,
                           'file': self.data.streaming_file,
                           'image_url': self.data.image_url }


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IStreamingPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IStreamingPortlet)
