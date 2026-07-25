import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { 
  Sparkles, 
  GraduationCap, 
  Building2, 
  BookOpen, 
  BrainCircuit, 
  FileCheck2, 
  ArrowRight, 
  Star, 
  Users, 
  Award,
  Zap,
  CheckCircle,
  Play
} from 'lucide-react';

export const Home = ({ setActiveTab, openAuthModal }) => {
  const [stats, setStats] = useState({ centers: 12, courses: 48, students: 1250, exams: 320 });
  const [featuredCenters, setFeaturedCenters] = useState([]);
  const [featuredCourses, setFeaturedCourses] = useState([]);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      const centersRes = await apiClient.get('/centers/?ordering=-rating');
      setFeaturedCenters(centersRes.data.results?.slice(0, 3) || centersRes.data?.slice(0, 3) || []);

      const coursesRes = await apiClient.get('/courses/');
      setFeaturedCourses(coursesRes.data.results?.slice(0, 3) || coursesRes.data?.slice(0, 3) || []);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '80px', paddingBottom: '60px' }}>
      
      {/* Hero Banner Section */}
      <section style={{ position: 'relative', paddingTop: '40px' }}>
        <div style={{ textAlign: 'center', maxWidth: '850px', margin: '0 auto' }}>
          
          <div className="badge badge-purple" style={{ marginBottom: '20px', padding: '6px 16px', fontSize: '0.85rem' }}>
            <Sparkles size={16} /> Sun'iy Intellekt Bilan Ta'lim Inqilobi V2.0
          </div>

          <h1 style={{ fontSize: '3.6rem', fontWeight: 800, lineHeight: '1.15', marginBottom: '24px' }}>
            Kelajak Ta'limi va <span className="gradient-text">IELTS Mock</span> Tizimi Bir Joyda
          </h1>

          <p style={{ fontSize: '1.15rem', color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '36px' }}>
            EDUQASH PRO — O'zbekiston bo'ylab o'quv markazlari, onlayn kurslar, AI bilan avtomatik insho tekshirish hamda real-vaqtli imtihon simulyatsiyasi integratsiya qilingan yagona platforma.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', flexWrap: 'wrap' }}>
            <button className="btn-primary" style={{ padding: '14px 28px', fontSize: '1rem' }} onClick={() => setActiveTab('exams')}>
              <FileCheck2 size={20} /> IELTS Mock Topshirish <ArrowRight size={18} />
            </button>
            <button className="btn-accent" style={{ padding: '14px 28px', fontSize: '1rem' }} onClick={() => setActiveTab('ai')}>
              <BrainCircuit size={20} /> AI Insho & Grammatika <Sparkles size={18} />
            </button>
          </div>

        </div>

        {/* Floating Quick Stats Counter */}
        <div className="glass-panel" style={{ marginTop: '60px', padding: '28px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px', textAlign: 'center' }}>
          <div>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#818cf8', fontFamily: 'var(--font-heading)' }}>{stats.centers}+</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '4px' }}>O'quv Markazlari</div>
          </div>
          <div>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#22d3ee', fontFamily: 'var(--font-heading)' }}>{stats.courses}+</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '4px' }}>Faol Kurslar</div>
          </div>
          <div>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#c084fc', fontFamily: 'var(--font-heading)' }}>{stats.students}+</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '4px' }}>Faol O'quvchilar</div>
          </div>
          <div>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#34d399', fontFamily: 'var(--font-heading)' }}>{stats.exams}+</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '4px' }}>Topshirilgan Imtihonlar</div>
          </div>
        </div>
      </section>

      {/* Featured Learning Centers Section */}
      <section>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
          <div>
            <h2 style={{ fontSize: '2rem', fontWeight: 800 }}>Mashhur O'quv Markazlari</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>Reytingi yuqori sertifikatlangan ta'lim maskanlari</p>
          </div>
          <button className="btn-secondary" onClick={() => setActiveTab('centers')}>
            Barchasini ko'rish <ArrowRight size={16} />
          </button>
        </div>

        <div className="grid-cards">
          {featuredCenters.length > 0 ? (
            featuredCenters.map((center) => (
              <div key={center.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#818cf8' }}>
                    <Building2 size={26} />
                  </div>
                  <div className="badge badge-orange" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Star size={14} fill="#fbbf24" color="#fbbf24" /> {center.rating || 5.0}
                  </div>
                </div>

                <div>
                  <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '6px' }}>{center.name}</h3>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', lineHeight: '1.5' }}>
                    {center.description || 'Ta\'lim yo\'nalishlari bo\'yicha sifatli darslar va tajribali ustozlar.'}
                  </p>
                </div>

                <div style={{ marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid var(--border-glass)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                  <span>📍 {center.address || 'Toshkent sh.'}</span>
                  <button 
                    onClick={() => setActiveTab('centers')}
                    style={{ background: 'none', border: 'none', color: '#818cf8', fontWeight: 600, cursor: 'pointer' }}
                  >
                    Batafsil
                  </button>
                </div>
              </div>
            ))
          ) : (
            [1, 2, 3].map((i) => (
              <div key={i} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <Building2 size={32} color="#818cf8" />
                <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Cambridge Education Center</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>IELTS 8.5+ natijali ustozlar bilan ingliz tili darslari.</p>
                <div className="badge badge-purple" style={{ width: 'fit-content' }}>⭐ 4.9 Reyting</div>
              </div>
            ))
          )}
        </div>
      </section>

      {/* AI Assistant Highlight Banner */}
      <section className="glass-panel" style={{ padding: '40px', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%)', position: 'relative', overflow: 'hidden' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'center' }}>
          <div>
            <div className="badge badge-cyan" style={{ marginBottom: '16px' }}>
              <BrainCircuit size={14} /> Sun'iy Intellekt Imkoniyatlari
            </div>
            <h2 style={{ fontSize: '2.4rem', fontWeight: 800, marginBottom: '16px' }}>
              Insho Yozing, <span className="gradient-text">AI Bir Sekundda</span> Baholaydi!
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '1rem', lineHeight: '1.6', marginBottom: '24px' }}>
              EDUQASH PRO AI yordamida IELTS Writing Task 1 & 2 insholaringizni grammatika, lug'at boyligi hamda koherentsiya bo'yicha tahlil qilib, IELTS Band balini bashorat qiladi.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '28px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle size={18} color="#10b981" /> IELTS Writing Task 1 & 2 uchun aniq Band Prediction
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle size={18} color="#10b981" /> Matndagi grammatik xatolarni real-vaqtda tuzatish
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.95rem' }}>
                <CheckCircle size={18} color="#10b981" /> Maqsadli balingizga mos individual AI Roadmap
              </div>
            </div>

            <button className="btn-accent" onClick={() => setActiveTab('ai')}>
              <Sparkles size={18} /> AI Yordamchini Sinab Ko'rish
            </button>
          </div>

          <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontWeight: 700, color: '#818cf8' }}>AI Essay Review Sample</span>
              <span className="badge badge-green">Predicted Band: 7.5</span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontStyle: 'italic', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '8px' }}>
              "Education plays a crucial role in modern society. Furthermore, technology enhances learning experiences..."
            </p>
            <div style={{ fontSize: '0.8rem', color: '#34d399', lineHeight: '1.5' }}>
              ✔ Excellent vocabulary cohesion.<br/>
              ✔ Advanced sentence structures used.
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};
