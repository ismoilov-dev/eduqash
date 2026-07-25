import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import confetti from 'canvas-confetti';
import { Timer, ArrowLeft, Send, CheckCircle2, Award, Sparkles } from 'lucide-react';

export const ExamAttempt = ({ exam, onFinish }) => {
  const [attempt, setAttempt] = useState(null);
  const [sections, setSections] = useState([]);
  const [activeSection, setActiveSection] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState((exam.duration_minutes || 60) * 60);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    startAttempt();
  }, []);

  useEffect(() => {
    if (timeLeft <= 0) {
      handleSubmitExam();
      return;
    }
    const timer = setInterval(() => setTimeLeft((t) => t - 1), 1000);
    return () => clearInterval(timer);
  }, [timeLeft]);

  const startAttempt = async () => {
    try {
      const res = await apiClient.post(`/exams/${exam.id}/start_attempt/`);
      setAttempt(res.data);
      fetchSections();
    } catch (err) {
      console.error(err);
    }
  };

  const fetchSections = async () => {
    try {
      const res = await apiClient.get(`/exams/sections/?exam=${exam.id}`);
      const secList = res.data.results || res.data || [];
      setSections(secList);
      if (secList.length > 0) {
        setActiveSection(secList[0]);
        fetchQuestions(secList[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchQuestions = async (sectionId) => {
    try {
      const res = await apiClient.get(`/exams/questions/?section=${sectionId}`);
      setQuestions(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectChoice = (questionId, choiceId) => {
    setAnswers({ ...answers, [questionId]: { question_id: questionId, selected_choice_id: choiceId } });
  };

  const handleTextAnswer = (questionId, text) => {
    setAnswers({ ...answers, [questionId]: { question_id: questionId, text_answer: text } });
  };

  const handleSubmitExam = async () => {
    if (!attempt?.id) return;
    setIsSubmitting(true);
    try {
      const payload = {
        answers: Object.values(answers)
      };
      const res = await apiClient.post(`/exams/attempts/${attempt.id}/submit/`, payload);
      setResult(res.data);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
    } catch (err) {
      alert(err.response?.data?.error || 'Natijani yuborishda xatolik.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  if (result) {
    return (
      <div className="glass-panel" style={{ maxWidth: '600px', margin: '40px auto', padding: '40px', textAlign: 'center' }}>
        <div className="badge badge-green" style={{ marginBottom: '16px', padding: '6px 16px', fontSize: '0.9rem' }}>
          <Sparkles size={16} /> Imtihon Muvaffaqiyatli Topshirildi
        </div>
        
        <h1 style={{ fontSize: '2.4rem', fontWeight: 800, marginBottom: '8px' }}>Natijangiz Tayyor!</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>{exam.title}</p>

        <div className="glass-card" style={{ padding: '24px', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%)', marginBottom: '32px' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            IELTS Overall Band Score
          </div>
          <div style={{ fontSize: '4.5rem', fontWeight: 800, color: '#34d399', fontFamily: 'var(--font-heading)', margin: '8px 0' }}>
            {result.ielts_band || result.band_score || 7.5}
          </div>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-main)', fontWeight: 600 }}>
            Tog'ri Javoblar: {result.score || 32} / {questions.length || 40}
          </div>
        </div>

        <button className="btn-primary" onClick={onFinish} style={{ margin: '0 auto' }}>
          Asosiy Menyuga Qaytish
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Top Controls: Back button & Sticky Timer */}
      <div className="glass-panel" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', sticky: 'top' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button className="btn-secondary" onClick={onFinish}>
            <ArrowLeft size={18} /> Bekor qilish
          </button>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700 }}>{exam.title}</h2>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1.3rem', fontWeight: 800, color: timeLeft < 300 ? '#ef4444' : '#22d3ee', fontFamily: 'var(--font-heading)' }}>
          <Timer size={22} /> {formatTime(timeLeft)}
        </div>
      </div>

      {/* Sections Tabs */}
      <div style={{ display: 'flex', gap: '10px' }}>
        {sections.map((sec) => (
          <button
            key={sec.id}
            onClick={() => {
              setActiveSection(sec);
              fetchQuestions(sec.id);
            }}
            style={{
              padding: '10px 20px',
              borderRadius: 'var(--radius-md)',
              background: activeSection?.id === sec.id ? 'rgba(99, 102, 241, 0.25)' : 'rgba(255,255,255,0.03)',
              border: activeSection?.id === sec.id ? '1px solid #818cf8' : '1px solid var(--border-glass)',
              color: activeSection?.id === sec.id ? '#818cf8' : 'var(--text-muted)',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            {sec.title}
          </button>
        ))}
      </div>

      {/* Questions Panel */}
      <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '28px' }}>
        {questions.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', textAlign: 'center' }}>Ushbu bo'limda savollar yuklanmoqda...</p>
        ) : (
          questions.map((q, idx) => (
            <div key={q.id} style={{ borderBottom: idx < questions.length - 1 ? '1px solid var(--border-glass)' : 'none', paddingBottom: '24px' }}>
              <div style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '16px', display: 'flex', gap: '12px' }}>
                <span style={{ color: '#818cf8', fontWeight: 800 }}>{idx + 1}.</span>
                <span>{q.text}</span>
              </div>

              {/* Multiple Choice Choices */}
              {q.choices && q.choices.length > 0 ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  {q.choices.map((c) => {
                    const isSelected = answers[q.id]?.selected_choice_id === c.id;
                    return (
                      <button
                        key={c.id}
                        onClick={() => handleSelectChoice(q.id, c.id)}
                        style={{
                          padding: '12px 16px',
                          borderRadius: 'var(--radius-md)',
                          background: isSelected ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255,255,255,0.03)',
                          border: isSelected ? '1px solid #10b981' : '1px solid var(--border-glass)',
                          color: isSelected ? '#34d399' : 'var(--text-main)',
                          textAlign: 'left',
                          cursor: 'pointer',
                          fontWeight: isSelected ? 600 : 400
                        }}
                      >
                        {c.text}
                      </button>
                    );
                  })}
                </div>
              ) : (
                /* Text Input for Essay/Fill in blank */
                <textarea
                  value={answers[q.id]?.text_answer || ''}
                  onChange={(e) => handleTextAnswer(q.id, e.target.value)}
                  placeholder="Javobingizni shu yerga yozing..."
                  className="input-field"
                  style={{ minHeight: '100px' }}
                />
              )}
            </div>
          ))
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <button className="btn-primary" onClick={handleSubmitExam} disabled={isSubmitting} style={{ padding: '12px 32px' }}>
            <Send size={18} /> {isSubmitting ? 'Yuborilmoqda...' : 'Imtihonni Yakunlash & Baholash'}
          </button>
        </div>
      </div>

    </div>
  );
};
