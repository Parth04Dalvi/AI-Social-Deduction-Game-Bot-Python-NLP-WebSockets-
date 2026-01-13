import { useState, useEffect } from 'react';

export default function ChatRoom({ clientId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data); // Parsing structured JSON
      setMessages((prev) => [...prev, data]);
    };
    setSocket(ws);
    return () => ws.close();
  }, [clientId]);

  const sendMessage = () => {
    if (socket && input) {
      socket.send(JSON.stringify({ type: "MESSAGE", text: input }));
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 p-6 text-slate-100 font-sans">
      <div className="flex justify-between border-b border-slate-800 pb-4 mb-4">
        <h1 className="text-2xl font-black text-red-500 tracking-tighter uppercase">Imposter AI</h1>
        <div className="text-xs text-slate-500 uppercase self-center">Status: Game Active</div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 mb-6 pr-4 custom-scrollbar">
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col ${msg.user === clientId ? 'items-end' : 'items-start'}`}>
            <span className="text-[10px] text-slate-500 uppercase mb-1">{msg.user || 'System'}</span>
            <div className={`px-4 py-2 rounded-2xl max-w-[80%] ${
              msg.user === 'Player_AI' ? 'bg-red-900/30 border border-red-500/50' : 
              msg.user === clientId ? 'bg-blue-600' : 'bg-slate-800'
            }`}>
              {msg.text || msg.content}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input 
          className="flex-1 bg-slate-900 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-500"
          placeholder="Defend yourself..."
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage} className="bg-red-600 px-6 py-3 rounded-xl font-bold hover:bg-red-700 transition-all">SEND</button>
      </div>
    </div>
  );
}
