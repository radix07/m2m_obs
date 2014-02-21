import os,sys
import atexit
import cherrypy
from cherrypy.process import servers

try:
	def fake_wait_for_occupied_port(host, port): return
	servers.wait_for_occupied_port = fake_wait_for_occupied_port

	cherrypy.config.update({'environment':'embedded'})
	port = int(os.environ.get("PORT", 5000))
	print port
	#if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
		#cherrypy.engine.start(blocking=False)
		#atexit.register(cherrypy.engine.stop)
		
	PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

	class Root(object): pass
	cherrypy.config.update({'server.socket_port': port,})
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
