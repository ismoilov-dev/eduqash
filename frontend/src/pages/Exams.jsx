import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { FileCheck2, Timer, Award, Play, Sparkles, CheckCircle } from 'lucide-react';

export const Exams = ({ onStartExam }) => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState(''); // '' | 'ielts_mock' | 'cefr' | 'custom'

  useEffect(() => {
    fetchExams();
  }, [filterType]);

  const fetchExams = async () => {
    setLoading(true);
    try {
      const url = filterType ? `/exams/?exam_type=${filterType}` : '/exams/';
      const res = await apiClient.get(url);
      setExams(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '36px', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%)' }}>
        <div className="badge badge-purple" style={{ marginBottom: '12px' }}>
          <Sparkles size={14} /> Avtomatik IELTS & CEFR Band Evaluator
        </div>
        <h1 style={{ fontSize: '2.4rem', fontWeight: 800, marginBottom: '12px' }}>
          IELTS Mock & CEFR Real-Time Imtihonlar Simulyatsiyasi
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1rem', maxWidth: '750px', lineHeight: '1.6' }}>
          Xalqaro standartlarga to'liq mos keladigan real vaqt taymerli Listening, Reading va Writing testlarini topshiring hamda bir sekundda IELTS Band balingizni oling!
        </p>
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px' }}>
        {[
          { id: '', label: 'Barcha Imtihonlar' },
          { id: 'ielts_mock', label: '🇬🇧 IELTS Mock' },
          { id: 'cefr', label: '🇪🇺 CEFR Exam' },
          { id: 'custom', label: '📝 Maxsus Testlar' },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setFilterType(t.id)}
            style={{
              background: filterType === t.id ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.03)',
              border: filterType === t.id ? '1px solid #818cf8' : '1px solid var(--border-glass)',
              color: filterType === t.id ? '#818cf8' : 'var(--text-muted)',
              padding: '10px 18px',
              borderRadius: 'var(--radius-md)',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Exams Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>Yuklanmoqda...</div>
      ) : exams.length === 0 ? (
        <div className="glass-panel" style={{ padding: '60px', textAlign: 'center', color: 'var(--text-dim)' }}>
          <FileCheck2 size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
          <h3>Hozircha imtihonlar mavjud emas</h3>
        </div>
      ) : (
        <div className="grid-cards">
          {exams.map((exam) => (
            <div key={exam.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className="badge badge-purple" style={{ textTransform: 'uppercase' }}>
                  {exam.exam_type?.replace('_', ' ')}
                </span>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Timer size={16} color="#06b6d4" /> {exam.duration_minutes || 60} daqiqa
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '8px' }}>{exam.title}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: '1.5' }}>
                  {exam.description || "Listening, Reading va Writing bo'limlari bilan to'liq imtihon."}
                </p>
              </div>

              <button 
                className="btn-primary" 
                style={{ width: '100%', justifyContent: 'center', marginTop: 'auto' }}
                onClick={() => onStartExam(exam)}
              >
                <Play size={16} /> Imtihonni Boshlash
              </button>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};
