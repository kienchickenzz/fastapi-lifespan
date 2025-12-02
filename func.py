from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn


@asynccontextmanager
async def my_lifespan_func(app: FastAPI):
    # Startup logic
    print("Starting up...")
    app.state.counter = 200
    app.state.message = "Hello, FastAPI with Lifespan!"
    
    yield # Ứng dụng chạy ở đây
    
    # Shutdown logic
    print("Shutting down...")

app = FastAPI(lifespan=my_lifespan_func)

@app.get("/")
async def root():
    return {
        "message": app.state.message,
        "counter": app.state.counter
    }

if __name__ == "__main__":
    uvicorn.run( app, host="127.0.0.1", port=8000 )
