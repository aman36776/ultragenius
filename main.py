from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers import users, tasks
from database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Include routes
app.include_router(users.router)
app.include_router(tasks.router)

# ✅ Custom Swagger UI with Bearer Token Auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Quantal API",
        version="1.0.0",
        description="A simple task management system with JWT auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
