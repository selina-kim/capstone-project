from flask import Flask
from src.routes import define_bp

def create_app():    
    app = Flask(__name__) 
    print("Test")

    app.register_blueprint(define_bp)
    return app

app = create_app()
