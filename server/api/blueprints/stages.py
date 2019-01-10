import flask
from flask import Blueprint
from flask_login import current_user, login_required, logout_user
from datetime import datetime

from server.api.utils import jsonify_response, paginate
from server.error_handling import RouteError
from server.api.database.models import Stage, Topic


stages_routes = Blueprint("stages", __name__, url_prefix="/stages")


def init_app(app):
    app.register_blueprint(stages_routes)


@stages_routes.route("/", methods=["GET"])
@jsonify_response
@login_required
@paginate
def stages():
    page = flask.request.args.get("page", 1, type=int)

    pagination = Stage.query.order_by(Stage.order).paginate(page, 10, False)
    return pagination


@stages_routes.route("/topic", methods=["POST"])
@jsonify_response
@login_required
def new_topic():
    if not current_user.is_admin:
        raise RouteError("Admin required.")

    data = flask.request.get_json()
    stage = Stage.get_by_id(data.get("stage_id"))
    if not stage:
        raise RouteError("Stage does not exist.")
    topic = Topic.create(
        title=data.get("title"), stage_id=stage.id, order=data.get("order")
    )
    return {"message": "Topic created successfully.", "data": topic.to_dict()}, 201


@stages_routes.route("/", methods=["POST"])
@jsonify_response
@login_required
def new_stage():
    if not current_user.is_admin:
        raise RouteError("Admin required.")
    data = flask.request.get_json()
    stage = Stage.create(title=data.get("title"), order=data.get("order"))
    return {"message": "Stage created successfully.", "data": stage.to_dict()}, 201