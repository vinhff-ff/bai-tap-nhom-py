from routes.Auth.login_routes import login_routes
from routes.Auth.register_routes import register_routes
from routes.Schedule.schedule_routes import (
    create_schedule_route,
    delete_schedule_route,
    list_schedules_route,
    update_schedule_route,
    list_schedules_by_status_route,
    overdue_schedules_route,
)

ROUTES = {
    "POST": {
        "/login": login_routes,
        "/register": register_routes,
        "/schedule/create": create_schedule_route,
        "/schedule/list": list_schedules_route,
        "/schedule/update": update_schedule_route,
        "/schedule/delete": delete_schedule_route,
        "/schedule/list-by-status": list_schedules_by_status_route,
        "/schedule/overdue": overdue_schedules_route,
    },
    "GET": {},
}