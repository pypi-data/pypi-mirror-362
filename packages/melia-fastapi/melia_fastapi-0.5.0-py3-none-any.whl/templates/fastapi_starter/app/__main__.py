import uvicorn as uvicorn

from app.api.deps import get_settings
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host=get_settings().api.host, port=get_settings().api.port)
