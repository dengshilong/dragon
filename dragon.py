import os
import sys

from jinja2 import Environment, select_autoescape, PackageLoader
from werkzeug import Request, Response as ResponseBase
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule


class Response(ResponseBase):
    default_mimetype = "text/html"


def _get_package_path(name):
    """Returns the path to a package or cwd if that cannot be found."""
    try:
        return os.path.abspath(os.path.dirname(sys.modules[name].__file__))
    except (KeyError, AttributeError):
        return os.getcwd()


class Dragon:
    static_path = '/static'
    response_class = Response
    root_path = None

    def __init__(self, package_name):
        self.package_name = package_name
        self.url_map = Map()
        self.view_functions = {}
        self.jinja_options = {
            'autoescape': select_autoescape(['html', 'xml'])
        }
        self.jinja_env = Environment(loader=self.create_jinja_loader(),
                                     **self.jinja_options)

        self.root_path = _get_package_path(package_name)
        if self.static_path is not None:
            self.url_map.add(Rule(self.static_path + '/<filename>',
                                  build_only=True, endpoint='static'))
            target = os.path.join(self.root_path, 'static')
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                self.static_path: target
            })

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

    def create_jinja_loader(self):
        return PackageLoader(self.package_name)

    def render_template(self, template_name, **context):
        return self.jinja_env.get_template(template_name).render(context)

    def test_client(self):
        """Creates a test client for this application.  For information
        about unit testing head over to :ref:`testing`.
        """
        from werkzeug import Client
        return Client(self, self.response_class, use_cookies=True)
