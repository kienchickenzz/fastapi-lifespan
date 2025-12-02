from fastapi import FastAPI
import uvicorn


class MyLifespan:
    def __init__(self, app: FastAPI):
        self.app = app
        self.counter = 0
    
    async def __aenter__(self):
        # Startup logic
        print("Starting up...")

        # Initialize state
        self.counter = 100
        self.app.state.counter = self.counter
        self.app.state.message = "Hello, FastAPI with Lifespan Class!"
    
        return {"message": "Started", "counter": self.counter}
    
    async def __aexit__(self, *args):
        # Shutdown logic
        print("Shutting down...")

app = FastAPI(lifespan=MyLifespan)

@app.get("/")
async def root():
    return {
        "message": app.state.message,
        "counter": app.state.counter
    }

if __name__ == "__main__":
    uvicorn.run( app, host="127.0.0.1", port=8000 )
