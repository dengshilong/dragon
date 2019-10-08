from werkzeug import Request, Response
from werkzeug.routing import Map, Rule


class Dragon:

    def __init__(self):
        self.url_map = Map()
        self.view_functions = {}
        self.response_class = Response

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return self.view_functions[endpoint](**values)
        except Exception as e:
            return e

    def make_response(self, rv, environ):
        if isinstance(rv, self.response_class):
            return rv
        if isinstance(rv, str):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        return self.response_class.force_type(rv, environ)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        response = self.make_response(response, environ)
        return response(environ, start_response)

    def add_url_rule(self, rule, endpoint, **options):
        options['endpoint'] = endpoint
        options.setdefault('methods', ('GET',))
        self.url_map.add(Rule(rule, **options))

    def route(self, rule, **options):
        def decorator(f):
            self.add_url_rule(rule, f.__name__, **options)
            self.view_functions[f.__name__] = f
            return f
        return decorator