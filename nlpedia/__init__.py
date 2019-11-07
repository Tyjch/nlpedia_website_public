# coding=utf-8
from flask import Flask, render_template
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(24)

    @app.route('/')
    def index():
        return render_template(
            'index.html'
        )

    from nlpedia.views import base
    app.register_blueprint(base.bp)

    from nlpedia.views import auth
    app.register_blueprint(auth.bp)

    from nlpedia.views import content
    app.register_blueprint(content.bp)

    from nlpedia.views import search
    app.register_blueprint(search.bp)

    from nlpedia.views import recommend
    app.register_blueprint(recommend.bp)

    # REMEMBER: Register additional blueprints as more view modules are created

    return app

