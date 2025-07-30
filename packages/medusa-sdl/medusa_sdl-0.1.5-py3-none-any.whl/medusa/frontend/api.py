from medusa.core.driver_loader import node_definitions
from flask import jsonify, Blueprint

bp = Blueprint("api", __name__)

@bp.route('/node-defs')
def get_node_defs():
    print("node_defs hit")
    return jsonify(node_definitions())
