from src.DD_Forge.app import app

def create_app():
    app1 = app
    # Register blueprints, configs, etc.
    return app1

def main():
    app2 = create_app()
    app2.run()