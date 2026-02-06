from fastapi import FastAPI, WebSocket
import asyncio
from .physics_engine import PhysicsEngine
from .field_state import FieldState

app = FastAPI()

physics = PhysicsEngine()
state = FieldState(physics)

@app.get("/api/field/state")
def get_field_state():
    return state.snapshot()

@app.websocket("/ws/field")
async def field_ws(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_json(state.snapshot())
        await asyncio.sleep(0.1)
