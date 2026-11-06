from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="FF52 Independent Test Backend")

players = {}
rooms = {}

@app.get("/")
async def home():
    return {
        "status": "online",
        "project": "FF52 Research Backend"
    }

@app.post("/register/{username}")
async def register(username: str):
    if username in players:
        return {"error": "Username already exists"}

    players[username] = {"username": username}
    return {"success": True, "username": username}

@app.get("/players")
async def get_players():
    return {"players": list(players.values())}

@app.post("/room/{room_id}/join/{username}")
async def join_room(room_id: str, username: str):
    if username not in players:
        return {"error": "Register first"}

    rooms.setdefault(room_id, [])

    if username not in rooms[room_id]:
        rooms[room_id].append(username)

    return {"room": room_id, "players": rooms[room_id]}

@app.get("/room/{room_id}")
async def get_room(room_id: str):
    return {"room": room_id, "players": rooms.get(room_id, [])}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Server received: {message}")
    except WebSocketDisconnect:
        pass
