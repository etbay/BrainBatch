from quart_cors import cors


def create_app():
    import quart
    import tracemalloc

    tracemalloc.start()
    app = quart.Quart(__name__)
    app = cors(app, allow_origin="http://localhost:5173")

    from user_management import user_bp
    from group_management import group_bp
    from file_uploads import uploads_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(uploads_bp)
    app.run(host="0.0.0.0", port=5173)


if __name__ == "__main__":
    create_app()
