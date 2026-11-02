"""Support Simulation API (issue #9), v2. No data here; it only calls the model."""
from flask import Blueprint, request
from flask_restful import Api, Resource

from model.simulation import getSimulation, routeSubmission

simulation_api = Blueprint('simulation_api', __name__, url_prefix='/api/simulation')
api = Api(simulation_api)


class ScenariosAPI(Resource):
    # GET /api/simulation/scenarios  -> questions (no needs/points) + hotline
    def get(self):
        return getSimulation(), 200


class ResultAPI(Resource):
    # POST /api/simulation/result   body: {"choice_ids": [1, 5, 9, ...]}
    # -> the top need, where to go next, and the hotline
    def post(self):
        body = request.get_json(silent=True) or {}
        choice_ids = body.get("choice_ids")
        if not isinstance(choice_ids, list) or not choice_ids:
            return {"message": "choice_ids must be a non-empty list"}, 400
        result = routeSubmission(choice_ids)
        if result is None:
            return {"message": "none of those choice_ids exist"}, 400
        return result, 200


api.add_resource(ScenariosAPI, '/scenarios')
api.add_resource(ResultAPI, '/result')
