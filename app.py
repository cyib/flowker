from flask import Flask, jsonify
from flask_cors import CORS
from src.api.routes.manager import bp as bp_manager
from src.api.routes.node import bp as bp_node
from src.api.routes.api import bp as bp_api
from src.api.routes.environment import bp as bp_environment

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(bp_environment)
app.register_blueprint(bp_manager)
app.register_blueprint(bp_node)
app.register_blueprint(bp_api)


if __name__ == "__main__":
    app.run()