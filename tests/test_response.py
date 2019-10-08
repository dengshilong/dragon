def test_response_creation(app, client):

    @app.route('/unicode')
    def from_unicode():
        return u'Hällo Wörld'

    @app.route('/args')
    def from_tuple():
        return 'Meh', 400, {'X-Foo': 'Testing'}, 'text/plain'

    c = app.test_client()
    assert c.get('/unicode').data == u'Hällo Wörld'.encode('utf-8')
    rv = c.get('/args')
    assert rv.data == b'Meh'
    assert rv.headers['X-Foo'] == 'Testing'
    assert rv.status_code == 400
    assert rv.mimetype == 'text/plain'