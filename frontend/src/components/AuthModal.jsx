import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { X, Lock, Mail, User, BookOpen, Building2, Sparkles, CheckCircle2 } from 'lucide-react';

export const AuthModal = ({ isOpen, onClose }) => {
  const { login, register, verifyEmail } = useAuth();
  const [mode, setMode] = useState('login'); // 'login' | 'register' | 'verify'
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'student',
    bio: ''
  });
  const [verifyCode, setVerifyCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  if (!isOpen) return null;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const res = await login({ username: formData.username || formData.email, password: formData.password });
    if (res.success) {
      onClose();
    } else {
      setError(res.message);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const res = await register(formData);
    if (res.success) {
      setSuccess('Muvaffaqiyatli ro\'yxatdan o\'tdingiz! Emailingizga tasdiqlash kodi yuborildi.');
      setMode('verify');
    } else {
      setError(res.message);
    }
  };

  const handleVerifySubmit = async (e) => {
    e.preventDefault();
    setError('');
    const res = await verifyEmail(formData.email, verifyCode);
    if (res.success) {
      setSuccess('Email muvaffaqiyatli tasdiqlandi!');
      setTimeout(() => onClose(), 1500);
    } else {
      setError(res.message);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100
    }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '480px', padding: '32px', position: 'relative' }}>
        
        <button 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer'
          }}
        >
          <X size={24} />
        </button>

        {/* Modal Title */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800 }}>
            {mode === 'login' && 'Tizimga Kirish'}
            {mode === 'register' && 'Ro\'yxatdan O\'tish'}
            {mode === 'verify' && 'Email Kodini Tasdiqlash'}
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            EDUQASH PRO platformasining barcha imkoniyatlaridan foydalaning
          </p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', padding: '10px 14px', borderRadius: 'var(--radius-md)', fontSize: '0.85rem', marginBottom: '16px' }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#34d399', padding: '10px 14px', borderRadius: 'var(--radius-md)', fontSize: '0.85rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={18} /> {success}
          </div>
        )}

        {/* Mode Forms */}
        {mode === 'login' && (
          <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Username yoki Email</label>
              <input 
                type="text" 
                name="username"
                value={formData.username} 
                onChange={handleChange}
                placeholder="masalan: ismat_dev yoki ismat@gmail.com" 
                className="input-field" 
                required 
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Parol</label>
              <input 
                type="password" 
                name="password"
                value={formData.password} 
                onChange={handleChange}
                placeholder="••••••••" 
                className="input-field" 
                required 
              />
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '8px' }}>
              Tizimga Kirish
            </button>

            <div style={{ textAlign: 'center', marginTop: '16px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Hisobingiz yo'qmi?{' '}
              <button 
                type="button" 
                onClick={() => { setMode('register'); setError(''); }}
                style={{ background: 'none', border: 'none', color: '#818cf8', fontWeight: 600, cursor: 'pointer' }}
              >
                Ro'yxatdan o'ting
              </button>
            </div>
          </form>
        )}

        {mode === 'register' && (
          <form onSubmit={handleRegisterSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Ism</label>
                <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} placeholder="Ismingiz" className="input-field" required />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Familiya</label>
                <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Familiyangiz" className="input-field" required />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Username</label>
              <input type="text" name="username" value={formData.username} onChange={handleChange} placeholder="ismat_dev" className="input-field" required />
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Email</label>
              <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="ismat@gmail.com" className="input-field" required />
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Parol</label>
              <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="••••••••" className="input-field" required />
            </div>

            {/* Role Selection */}
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px', display: 'block' }}>Tizimdagi Rolingiz</label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
                {[
                  { id: 'student', label: 'Talaba', icon: User },
                  { id: 'teacher', label: 'O\'qituvchi', icon: BookOpen },
                  { id: 'center_owner', label: 'Markaz Egalari', icon: Building2 },
                ].map((r) => {
                  const Icon = r.icon;
                  const isSelected = formData.role === r.id;
                  return (
                    <button
                      key={r.id}
                      type="button"
                      onClick={() => setFormData({ ...formData, role: r.id })}
                      style={{
                        padding: '10px 4px',
                        borderRadius: 'var(--radius-md)',
                        background: isSelected ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.03)',
                        border: isSelected ? '1px solid #818cf8' : '1px solid var(--border-glass)',
                        color: isSelected ? '#818cf8' : 'var(--text-muted)',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        gap: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      <Icon size={16} />
                      {r.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '8px' }}>
              Ro'yxatdan O'tish
            </button>

            <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Akkountingiz bormi?{' '}
              <button 
                type="button" 
                onClick={() => { setMode('login'); setError(''); }}
                style={{ background: 'none', border: 'none', color: '#818cf8', fontWeight: 600, cursor: 'pointer' }}
              >
                Tizimga kirish
              </button>
            </div>
          </form>
        )}

        {mode === 'verify' && (
          <form onSubmit={handleVerifySubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center' }}>
              <strong>{formData.email}</strong> manziliga yuborilgan 6 xonali tasdiqlash kodini kiriting:
            </p>

            <input 
              type="text" 
              value={verifyCode} 
              onChange={(e) => setVerifyCode(e.target.value)}
              placeholder="123456" 
              className="input-field" 
              style={{ textAlign: 'center', fontSize: '1.4rem', letterSpacing: '0.3em', fontWeight: 700 }}
              maxLength={6}
              required 
            />

            <button type="submit" className="btn-accent" style={{ width: '100%', justifyContent: 'center' }}>
              Kodni Tasdiqlash
            </button>
          </form>
        )}

      </div>
    </div>
  );
};
