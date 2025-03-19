import uvicorn
from fastapi import FastAPI
from src.api.endpoints import router
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)