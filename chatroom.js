// components/ChatRoom.js
import { useState, useEffect } from 'react';

export default function ChatRoom({ clientId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);
  const [myRole, setMyRole] = useState('Waiting...');

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "ROLE_ASSIGN") setMyRole(data.role);
      setMessages((prev) => [...prev, data]);
    };
    setSocket(ws);
    return () => ws.close();
  }, [clientId]);

  const sendVote = (targetId) => {
    socket.send(JSON.stringify({ type: "VOTE", target: targetId }));
  };

  return (
    <div className="p-4 max-w-lg mx-auto bg-slate-900 text-white rounded-2xl shadow-2xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-red-500">ImposterAI</h2>
        <span className="text-xs bg-gray-700 px-2 py-1 rounded">Role: {myRole}</span>
      </div>

      <div className="h-80 overflow-y-auto space-y-2 border-b border-gray-800 mb-4 p-2">
        {messages.map((msg, i) => (
          <div key={i} className={`text-sm ${msg.type === 'SYSTEM' ? 'text-yellow-400 italic' : ''}`}>
            {msg.user && <b className="text-blue-400">{msg.user}: </b>}
            {msg.content}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input 
          className="flex-1 bg-gray-800 p-3 rounded-lg outline-none focus:ring-2 focus:ring-red-500"
          placeholder="Type your defense..."
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && socket.send(JSON.stringify({type: "CHAT", content: input}))}
        />
        <button onClick={() => sendVote("Player_AI")} className="bg-red-600 px-4 py-2 rounded-lg font-bold hover:bg-red-700">Vote AI</button>
      </div>
    </div>
  );
}
