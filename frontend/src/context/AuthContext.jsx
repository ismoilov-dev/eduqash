import React, { createContext, useState, useEffect, useContext } from 'react';
import { apiClient } from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const handleLogoutEvent = () => {
      setUser(null);
    };
    window.addEventListener('auth-logout', handleLogoutEvent);
    return () => window.removeEventListener('auth-logout', handleLogoutEvent);
  }, []);

  const saveAuthData = (userData, tokens) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    if (tokens?.access) localStorage.setItem('access_token', tokens.access);
    if (tokens?.refresh) localStorage.setItem('refresh_token', tokens.refresh);
  };

  const login = async (credentials) => {
    setLoading(true);
    try {
      const res = await apiClient.post('/auth/login/', credentials);
      saveAuthData(res.data.user, res.data.tokens);
      return { success: true, user: res.data.user };
    } catch (err) {
      return { success: false, message: err.response?.data?.error || 'Login xatoligi yuz berdi.' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (data) => {
    setLoading(true);
    try {
      const res = await apiClient.post('/auth/register/', data);
      saveAuthData(res.data.user, res.data.tokens);
      return { success: true, message: res.data.message };
    } catch (err) {
      return { success: false, message: err.response?.data?.error || Object.values(err.response?.data || {}).flat().join(' ') || 'Ro\'yxatdan o\'tish xatosi.' };
    } finally {
      setLoading(false);
    }
  };

  const verifyEmail = async (email, code) => {
    try {
      const res = await apiClient.post('/auth/verify-email/', { email, code });
      if (user) {
        const updated = { ...user, is_email_verified: true };
        setUser(updated);
        localStorage.setItem('user', JSON.stringify(updated));
      }
      return { success: true, message: res.data.message };
    } catch (err) {
      return { success: false, message: err.response?.data?.error || 'Kod noto\'g\'ri.' };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, verifyEmail, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
