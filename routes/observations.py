from flask import Blueprint
from controllers.observation import search_observations, add_observation, delete_observation, update_observation

observations_bp = Blueprint("observations", __name__)

# JSON endpoints
observations_bp.route("/observations/search", methods=["GET"])(search_observations)
observations_bp.route("/observations", methods=["POST"])(add_observation)
observations_bp.route("/observations/<int:observation_id>", methods=["PUT"])(update_observation)
observations_bp.route("/observations/<int:observation_id>", methods=["DELETE"])(delete_observation)