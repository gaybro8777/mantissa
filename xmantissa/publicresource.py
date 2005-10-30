from zope.interface import implements

from nevow import rend, livepage, tags
from xmantissa.webtheme import getAllThemes
from xmantissa.ixmantissa import IPublicPage

def getLoader(n):
    # TODO: implement PublicApplication (?) in webapp.py, so we can make sure
    # that these go in the right order.  Right now we've only got the one
    # though.
    for t in getAllThemes():
        fact = t.getDocFactory(n, None)
        if fact is not None:
            return fact

    raise RuntimeError("No loader for %r anywhere" % (n,))

class PublicPageMixin(object):
    fragment = None
    title = ''
    username = ''

    def render_navigation(self, ctx, data):
        return ""

    def render_search(self, ctx, data):
        return ""

    def render_title(self, ctx, data):
        return ctx.tag[self.title]

    def render_username(self, ctx, data):
        if self.username is not None:
            return ctx.tag.fillSlots('username', self.username)
        return ctx.tag.clear()[tags.a(href='/login')['Sign in']]

    def render_header(self, ctx, data):
        if self.staticContent is None:
            return ctx.tag

        header = self.staticContent.getHeader()
        if header is not None:
            return ctx.tag[header]
        else:
            return ctx.tag

    def render_footer(self, ctx, data):
        if self.staticContent is None:
            return ctx.tag

        header = self.staticContent.getFooter()
        if header is not None:
            return ctx.tag[header]
        else:
            return ctx.tag

    def render_content(self, ctx, data):
        return ctx.tag[self.fragment]

    def render_head(self, ctx, data):
        content = []
        for theme in getAllThemes():
            extra = theme.head()
            if extra is not None:
                content.append(extra)

        return ctx.tag[content]

class PublicPage(PublicPageMixin, rend.Page):
    def __init__(self, original, fragment, staticContent, forUser):
        super(PublicPage, self).__init__(original, docFactory=getLoader("public-shell"))
        self.fragment = fragment
        self.staticContent = staticContent
        self.username = forUser

class PublicLivePage(PublicPageMixin, livepage.LivePage):
    def __init__(self, original, fragment, staticContent, forUser):
        super(PublicLivePage, self).__init__(original, docFactory=getLoader("public-shell"))
        self.fragment = fragment
        self.staticContent = staticContent
        self.username = forUser

    def render_head(self, ctx, data):
        tag = super(PublicLivePage, self).render_head(ctx, data)
        return tag[livepage.glue]

class GenericPublicPage(object):
    implements(IPublicPage)

    def __init__(self, publicPageClass, original, staticContent):
        self.publicPageClass = publicPageClass
        self.original = original
        self.staticContent = staticContent

    def anonymousResource(self):
        raise NotImplementedError("Why are you using this class if all you want is an anonymous resource?")

    def resourceForUser(self, username):
        return self.publicPageClass(self.original, self.staticContent, username)