from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configuration.LogConfiguration import LogConfiguration
from controllers.ProductController import ProductRouter

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

app.include_router(ProductRouter)

LogConfiguration.configure()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")