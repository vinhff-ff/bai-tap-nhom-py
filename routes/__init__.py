from routes.Auth.login_routes import login_routes
from routes.Auth.register_routes import register_routes
ROUTES = {
    "POST": {
        "/login": login_routes,
        "/register": register_routes,
    },
    "GET": {
        
    }
}