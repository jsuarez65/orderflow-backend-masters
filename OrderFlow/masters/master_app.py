from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configuration.LogConfiguration import LogConfiguration
from controllers.PermissionController import PermissionRouter
from controllers.RolController import RolRouter
from controllers.UsersController import UsersRouter

app = FastAPI(
    title="OrderFlow API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(PermissionRouter)
app.include_router(RolRouter)
app.include_router(UsersRouter)

LogConfiguration.configure()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

