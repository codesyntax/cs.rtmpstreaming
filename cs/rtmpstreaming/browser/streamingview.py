from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class IStreamingView(Interface):
    """
    Streaming view interface
    """

    def script_code():
        """ return the javascript for the Streaming code"""


class StreamingView(BrowserView):
    """
    Streaming browser view
    """
    implements(IStreamingView)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

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
        return TEMPLATE % {'width': self.portal.getProperty('streaming_width'),
                           'height': self.portal.getProperty('streaming_height'),
                           'protocol': self.portal.getProperty('streaming_protocol'),
                           'server': self.portal.getProperty('streaming_server'),
                           'file': self.portal.getProperty('streaming_file'),
                           'image_url': self.portal.getProperty('streaming_image_url')
                           }