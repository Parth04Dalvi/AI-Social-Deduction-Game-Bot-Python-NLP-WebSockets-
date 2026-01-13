import os, json, random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

class GameEngine:
    def __init__(self):
        self.players = {} # {client_id: {"role": "crew", "votes": 0}}
        self.phase = "DISCUSSION" # DISCUSSION or VOTING
        self.imposter_id = None

    def start_game(self, player_ids: List[str]):
        self.imposter_id = random.choice(player_ids)
        for pid in player_ids:
            self.players[pid] = {"role": "imposter" if pid == self.imposter_id else "crew", "votes": 0}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

game = GameEngine()
manager = ConnectionManager()

async def get_strategic_ai_response(history: str, role: str):
    # Strategic prompt engineering to prevent "robotic" agreement
    prompt = f"""
    Context: Social Deduction Game. You are '{role}'. 
    Goal: If imposter, deflect; if crewmate, find the liar. 
    Chat History: {history}
    Respond as 'Player_AI' in one short, slightly casual sentence:
    """
    response = model.generate_content(prompt)
    return response.text

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    
    # Initialize game if this is the 4th player
    if len(manager.active_connections) == 4:
        game.start_game(list(manager.active_connections.keys()))
        await manager.broadcast({"type": "SYSTEM", "content": "Game Started! Check your secret roles."})

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)

            if data["type"] == "CHAT":
                await manager.broadcast({"type": "MESSAGE", "user": client_id, "content": data["content"]})
                
                # AI simulates a "thinking" delay for realism
                if "sus" in data["content"] or "imposter" in data["content"]:
                    ai_role = game.players.get("Player_AI", {"role": "crew"})["role"]
                    reply = await get_strategic_ai_response(data["content"], ai_role)
                    await manager.broadcast({"type": "MESSAGE", "user": "Player_AI", "content": reply})

            elif data["type"] == "VOTE":
                target = data["target"]
                game.players[target]["votes"] += 1
                await manager.broadcast({"type": "SYSTEM", "content": f"A vote was cast against {target}!"})

    except WebSocketDisconnect:
        manager.disconnect(client_id)
