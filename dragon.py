from werkzeug import Request, Response


class Dragon:

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = Response('Hello, World')
        return response(environ, start_response)