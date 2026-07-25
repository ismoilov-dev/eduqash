import React, { useState, useEffect, useRef } from 'react';
import { apiClient } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { MessageSquare, Send, Paperclip, User, Circle } from 'lucide-react';

export const Chat = () => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [activeConv, setActiveConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(true);
  
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (activeConv) {
      fetchMessages(activeConv.id);
      connectWebSocket(activeConv.id);
    }
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [activeConv]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchConversations = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/chat/conversations/');
      const list = res.data.results || res.data || [];
      setConversations(list);
      if (list.length > 0) {
        setActiveConv(list[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (convId) => {
    try {
      const res = await apiClient.get(`/chat/messages/?conversation=${convId}`);
      setMessages(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const connectWebSocket = (convId) => {
    if (socketRef.current) {
      socketRef.current.close();
    }
    const token = localStorage.getItem('access_token');
    const wsHost = import.meta.env.VITE_WS_URL || '169.58.72.177';
    const wsUrl = `ws://${wsHost}/ws/chat/${convId}/?token=${token}`;

    try {
      const ws = new WebSocket(wsUrl);
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      };
      socketRef.current = ws;
    } catch (e) {
      console.error('WebSocket connection error:', e);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || !activeConv) return;

    const payload = { message: inputText.trim() };

    // Send via WebSocket if open
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(payload));
      setInputText('');
    } else {
      // Fallback REST API POST
      try {
        const res = await apiClient.post('/chat/messages/', {
          conversation: activeConv.id,
          text: inputText.trim()
        });
        setMessages((prev) => [...prev, res.data]);
        setInputText('');
      } catch (err) {
        console.error(err);
      }
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', height: 'calc(100vh - 180px)' }}>
      
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800 }}>Jonli Muloqot & Chat</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          O'qituvchilar va o'quvchilar o'rtasidagi real-vaqtli WebSocket suhbatlari
        </p>
      </div>

      {/* Main Chat Layout: Sidebar + Messages Box */}
      <div className="glass-panel" style={{ flex: 1, display: 'grid', gridTemplateColumns: '300px 1fr', overflow: 'hidden', padding: 0 }}>
        
        {/* Conversations List Sidebar */}
        <div style={{ borderRight: '1px solid var(--border-glass)', display: 'flex', flexDirection: 'column', padding: '16px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '14px', color: 'var(--text-muted)' }}>Suhbatlar</h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto' }}>
            {conversations.length > 0 ? (
              conversations.map((conv) => {
                const isSelected = activeConv?.id === conv.id;
                return (
                  <div
                    key={conv.id}
                    onClick={() => setActiveConv(conv)}
                    style={{
                      padding: '12px',
                      borderRadius: 'var(--radius-md)',
                      background: isSelected ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.02)',
                      border: isSelected ? '1px solid #818cf8' : '1px solid var(--border-glass)',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '10px'
                    }}
                  >
                    <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 700 }}>
                      <User size={18} />
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.88rem' }}>{conv.title || 'Chat Group'}</div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Online</div>
                    </div>
                  </div>
                );
              })
            ) : (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', marginTop: '20px' }}>Hozircha suhbatlar yo'q</p>
            )}
          </div>
        </div>

        {/* Active Messages Box */}
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          
          {activeConv ? (
            <>
              {/* Chat Header */}
              <div style={{ padding: '16px 24px', borderBottom: '1px solid var(--border-glass)', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Circle size={10} fill="#10b981" color="#10b981" />
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{activeConv.title || 'Muloqot'}</h3>
              </div>

              {/* Messages History */}
              <div style={{ flex: 1, padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {messages.map((msg, idx) => {
                  const isMine = msg.sender_id === user?.id || msg.sender === user?.username;
                  return (
                    <div
                      key={idx}
                      style={{
                        alignSelf: isMine ? 'flex-end' : 'flex-start',
                        maxWidth: '70%',
                        background: isMine ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)' : 'rgba(30, 41, 59, 0.6)',
                        border: isMine ? 'none' : '1px solid var(--border-glass)',
                        color: '#fff',
                        padding: '12px 16px',
                        borderRadius: '16px',
                        borderBottomRightRadius: isMine ? '4px' : '16px',
                        borderBottomLeftRadius: isMine ? '16px' : '4px',
                        boxShadow: isMine ? '0 4px 15px rgba(99, 102, 241, 0.3)' : 'none'
                      }}
                    >
                      <div style={{ fontSize: '0.75rem', opacity: 0.8, fontWeight: 600, marginBottom: '2px' }}>
                        {msg.sender_username || msg.sender || 'Foydalanuvchi'}
                      </div>
                      <div style={{ fontSize: '0.92rem', lineHeight: '1.5' }}>
                        {msg.message || msg.text}
                      </div>
                    </div>
                  );
                })}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Form */}
              <form onSubmit={handleSendMessage} style={{ padding: '16px 24px', borderTop: '1px solid var(--border-glass)', display: 'flex', gap: '12px' }}>
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Xabaringizni yozing..."
                  className="input-field"
                  style={{ flex: 1 }}
                />
                <button type="submit" className="btn-primary" style={{ padding: '10px 20px' }}>
                  <Send size={18} />
                </button>
              </form>
            </>
          ) : (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-dim)' }}>
              Suhbatni tanlang
            </div>
          )}

        </div>

      </div>

    </div>
  );
};
