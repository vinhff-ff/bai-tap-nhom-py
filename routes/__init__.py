from routes.Auth.login_routes import login_routes
from routes.Auth.register_routes import register_routes
from routes.Task.task_routes import (
    filter_tasks_by_status_routes,
    get_overdue_tasks_routes,
)

ROUTES = {
    "POST": {
        "/login": login_routes,
        "/register": register_routes,
    },
    "GET": {
        "/tasks/overdue": get_overdue_tasks_routes,
        "/tasks/filter": filter_tasks_by_status_routes,
    }
}