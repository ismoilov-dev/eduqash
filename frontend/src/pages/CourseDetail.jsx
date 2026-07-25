import React, { useState, useEffect } from 'react';
import { apiClient, uploadFileApi } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Play, ArrowLeft, Video, FileText, Upload, CheckCircle2, Star, Send } from 'lucide-react';

export const CourseDetail = ({ course, onBack }) => {
  const { user } = useAuth();
  const [lessons, setLessons] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [homeworks, setHomeworks] = useState([]);
  const [submissionText, setSubmissionText] = useState('');
  const [submittedMessage, setSubmittedMessage] = useState('');

  useEffect(() => {
    if (course?.id) {
      fetchLessons();
    }
  }, [course]);

  const fetchLessons = async () => {
    try {
      const res = await apiClient.get(`/courses/lessons/?course=${course.id}`);
      const list = res.data.results || res.data || [];
      setLessons(list);
      if (list.length > 0) {
        setActiveLesson(list[0]);
        fetchHomeworks(list[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchHomeworks = async (lessonId) => {
    try {
      const res = await apiClient.get(`/courses/homeworks/?lesson=${lessonId}`);
      setHomeworks(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectLesson = (lesson) => {
    setActiveLesson(lesson);
    setSubmittedMessage('');
    fetchHomeworks(lesson.id);
  };

  const handleSubmitHomework = async (homeworkId) => {
    try {
      await apiClient.post('/courses/submissions/', {
        homework: homeworkId,
        submission_text: submissionText
      });
      setSubmittedMessage('Uy vazifangiz muvaffaqiyatli topshirildi!');
      setSubmissionText('');
    } catch (err) {
      alert(err.response?.data?.error || 'Vazifa topshirishda xatolik.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      
      {/* Back Button & Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button className="btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} /> Orqaga
        </button>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>{course.title}</h1>
      </div>

      {/* Main Content Layout: Video Player + Lessons List */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        
        {/* Video Player & Homework Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {activeLesson ? (
            <div className="glass-panel" style={{ padding: '24px', overflow: 'hidden' }}>
              <div style={{
                position: 'relative',
                paddingTop: '56.25%', // 16:9 Aspect Ratio
                background: '#000',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                marginBottom: '20px'
              }}>
                {activeLesson.video_url ? (
                  <iframe 
                    src={activeLesson.video_url.replace('watch?v=', 'embed/')} 
                    style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
                    allowFullScreen
                    title={activeLesson.title}
                  />
                ) : (
                  <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
                    <Video size={48} style={{ opacity: 0.3 }} />
                  </div>
                )}
              </div>

              <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '8px' }}>{activeLesson.title}</h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: '1.6' }}>
                {activeLesson.content || 'Dars mazmuni va videodarslik.'}
              </p>

              {/* Homework Submission Box */}
              {homeworks.length > 0 && (
                <div style={{ marginTop: '28px', paddingTop: '20px', borderTop: '1px solid var(--border-glass)' }}>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={20} color="#818cf8" /> Uy Vazifasi
                  </h3>
                  
                  {homeworks.map((hw) => (
                    <div key={hw.id} className="glass-card" style={{ padding: '16px', marginBottom: '12px' }}>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem', marginBottom: '4px' }}>{hw.title}</div>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '12px' }}>{hw.description}</p>

                      {submittedMessage ? (
                        <div style={{ color: '#34d399', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <CheckCircle2 size={16} /> {submittedMessage}
                        </div>
                      ) : (
                        <div style={{ display: 'flex', gap: '10px' }}>
                          <textarea 
                            value={submissionText}
                            onChange={(e) => setSubmissionText(e.target.value)}
                            placeholder="Javobingiz va vazifa matni..."
                            className="input-field"
                            style={{ minHeight: '60px' }}
                          />
                          <button 
                            className="btn-accent" 
                            style={{ height: 'fit-content', alignSelf: 'flex-end' }}
                            onClick={() => handleSubmitHomework(hw.id)}
                          >
                            <Send size={16} /> Topshirish
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-dim)' }}>
              Ushbu kursda hozircha darslar yuklanmagan.
            </div>
          )}

        </div>

        {/* Lessons Sidebar */}
        <div className="glass-panel" style={{ padding: '20px', height: 'fit-content' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Kurs Darslari ({lessons.length})</h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {lessons.map((lesson, idx) => {
              const isSelected = activeLesson?.id === lesson.id;
              return (
                <div
                  key={lesson.id}
                  onClick={() => handleSelectLesson(lesson)}
                  style={{
                    padding: '12px 14px',
                    borderRadius: 'var(--radius-md)',
                    background: isSelected ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.02)',
                    border: isSelected ? '1px solid #818cf8' : '1px solid var(--border-glass)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px'
                  }}
                >
                  <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: isSelected ? '#6366f1' : 'rgba(255,255,255,0.1)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: 700 }}>
                    {idx + 1}
                  </div>
                  <div style={{ fontSize: '0.9rem', fontWeight: isSelected ? 600 : 500, color: isSelected ? '#818cf8' : 'var(--text-main)' }}>
                    {lesson.title}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

    </div>
  );
};
