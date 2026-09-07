from fastapi import FastAPI
from app.api.routes import router
from app.api.auth import router_auth
from app.api.users import router_user


app = FastAPI(
    title="Auth Service",
    version="0.1.0"
)

app.include_router(router)
app.include_router(router_auth)
app.include_router(router_user)
