class Dragon:

    def __call__(self, environ, start_response):
        response_body = b"Hello, World!"
        status = "200 OK"
        start_response(status, response_headers=[])
        return iter([response_body])