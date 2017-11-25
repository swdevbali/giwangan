from flask import Flask, render_template
from flask_admin import Admin

from web_app.models import db, Page, Menu
from web_app.views import PageModelView, MenuModelView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    admin = Admin(app, name=app.config['TITLE'], template_mode='bootstrap3')
    admin.add_view(PageModelView(Page, db.session))
    admin.add_view(MenuModelView(Menu, db.session))

    @app.route('/')
    def index():
        page = Page.query.filter_by(title='homepage').first()
        content = 'empty'
        if page is not None:
            content = page.content
        return render_template('index.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'], CONTENT=content)

    @app.route('/about')
    def about():
        return render_template('about.html', TITLE=app.config['TITLE'],
                               TAGLINE=app.config['TAGLINE'])

    @app.route('/testdb')
    def testdb():
        import psycopg2
        con = psycopg2.connect('dbname=web_app user=devuser password=devpassword host=postgres')
        cur = con.cursor()
        cur.execute("SELECT * FROM page;")

        if cur.rowcount > 0:
            id, title = cur.fetchone()
        else:
            return 'empty'

        con.close()
        return title

    @app.route('/testdbsqlalchemy')
    def testdbsqlalchemy():
        page = Page.query.filter_by(id=2).first()
        if page is not None:
            return page.title
        else:
            return 'empty'

    return app