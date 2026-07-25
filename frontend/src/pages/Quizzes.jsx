import React, { useState, useEffect } from 'react';
import { apiClient, uploadFileApi } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Trophy, Upload, Sparkles, CheckCircle2, Play, Star, Award, Layers } from 'lucide-react';

export const Quizzes = () => {
  const { user } = useAuth();
  const [quizzes, setQuizzes] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  const [excelFile, setExcelFile] = useState(null);
  const [bankId, setBankId] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');

  useEffect(() => {
    fetchQuizzesAndLeaderboard();
  }, []);

  const fetchQuizzesAndLeaderboard = async () => {
    setLoading(true);
    try {
      const qRes = await apiClient.get('/quizzes/');
      setQuizzes(qRes.data.results || qRes.data || []);

      const lRes = await apiClient.get('/quizzes/leaderboard/');
      setLeaderboard(lRes.data.results || lRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExcelUpload = async (e) => {
    e.preventDefault();
    if (!excelFile) return;
    const formData = new FormData();
    formData.append('file', excelFile);
    if (bankId) formData.append('bank_id', bankId);

    try {
      await uploadFileApi('/quizzes/import-excel/', formData);
      setUploadSuccess('Excel savollari muvaffaqiyatli yuklandi!');
      setExcelFile(null);
      fetchQuizzesAndLeaderboard();
    } catch (err) {
      alert(err.response?.data?.error || 'Excel yuklashda xatolik.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', fontWeight: 800 }}>Quizlar va Peshqadamlar Jadvali</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>
            Interaktiv bilim sinovlari va haftalik peshqadam o'quvchilar reytingi
          </p>
        </div>
      </div>

      {/* Main Layout: Quizzes list + Leaderboard */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '28px' }}>
        
        {/* Quizzes List & Excel Upload */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Excel Import Box (For Teachers/Admins) */}
          {(user?.role === 'teacher' || user?.role === 'admin' || user?.role === 'super_admin') && (
            <div className="glass-panel" style={{ padding: '24px', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%)' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Upload size={20} color="#c084fc" /> Excel (.xlsx) Orqali Savollarni Yuklash
              </h3>

              {uploadSuccess && (
                <div style={{ color: '#34d399', fontSize: '0.85rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckCircle2 size={16} /> {uploadSuccess}
                </div>
              )}

              <form onSubmit={handleExcelUpload} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <input 
                  type="file" 
                  accept=".xlsx, .xls"
                  onChange={(e) => setExcelFile(e.target.files[0])}
                  className="input-field" 
                  style={{ flex: 1 }}
                  required
                />
                <button type="submit" className="btn-accent">
                  Import Qilish
                </button>
              </form>
            </div>
          )}

          {/* Quizzes Cards */}
          {loading ? (
            <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px' }}>Yuklanmoqda...</div>
          ) : (
            <div className="grid-cards" style={{ gridTemplateColumns: '1fr 1fr' }}>
              {quizzes.map((quiz) => (
                <div key={quiz.id} className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span className="badge badge-cyan">
                      <Layers size={14} /> {quiz.category || 'General'}
                    </span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      ⏱️ {quiz.time_limit_minutes || 15} daq
                    </span>
                  </div>

                  <div>
                    <h4 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '4px' }}>{quiz.title}</h4>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{quiz.description || 'Tezkor bilim sinovi testlari.'}</p>
                  </div>

                  <button className="btn-primary" style={{ marginTop: 'auto', padding: '8px 16px', fontSize: '0.85rem', justifyContent: 'center' }}>
                    <Play size={14} /> Quizni Boshlash
                  </button>
                </div>
              ))}
            </div>
          )}

        </div>

        {/* Leaderboard Panel */}
        <div className="glass-panel" style={{ padding: '24px', height: 'fit-content' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <Trophy size={24} color="#fbbf24" />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>Peshqadamlar Jadvali</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {leaderboard.length > 0 ? (
              leaderboard.map((item, idx) => (
                <div 
                  key={idx} 
                  className="glass-card"
                  style={{ 
                    padding: '12px 16px', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between',
                    background: idx === 0 ? 'rgba(245, 158, 11, 0.15)' : 'rgba(255,255,255,0.02)',
                    border: idx === 0 ? '1px solid rgba(245, 158, 11, 0.4)' : '1px solid var(--border-glass)'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ 
                      width: '28px', 
                      height: '28px', 
                      borderRadius: '50%', 
                      background: idx === 0 ? '#f59e0b' : idx === 1 ? '#94a3b8' : idx === 2 ? '#b45309' : 'rgba(255,255,255,0.1)',
                      color: '#fff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 800,
                      fontSize: '0.8rem'
                    }}>
                      {idx + 1}
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{item.user_name || item.username || 'Student'}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{item.quiz_title || 'Quiz'}</div>
                    </div>
                  </div>

                  <div style={{ fontWeight: 800, color: '#34d399', fontSize: '1rem', fontFamily: 'var(--font-heading)' }}>
                    {item.score} ball
                  </div>
                </div>
              ))
            ) : (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center' }}>Reytinglar yuklanmoqda...</p>
            )}
          </div>
        </div>

      </div>

    </div>
  );
};
