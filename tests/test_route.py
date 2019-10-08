import dragon


def test_request_dispatching(app, client):
    @app.route('/')
    def index():
        return 'index'

    @app.route('/more', methods=['GET', 'POST'])
    def more():
        return 'more'

    assert client.get('/').data == b'index'
    rv = client.post('/')
    assert rv.status_code == 405
    assert sorted(rv.allow) == ['GET', 'HEAD']
    rv = client.head('/')
    assert rv.status_code == 200
    assert not rv.data  # head truncates
    assert client.post('/more').data == b'more'
    assert client.get('/more').data == b'more'
    rv = client.delete('/more')
    assert rv.status_code == 405
    assert sorted(rv.allow) == ['GET', 'HEAD', 'POST']