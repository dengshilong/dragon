from dragon import Dragon

app = Dragon(__name__)


@app.route('/user/<username>')
def show_user(username):
    return f'hello {username}'


@app.route('/book/<bookname>')
def show_book(bookname):
    return app.render_template('book.html', **{'bookname': bookname})


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)