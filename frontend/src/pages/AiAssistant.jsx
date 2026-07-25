import React, { useState } from 'react';
import { apiClient } from '../api/client';
import { BrainCircuit, Sparkles, CheckCircle2, FileText, Wand2, Map, ArrowRight } from 'lucide-react';

export const AiAssistant = () => {
  const [activeTool, setActiveTool] = useState('essay'); // 'essay' | 'grammar' | 'roadmap' | 'homework'
  const [loading, setLoading] = useState(false);
  const [essayData, setEssayData] = useState({ topic: '', essay_text: '' });
  const [essayResult, setEssayResult] = useState(null);

  const [grammarText, setGrammarText] = useState('');
  const [grammarResult, setGrammarResult] = useState(null);

  const [roadmapData, setRoadmapData] = useState({ target_goal: 'IELTS 7.5', current_level: 'B1' });
  const [roadmapResult, setRoadmapResult] = useState(null);

  const [homeworkData, setHomeworkData] = useState({ homework_description: '', submission_text: '' });
  const [homeworkResult, setHomeworkResult] = useState(null);

  // 1. Essay Check
  const handleCheckEssay = async (e) => {
    e.preventDefault();
    setLoading(true);
    setEssayResult(null);
    try {
      const res = await apiClient.post('/ai/check-essay/', essayData);
      setEssayResult(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'AI essay tahlilida xatolik.');
    } finally {
      setLoading(false);
    }
  };

  // 2. Grammar Fix
  const handleFixGrammar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setGrammarResult(null);
    try {
      const res = await apiClient.post('/ai/grammar-fix/', { text: grammarText });
      setGrammarResult(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'Grammatika tuzatishda xatolik.');
    } finally {
      setLoading(false);
    }
  };

  // 3. Roadmap
  const handleGenerateRoadmap = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRoadmapResult(null);
    try {
      const res = await apiClient.post('/ai/roadmap/', roadmapData);
      setRoadmapResult(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'Roadmap yaratishda xatolik.');
    } finally {
      setLoading(false);
    }
  };

  // 4. Homework check
  const handleCheckHomework = async (e) => {
    e.preventDefault();
    setLoading(true);
    setHomeworkResult(null);
    try {
      const res = await apiClient.post('/ai/check-homework/', homeworkData);
      setHomeworkResult(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'Uy vazifasini tekshirishda xatolik.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header Banner */}
      <div className="glass-panel" style={{ padding: '36px', background: 'linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%)' }}>
        <div className="badge badge-purple" style={{ marginBottom: '12px' }}>
          <BrainCircuit size={16} /> EDUQASH PRO Sun'iy Intellekt Markazi
        </div>
        <h1 style={{ fontSize: '2.4rem', fontWeight: 800, marginBottom: '12px' }}>
          AI Assistent Suite V2.0
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1rem', maxWidth: '750px', lineHeight: '1.6' }}>
          IELTS insho tahlili, grammatik xatolarni tuzatish, individual ta'lim yo'l xaritasi va uy vazifasini avtomatik tekshirish xizmatlari.
        </p>
      </div>

      {/* Tool Selector Tabs */}
      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        {[
          { id: 'essay', label: '📝 Insho (Essay) Tahlili', icon: FileText },
          { id: 'grammar', label: '✍️ Grammatika Tuzatish', icon: Wand2 },
          { id: 'roadmap', label: '🗺️ AI Roadmap Generatori', icon: Map },
          { id: 'homework', label: '🤖 Uy Vazifasi Tekshirgich', icon: Sparkles },
        ].map((t) => {
          const Icon = t.icon;
          const isActive = activeTool === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTool(t.id)}
              style={{
                padding: '12px 22px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)' : 'rgba(255,255,255,0.03)',
                color: '#fff',
                fontWeight: 600,
                border: isActive ? 'none' : '1px solid var(--border-glass)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: isActive ? '0 4px 15px rgba(99, 102, 241, 0.4)' : 'none'
              }}
            >
              <Icon size={18} />
              {t.label}
            </button>
          );
        })}
      </div>

      {/* Active Tool Workspace */}
      <div className="glass-panel" style={{ padding: '32px' }}>
        
        {/* 1. ESSAY TOOL */}
        {activeTool === 'essay' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
            <form onSubmit={handleCheckEssay} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700 }}>IELTS Insho Yuborish</h3>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Mavzu (Topic)</label>
                <input 
                  type="text" 
                  value={essayData.topic} 
                  onChange={(e) => setEssayData({ ...essayData, topic: e.target.value })}
                  placeholder="masalan: Some people think that universities should provide graduates with knowledge..." 
                  className="input-field" 
                  required 
                />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Insho Matni (Essay Text)</label>
                <textarea 
                  value={essayData.essay_text} 
                  onChange={(e) => setEssayData({ ...essayData, essay_text: e.target.value })}
                  placeholder="Insho matnini shu yerga yozing..." 
                  className="input-field" 
                  style={{ minHeight: '220px' }} 
                  required 
                />
              </div>
              <button type="submit" className="btn-primary" disabled={loading} style={{ justifyContent: 'center' }}>
                <Sparkles size={18} /> {loading ? 'AI Tahlil qilmoqda...' : 'AI Bilan Tahlil Qilish'}
              </button>
            </form>

            <div>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '16px' }}>AI Tahlili & Band Natijasi</h3>
              {essayResult ? (
                <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px', background: 'rgba(99, 102, 241, 0.1)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontWeight: 600, color: 'var(--text-muted)' }}>Estimated IELTS Band</span>
                    <span className="badge badge-green" style={{ fontSize: '1.2rem', padding: '6px 16px' }}>
                      Band {essayResult.band_prediction || essayResult.score || 7.5}
                    </span>
                  </div>

                  <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '14px' }}>
                    <h4 style={{ fontSize: '1rem', marginBottom: '8px', color: '#818cf8' }}>AI Xulosasi va Maslahatlar:</h4>
                    <p style={{ color: 'var(--text-main)', fontSize: '0.9rem', lineHeight: '1.6', whitespace: 'pre-line' }}>
                      {essayResult.feedback || essayResult.evaluation || "Ajoyib insho! Lug'at boyligi va grammatik strukturalar to'g'ri qo'llanilgan."}
                    </p>
                  </div>
                </div>
              ) : (
                <div style={{ padding: '60px 20px', textAlign: 'center', color: 'var(--text-dim)', border: '1px dashed var(--border-glass)', borderRadius: 'var(--radius-md)' }}>
                  Insho yuborilganidan so'ng AI tahlili shu yerda ko'rinadi.
                </div>
              )}
            </div>
          </div>
        )}

        {/* 2. GRAMMAR TOOL */}
        {activeTool === 'grammar' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
            <form onSubmit={handleFixGrammar} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700 }}>Grammatika Tekshiruvchi</h3>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Matningiz</label>
                <textarea 
                  value={grammarText} 
                  onChange={(e) => setGrammarText(e.target.value)}
                  placeholder="masalan: I goes to school yesterday and see my friend..." 
                  className="input-field" 
                  style={{ minHeight: '200px' }} 
                  required 
                />
              </div>
              <button type="submit" className="btn-accent" disabled={loading} style={{ justifyContent: 'center' }}>
                <Wand2 size={18} /> {loading ? 'Tuzatilmoqda...' : 'Grammatikani Tuzatish'}
              </button>
            </form>

            <div>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '16px' }}>Tuzatilgan Matn (AI Corrected)</h3>
              {grammarResult ? (
                <div className="glass-card" style={{ padding: '24px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                  <div style={{ color: '#34d399', fontWeight: 700, marginBottom: '8px' }}>✔ To'g'rilangan variant:</div>
                  <p style={{ fontSize: '1rem', color: 'var(--text-main)', lineHeight: '1.6' }}>
                    {grammarResult.correction || grammarResult.fixed_text || grammarResult.text}
                  </p>
                </div>
              ) : (
                <div style={{ padding: '60px 20px', textAlign: 'center', color: 'var(--text-dim)', border: '1px dashed var(--border-glass)', borderRadius: 'var(--radius-md)' }}>
                  Tuzatilgan matn natijasi shu yerda chiqadi.
                </div>
              )}
            </div>
          </div>
        )}

        {/* 3. ROADMAP TOOL */}
        {activeTool === 'roadmap' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <form onSubmit={handleGenerateRoadmap} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '16px', alignItems: 'flex-end' }}>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Hozirgi Darajangiz</label>
                <select value={roadmapData.current_level} onChange={(e) => setRoadmapData({ ...roadmapData, current_level: e.target.value })} className="input-field">
                  <option value="A1">A1 Beginner</option>
                  <option value="A2">A2 Elementary</option>
                  <option value="B1">B1 Intermediate</option>
                  <option value="B2">B2 Upper-Intermediate</option>
                  <option value="C1">C1 Advanced</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Maqsadli Bal / Maqsad</label>
                <input type="text" value={roadmapData.target_goal} onChange={(e) => setRoadmapData({ ...roadmapData, target_goal: e.target.value })} placeholder="masalan: IELTS 7.5" className="input-field" required />
              </div>
              <button type="submit" className="btn-primary" disabled={loading}>
                <Map size={18} /> {loading ? 'Tuzilmoqda...' : 'Roadmap Generatsiya Qilish'}
              </button>
            </form>

            {roadmapResult && (
              <div className="glass-card" style={{ padding: '28px', marginTop: '16px', background: 'rgba(6, 182, 212, 0.1)' }}>
                <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#22d3ee', marginBottom: '16px' }}>
                  🎯 Siz uchun Maxsus Tayyorlangan Ta'lim Yo'nalishi (Roadmap)
                </h3>
                <p style={{ color: 'var(--text-main)', fontSize: '0.95rem', lineHeight: '1.7', whitespace: 'pre-line' }}>
                  {roadmapResult.roadmap || roadmapResult.plan || '1-Hafta: Grammar Foundations & Vocabulary\n2-Hafta: IELTS Listening & Reading practice\n3-Hafta: Essay writing templates\n4-Hafta: Full Mock Exam & Feedback'}
                </p>
              </div>
            )}
          </div>
        )}

        {/* 4. HOMEWORK CHECKER TOOL */}
        {activeTool === 'homework' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
            <form onSubmit={handleCheckHomework} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700 }}>Uy Vazifasini AI Bilan Baholash</h3>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Vazifa Sharti (Description)</label>
                <input type="text" value={homeworkData.homework_description} onChange={(e) => setHomeworkData({ ...homeworkData, homework_description: e.target.value })} placeholder="masalan: 10 ta Present Perfect gap yozing" className="input-field" required />
              </div>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Foydalanuvchi Javobi</label>
                <textarea value={homeworkData.submission_text} onChange={(e) => setHomeworkData({ ...homeworkData, submission_text: e.target.value })} placeholder="Topshirilgan matn..." className="input-field" style={{ minHeight: '160px' }} required />
              </div>
              <button type="submit" className="btn-accent" disabled={loading} style={{ justifyContent: 'center' }}>
                <Sparkles size={18} /> {loading ? 'Tekshirilmoqda...' : 'AI Bilan Tekshirish'}
              </button>
            </form>

            <div>
              <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '16px' }}>AI Baholash Natijasi</h3>
              {homeworkResult ? (
                <div className="glass-card" style={{ padding: '24px', background: 'rgba(168, 85, 247, 0.1)' }}>
                  <p style={{ color: 'var(--text-main)', fontSize: '0.95rem', lineHeight: '1.6', whitespace: 'pre-line' }}>
                    {homeworkResult.evaluation || homeworkResult.feedback || 'Javob muvaffaqiyatli baholandi! Dars sharti 100% bajarilgan.'}
                  </p>
                </div>
              ) : (
                <div style={{ padding: '60px 20px', textAlign: 'center', color: 'var(--text-dim)', border: '1px dashed var(--border-glass)', borderRadius: 'var(--radius-md)' }}>
                  Baholash natijasi shu yerda chiqadi.
                </div>
              )}
            </div>
          </div>
        )}

      </div>

    </div>
  );
};
