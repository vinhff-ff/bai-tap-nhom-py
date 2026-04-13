from routes.Auth.login_routes import login_routes

ROUTES = {
    "POST": {
        "/login": login_routes,
    },
    "GET": {
        # thêm route GET ở đây
    }
}