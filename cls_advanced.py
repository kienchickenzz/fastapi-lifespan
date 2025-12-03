from fastapi import FastAPI, Request
import asyncio
import uvicorn
from typing import Mapping, Any

class AppDependencies(Mapping):
    def __init__(self, /, **kwargs: Any):
        self.db: str = ""
        self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return self.__dict__.__len__()


class MyInitializer:
    def __init__(self, app: FastAPI):
        self.app = app
        self.deps = AppDependencies()

    async def _setup_db(self):
        # Giả lập khởi tạo database connection
        print("Setting up database...")
        await asyncio.sleep(1)
        return "DatabaseConnection"
    
    async def __aenter__(self):
        # Khởi tạo dependencies
        self.deps.db = await self._setup_db()
        
        # Gán vào app.state
        self.app.state.dependencies = self.deps
        
        # Cũng có thể gán riêng lẻ
        self.app.state.db = self.deps.db
        
        return self.deps
    
    async def _cleanup(self):
        # Giả lập dọn dẹp resources
        print("Cleaning up resources...")
        await asyncio.sleep(1)
        print("Resources cleaned up.")

    async def __aexit__(self, *args):
        await self._cleanup()

app = FastAPI(lifespan=MyInitializer)

@app.get("/")
async def root():
    deps = app.state._state.get("dependencies")
    return {
        "db": deps.db,
        "state": {
            "db": app.state.db,
        }
    }

@app.get("/test")
async def test_request_state(request: Request):
    return {
        "app_state": app.state,
        "app_state_state": app.state._state,
        "request_state": request.state,
        "request_state_state": request.state._state, 
    }

if __name__ == "__main__":
    uvicorn.run( app, host="127.0.0.1", port=8000)
