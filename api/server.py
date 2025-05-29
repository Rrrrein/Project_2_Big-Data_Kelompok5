from app import app
import cherrypy

if __name__ == "__main__":
    cherrypy.tree.graft(app, '/')
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 9999,
        'engine.autoreload.on': False
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
