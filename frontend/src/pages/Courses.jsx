import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { BookOpen, Search, Filter, Plus, Video, Play, FileText, CheckCircle, X, DollarSign } from 'lucide-react';

export const Courses = ({ onSelectCourse }) => {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState(''); // '' | 'online' | 'offline'
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newCourse, setNewCourse] = useState({
    title: '',
    description: '',
    price: 0,
    type: 'online'
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCourses();
  }, [search, typeFilter]);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      let params = [];
      if (search) params.push(`search=${encodeURIComponent(search)}`);
      if (typeFilter) params.push(`type=${typeFilter}`);
      const queryString = params.length ? `?${params.join('&')}` : '';
      
      const res = await apiClient.get(`/courses/${queryString}`);
      setCourses(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await apiClient.post('/courses/', newCourse);
      setIsModalOpen(false);
      fetchCourses();
    } catch (err) {
      setError(err.response?.data?.error || 'Kurs yaratishda xatolik yuz berdi.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', fontWeight: 800 }}>Onlayn & Offlayn Kurslar</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>
            Tajribali o'qituvchilar va IT/IELTS mutaxassislari tomonidan tayyorlangan darslar
          </p>
        </div>

        {(user?.role === 'teacher' || user?.role === 'admin' || user?.role === 'super_admin') && (
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={18} /> Yangi Kurs Qo'shish
          </button>
        )}
      </div>

      {/* Filter Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: '280px' }}>
          <Search size={20} color="var(--text-muted)" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
          <input 
            type="text" 
            value={search} 
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Kurs nomi bo'yicha qidiruv..." 
            className="input-field" 
            style={{ paddingLeft: '48px' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          {[
            { id: '', label: 'Barcha Kurslar' },
            { id: 'online', label: '🌐 Onlayn' },
            { id: 'offline', label: '🏢 Offlayn' },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setTypeFilter(t.id)}
              style={{
                background: typeFilter === t.id ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.03)',
                border: typeFilter === t.id ? '1px solid #818cf8' : '1px solid var(--border-glass)',
                color: typeFilter === t.id ? '#818cf8' : 'var(--text-muted)',
                padding: '10px 18px',
                borderRadius: 'var(--radius-md)',
                fontWeight: 600,
                cursor: 'pointer',
                fontSize: '0.88rem'
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Course Cards Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>Yuklanmoqda...</div>
      ) : courses.length === 0 ? (
        <div className="glass-panel" style={{ padding: '60px', textAlign: 'center', color: 'var(--text-dim)' }}>
          <BookOpen size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
          <h3>Kurslar topilmadi</h3>
        </div>
      ) : (
        <div className="grid-cards">
          {courses.map((course) => (
            <div key={course.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className={course.type === 'online' ? 'badge badge-purple' : 'badge badge-cyan'}>
                  {course.type === 'online' ? '🌐 Onlayn Kurs' : '🏢 Offlayn Kurs'}
                </span>
                <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#34d399', fontFamily: 'var(--font-heading)' }}>
                  {course.price > 0 ? `${Number(course.price).toLocaleString()} so'm` : 'Bepul'}
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '8px' }}>{course.title}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: '1.5' }}>
                  {course.description || 'Kurs darslari va videolari bilan bilimingizni oshiring.'}
                </p>
              </div>

              <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--border-glass)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                  👨‍🏫 {course.teacher_name || 'O\'qituvchi'}
                </div>

                <button 
                  className="btn-primary" 
                  style={{ padding: '8px 16px', fontSize: '0.85rem' }}
                  onClick={() => onSelectCourse(course)}
                >
                  <Play size={14} /> Darslarni Ko'rish
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal for Creating Course */}
      {isModalOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px', padding: '32px', position: 'relative' }}>
            <button onClick={() => setIsModalOpen(false)} style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
              <X size={24} />
            </button>

            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '20px' }}>Yangi Kurs Yaratish</h2>

            {error && (
              <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171', padding: '10px 14px', borderRadius: 'var(--radius-md)', fontSize: '0.85rem', marginBottom: '16px' }}>
                {error}
              </div>
            )}

            <form onSubmit={handleCreateCourse} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Kurs Sarlavhasi</label>
                <input type="text" value={newCourse.title} onChange={(e) => setNewCourse({ ...newCourse, title: e.target.value })} placeholder="masalan: IELTS 8.0 Masterclass" className="input-field" required />
              </div>

              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Kurs Tavsifi</label>
                <textarea value={newCourse.description} onChange={(e) => setNewCourse({ ...newCourse, description: e.target.value })} placeholder="Kurs haqida qisqacha..." className="input-field" style={{ minHeight: '80px' }} />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Narxi (so'm)</label>
                  <input type="number" value={newCourse.price} onChange={(e) => setNewCourse({ ...newCourse, price: Number(e.target.value) })} className="input-field" required />
                </div>
                <div>
                  <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Kurs Turi</label>
                  <select value={newCourse.type} onChange={(e) => setNewCourse({ ...newCourse, type: e.target.value })} className="input-field">
                    <option value="online">🌐 Onlayn</option>
                    <option value="offline">🏢 Offlayn</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '12px' }}>
                Kursni Saqlash
              </button>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
