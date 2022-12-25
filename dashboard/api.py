import os

import uvicorn

from src.api.app import app

if __name__ == "__main__":
    is_debug = os.getenv("DEBUG", "0") == "1"
    uvicorn.run(app, host="localhost" if is_debug else "0.0.0.0", port=os.getenv("PORT", 8000))
