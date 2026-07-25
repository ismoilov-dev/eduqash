import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { Bell, CheckCheck, X, Sparkles } from 'lucide-react';

export const NotificationCenter = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchNotifications();
    }
  }, [isOpen]);

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/notifications/');
      setNotifications(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const markAllRead = async () => {
    try {
      await apiClient.post('/notifications/mark_all_read/');
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.6)',
      zIndex: 100,
      display: 'flex',
      justifyContent: 'flex-end'
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '420px',
        height: '100vh',
        borderRadius: 0,
        padding: '24px',
        display: 'flex',
        flexDirection: 'column',
        borderRight: 'none',
        borderTop: 'none',
        borderBottom: 'none'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Bell size={22} color="#818cf8" />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Bildirishnomalar</h3>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button 
              onClick={markAllRead} 
              style={{ background: 'none', border: 'none', color: '#10b981', cursor: 'pointer', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <CheckCheck size={16} /> Barchasini o'qilgan deb belgilash
            </button>
            <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
              <X size={20} />
            </button>
          </div>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {loading ? (
            <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginTop: '40px' }}>Yuklanmoqda...</p>
          ) : notifications.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'var(--text-dim)', marginTop: '80px' }}>
              <Bell size={40} style={{ opacity: 0.3, marginBottom: '12px' }} />
              <p>Hozircha yangi bildirishnomalar yo'q</p>
            </div>
          ) : (
            notifications.map((n) => (
              <div 
                key={n.id} 
                className="glass-card" 
                style={{ 
                  padding: '14px', 
                  opacity: n.is_read ? 0.6 : 1, 
                  borderLeft: n.is_read ? '1px solid var(--border-glass)' : '3px solid #818cf8' 
                }}
              >
                <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '4px' }}>
                  {n.title || 'Bildirishnoma'}
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                  {n.message || n.text}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '8px', textAlign: 'right' }}>
                  {new Date(n.created_at || Date.now()).toLocaleString()}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
