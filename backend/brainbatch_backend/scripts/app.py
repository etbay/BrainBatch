def create_app():
    import quart
    import tracemalloc

    tracemalloc.start()
    app = quart.Quart(__name__)

    from user_management import user_bp
    from group_management import group_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)
    return app


if __name__ == "__main__":
    create_app()
