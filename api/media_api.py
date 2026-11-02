"""Media Submissions API (Luke Sanders, issue #14). No data here; it only calls the model."""
from flask import Blueprint, request
from flask_restful import Api, Resource

from model.media import getMediaPage, submitMedia

media_api = Blueprint('media_api', __name__, url_prefix='/api/media')
api = Api(media_api)


class SubmissionsAPI(Resource):
    # GET /api/media/submissions  -> allowed types + pending list
    def get(self):
        return getMediaPage(), 200

    # POST /api/media/submissions  body: {"title": "...", "media_type": "Photo"}
    # -> 201 "Pending review", or 400 with the reason it was rejected
    def post(self):
        body = request.get_json(silent=True) or {}
        title = str(body.get("title", "")).strip()
        media_type = str(body.get("media_type", "")).strip()
        result = submitMedia(title, media_type)
        return result, (201 if result["accepted"] else 400)


api.add_resource(SubmissionsAPI, '/submissions')
