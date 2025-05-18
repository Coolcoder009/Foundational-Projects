import React, { useState, useRef, useEffect } from 'react';
import './App.css';

// Base URL from env (CRA or Vite) — fallback to localhost
const API_BASE = process.env.REACT_APP_API_URL;

export default function FullScreenChatbot() {
  const [messages, setMessages] = useState([]); // {role:'user'|'assistant', text:string}
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const sendMessage = async () => {
    const txt = input.trim();
    if (!txt) return;
    setMessages(m => [...m, { role: 'user', text: txt }]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/query-response`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: txt })
      });
      const data = await res.json();
      setMessages(m => [...m, { role: 'assistant', text: data.reply || data.text || '...' }]);
    } catch (err) {
      setMessages(m => [...m, { role: 'assistant', text: 'Server error.' }]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleKey = e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="cb-container">
      <div className="cb-messages">
        {messages.map((m, i) => (
          <div key={i} className={`cb-msg cb-${m.role}`}>
            {m.text}
          </div>
        ))}

        {loading && (
          <div className="cb-spinner-wrapper">
            <div className="cb-spinner" />
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="cb-input-bar">
        <textarea
          className="cb-input"
          value={input}
          placeholder="Type…"
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
        />
        <button className="cb-send-btn" onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
