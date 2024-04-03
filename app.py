from flask import Flask, jsonify
from flask_cors import CORS
from src.api.routes.manager import bp as bp_manager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(bp_manager)


if __name__ == "__main__":
    app.run()