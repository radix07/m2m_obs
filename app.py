import os,sys
import atexit
import cherrypy
try:
	cherrypy.config.update({'environment':'embedded'})

	#if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
		#cherrypy.engine.start(blocking=False)
		#atexit.register(cherrypy.engine.stop)
		
	PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

	class Root(object): pass

	cherrypy.tree.mount(Root(), '/', config={
			'/': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': PATH+'/sb-admin-v2',
					'tools.staticdir.index': 'index.html',
				},
		})

	cherrypy.engine.start()
	cherrypy.engine.block()
	#application = cherrypy.Application(Root(), script_name='', config=None)
except Exception, e:
	print e