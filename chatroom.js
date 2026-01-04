// components/ChatRoom.js
import { useState, useEffect } from 'react';

export default function ChatRoom({ clientId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };
    setSocket(ws);
    return () => ws.close();
  }, [clientId]);

  const sendMessage = () => {
    socket.send(input);
    setInput('');
  };

  return (
    <div className="p-4 max-w-lg mx-auto bg-gray-900 text-white rounded-xl">
      <h2 className="text-xl font-bold mb-4">The Imposter Room</h2>
      <div className="h-64 overflow-y-auto border-b border-gray-700 mb-4">
        {messages.map((msg, i) => (
          <p key={i} className="mb-2">{msg}</p>
        ))}
      </div>
      <input 
        className="bg-gray-800 p-2 w-full rounded"
        value={input} 
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
      />
    </div>
  );
}
