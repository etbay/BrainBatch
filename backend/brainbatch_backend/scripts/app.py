def create_app():
    import quart
    import tracemalloc

    tracemalloc.start()
    app = quart.Quart(__name__)

    from user_management import user_bp
    from group_management import group_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)
<<<<<<< Updated upstream:backend/brainbatch_backend/scripts/app.py
=======
    app.run(host="127.0.0.1", port=5000, use_reloader=False)
>>>>>>> Stashed changes:backend/scripts/app_main.py
    return app


if __name__ == "__main__":
    create_app()
