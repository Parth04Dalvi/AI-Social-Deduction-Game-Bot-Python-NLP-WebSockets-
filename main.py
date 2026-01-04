import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import google.generativeai as genai

app = FastAPI()

# Configure your Gemini API (already in your skill set) [cite: 46]
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# The "Social Deduction" Prompt Logic
async def get_ai_response(chat_history: str):
    prompt = f"""
    You are a secret AI player in a game of 'Imposter'. 
    The players are discussing who the AI is. 
    Your goal is to blend in, act slightly casual, and deflect suspicion.
    Chat History: {chat_history}
    Respond with one short sentence as 'User_AI':
    """
    response = model.generate_content(prompt)
    return response.text

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the human message
            await manager.broadcast(f"{client_id}: {data}")
            
            # Logic: If someone mentions 'AI', the Bot defends itself
            if "AI" in data or "imposter" in data:
                ai_reply = await get_ai_response(data)
                await manager.broadcast(f"Player_4: {ai_reply}") # Bot hides as Player_4
    except WebSocketDisconnect:
        manager.disconnect(websocket)
