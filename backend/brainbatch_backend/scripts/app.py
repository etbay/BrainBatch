def create_app():
    import quart
    import tracemalloc

    tracemalloc.start()
    app = quart.Quart(__name__)

    # Set maximum file upload size to 5 MiB
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    from user_management import user_bp
    from group_management import group_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)
    app.run(host="127.0.0.1", port=5000, use_reloader=False)
    return app


if __name__ == "__main__":
    create_app()
