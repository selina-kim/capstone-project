from flask import Flask
from routes.dictionary import *
from routes.translate import *
# from routes.fsrs import *                 # TODO uncomment
from dotenv import load_dotenv

load_dotenv()

def create_app():    
    app = Flask(__name__) 
    print("Test")

    app.config['JSON_AS_ASCII'] = False

    app.register_blueprint(define_bp)
    app.register_blueprint(translate_bp)
    # app.register_blueprint(fsrs_bp)       # TODO uncomment

    return app

app = create_app()
