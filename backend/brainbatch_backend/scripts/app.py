import quart
from user_management import user_bp
import tracemalloc


def create_app():
    tracemalloc.start()
    app = quart.Quart(__name__)
    app.register_blueprint(user_bp)
    return app

if __name__ == "__main__":
    create_app()
