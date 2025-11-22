# from flask import Blueprint, request, jsonify
# from blueprintapp.app import db
# from blueprintapp.blueprints.api.models import Todo
# from blueprintapp.blueprints.api.db_operations import (
#     db_read_all_todos,
#     db_read_todo_by_tid,
#     db_delete_todo,
#     db_create_new_todo_obj,
#     db_update_todo,
# )
# from blueprintapp.blueprints.api.utilities import (
#     valid_title_and_duedate,
#     jsend_success,
#     jsend_fail,
# )


# api = Blueprint("api", __name__, template_folder="templates")


# # Get all todos
# @api.route("/todos", methods=["GET"])
# def get_todos():
#     todos = db_read_all_todos()

#     todos_list = [
#         {
#             "tid": todo.tid,
#             "title": todo.title,
#             "description": todo.description,
#             "duedate": todo.duedate.isoformat(),
#             "done": todo.done,
#         }
#         for todo in todos
#     ]
#     return jsend_success(data_key="todos", data_value=todos_list)


# # Get a specific todo by id
# @api.route("/todos/<int:tid>", methods=["GET"])
# def get_todo(tid):
#     todo = db_read_todo_by_tid(tid=tid)

#     if todo == None:
#         return jsend_fail(
#             data_key="todo", data_value="Todo does not exist", status_code=404
#         )

#     todo_data = {
#         "tid": todo.tid,
#         "title": todo.title,
#         "description": todo.description,
#         "duedate": todo.duedate.isoformat(),
#         "done": todo.done,
#     }
#     return jsend_success(data_key="todo", data_value=todo_data)


# # Create new todo
# @api.route("/todos", methods=["POST"])
# def create_todo():
#     data = request.get_json()
#     response = valid_title_and_duedate(data=data)
#     if type(response) is not dict:
#         return response

#     # Create the new todo object
#     new_todo = Todo(
#         title=response.get("title"),
#         description=data.get("description"),
#         duedate=response.get("duedate"),
#         done=data.get("done", False),
#     )
#     # TODO dependency injection?
#     db_create_new_todo_obj(todo=new_todo, db_session=db.session)
#     # TODO success follow delete patern? Maybe returning newly created todo object in the response?
#     return jsend_success(status_code=201)


# # Update an existing todo
# @api.route("/todos/<int:tid>", methods=["PUT"])
# def update_todo(tid):
#     # todo = db_read_todo_by_tid_or_404(tid=tid)
#     todo = db_read_todo_by_tid(tid=tid)

#     if todo == None:
#         return jsend_fail(
#             data_key="todo", data_value="Todo does not exist", status_code=404
#         )

#     data = request.get_json()
#     response = valid_title_and_duedate(data=data)
#     if type(response) is not dict:
#         return response

#     db_update_todo(
#         todo=todo,
#         title=response.get("title"),
#         description=data.get("description"),
#         duedate=response.get("duedate"),
#         done=data.get("done"),
#     )
#     # TODO should update follow delete patern?
#     return jsend_success()


# # Delete an existing todo
# @api.route("/todos/<int:tid>", methods=["DELETE"])
# def delete_todo(tid):
#     todo = db_read_todo_by_tid(tid=tid)

#     if todo == None:
#         return jsend_fail(
#             data_key="todo", data_value="Todo does not exist", status_code=404
#         )

#     db_delete_todo(todo=todo)
#     return jsend_success()

from flask import Blueprint, request
from blueprintapp.blueprints.api.db_operations import (
    db_get_all_alerts,
    db_create_alert,
    db_get_alert_by_id,
    db_delete_alert,
    db_update_alert,
)
from blueprintapp.blueprints.api.utilities import validate_alert
from blueprintapp.blueprints.api.utilities import jsend_success, jsend_fail

alerts = Blueprint("alerts", __name__)


@alerts.route("/alerts", methods=["GET"])
def list_alerts():
    active = request.args.get("active", "false").lower() == "true"
    alerts_list = db_get_all_alerts(active_only=active)
    # Serialize output
    result = []
    for a in alerts_list:
        result.append(
            {
                "id": a.id,
                "email": a.email,
                "threshold": a.threshold,
                "active": a.active,
                "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
        )
    return jsend_success(data_key="alerts", data_value=result)


@alerts.route("/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()
    result = validate_alert(data)
    if not isinstance(result, dict):
        return result
    alert = db_create_alert(result["email"], result["threshold"])
    # Return created resource
    alert_data = {
        "id": alert.id,
        "email": alert.email,
        "threshold": alert.threshold,
        "active": alert.active,
        "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
    return jsend_success("alert", alert_data, status_code=201)


@alerts.route("/alerts/<int:alert_id>", methods=["GET"])
def get_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail(
            data_key="alert", data_value="Alert does not exist", status_code=404
        )

    alert_data = {
        "id": a.id,
        "email": a.email,
        "threshold": a.threshold,
        "active": a.active,
        "triggered_at": a.triggered_at.isoformat() if a.triggered_at else None,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }
    return jsend_success(data_key="alert", data_value=alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["PUT", "PATCH"])
def update_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail("alert", "Alert does not exist", status_code=404)

    data = request.get_json() or {}
    email = data.get("email")
    threshold = data.get("threshold")
    active = data.get("active")

    # basic validation
    if threshold is not None:
        try:
            threshold = float(threshold)
        except (ValueError, TypeError):
            return jsend_fail("threshold", "threshold must be a number")

    if email is not None and not str(email).strip():
        return jsend_fail("email", "email must be a non-empty string")

    updated = db_update_alert(a, email=email, threshold=threshold, active=active)

    alert_data = {
        "id": updated.id,
        "email": updated.email,
        "threshold": updated.threshold,
        "active": updated.active,
        "triggered_at": (
            updated.triggered_at.isoformat() if updated.triggered_at else None
        ),
        "created_at": updated.created_at.isoformat() if updated.created_at else None,
    }
    return jsend_success("alert", alert_data)


@alerts.route("/alerts/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id: int):
    a = db_get_alert_by_id(alert_id)
    if a is None:
        return jsend_fail("alert", "Alert does not exist", status_code=404)

    db_delete_alert(a)
    return jsend_success()
