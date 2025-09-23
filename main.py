from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import WebSocket

class CmdData(BaseModel):
    vx: float
    wz: float

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "file://",
    "null",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def read_health():
    return {"status": "OK"}

@app.post("/cmd")
def receive_cmd(data: CmdData):
    print(f"Received command: vx={data.vx}, wz={data.wz}")
    return {"message": "Command received successfully"}

@app.websocket("/ws/cmd")
async def websocket_cmd_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received WS command: vx={data['vx']}, wz={data['wz']}")
            await websocket.send_json({"status": "received"})
    except Exception as e:
        print(f"WebSocket closed: {e}")
    finally:
        await websocket.close()