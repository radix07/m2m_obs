import os
import cherrypy

PATH = os.path.abspath(os.path.dirname(__file__))
class Root(object): pass

cherrypy.tree.mount(Root(), '/', config={
        '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH+'\sb-admin-v2',
                'tools.staticdir.index': 'index.html',
            },
    })

cherrypy.engine.start()
cherrypy.engine.block()