import os, json, random, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

class GameManager:
    def __init__(self):
        self.players = {} # {client_id: {"role": "crew", "votes": 0}}
        self.imposter_id = None
        self.game_active = False

    def start_game(self, player_ids: List[str]):
        self.imposter_id = random.choice(player_ids)
        for pid in player_ids:
            self.players[pid] = {"role": "imposter" if pid == self.imposter_id else "crew", "votes": 0}
        self.game_active = True

manager = GameManager()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

conn_manager = ConnectionManager()

async def get_agentic_response(history: str, role: str, personality: str):
    # Persona-driven prompt engineering
    prompt = f"""
    You are a player in a social deduction game. Role: {role}. Personality: {personality}.
    Chat History: {history}
    Goal: Blend in. If you are the imposter, shift blame subtly. 
    Respond as 'Player_AI' in one short, slightly casual sentence.
    """
    response = model.generate_content(prompt)
    return response.text

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await conn_manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json() # Use JSON for structured commands
            
            if data["type"] == "MESSAGE":
                await conn_manager.broadcast({"type": "CHAT", "user": client_id, "text": data["text"]})
                
                # Logic: Trigger AI reasoning if suspect keywords appear
                if any(word in data["text"].lower() for word in ["ai", "sus", "imposter"]):
                    await asyncio.sleep(2) # Simulated thinking delay
                    ai_role = manager.players.get("Player_AI", {"role": "crew"})["role"]
                    reply = await get_agentic_response(data["text"], ai_role, "Defensive but friendly")
                    await conn_manager.broadcast({"type": "CHAT", "user": "Player_AI", "text": reply})

    except WebSocketDisconnect:
        conn_manager.disconnect(client_id)
