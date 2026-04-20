from routes.Auth.login_routes import login_routes
from routes.Auth.register_routes import register_routes
from routes.Task.task_routes import (
    create_task_route,
    delete_task_route,
    list_tasks_route,
    list_tasks_by_status_route,
    overdue_tasks_route,
    update_task_route,
)

ROUTES = {
    "POST": {
        "/login": login_routes,
        "/register": register_routes,

        '''======================================================'''

        "/schedule/create": create_task_route,
        "/schedule/list": list_tasks_route,
        "/schedule/update": update_task_route,
        "/schedule/delete": delete_task_route,

        '''========================================================'''
        
        "/schedule/list-by-status": list_tasks_by_status_route,
        "/schedule/overdue": overdue_tasks_route,
        
    },
    "GET": {},
}