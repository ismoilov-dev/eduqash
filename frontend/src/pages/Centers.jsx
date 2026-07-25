import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Building2, Search, Star, Phone, Send, MapPin, Plus, X, CheckCircle2 } from 'lucide-react';

export const Centers = () => {
  const { user } = useAuth();
  const [centers, setCenters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const [newCenter, setNewCenter] = useState({
    name: '',
    description: '',
    address: '',
    phone: '',
    telegram: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchCenters();
  }, [search]);

  const fetchCenters = async () => {
    setLoading(true);
    try {
      const url = search ? `/centers/?search=${encodeURIComponent(search)}` : '/centers/';
      const res = await apiClient.get(url);
      setCenters(res.data.results || res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCenter = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await apiClient.post('/centers/', newCenter);
      setSuccess('Yangi o\'quv markazi muvaffaqiyatli yaratildi!');
      setIsModalOpen(false);
      fetchCenters();
    } catch (err) {
      setError(err.response?.data?.error || 'Markaz yaratishda xatolik yuz berdi.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header & Controls */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', fontWeight: 800 }}>O'quv Markazlari Kataloq</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>
            O'zbekistondagi eng nufuzli ta'lim markazlari bilan tanishing
          </p>
        </div>

        {(user?.role === 'center_owner' || user?.role === 'admin' || user?.role === 'super_admin') && (
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            <Plus size={18} /> Yangi Markaz Qo'shish
          </button>
        )}
      </div>

      {/* Search Input */}
      <div style={{ position: 'relative', maxWidth: '450px' }}>
        <Search size={20} color="var(--text-muted)" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
        <input 
          type="text" 
          value={search} 
          onChange={(e) => setSearch(e.target.value)}
          placeholder="O'quv markazi nomi yoki manzilini qidirish..." 
          className="input-field" 
          style={{ paddingLeft: '48px' }}
        />
      </div>

      {/* Centers Cards Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>Yuklanmoqda...</div>
      ) : centers.length === 0 ? (
        <div className="glass-panel" style={{ padding: '60px', textAlign: 'center', color: 'var(--text-dim)' }}>
          <Building2 size={48} style={{ opacity: 0.3, marginBottom: '16px' }} />
          <h3>Hech qanday o'quv markazi topilmadi</h3>
        </div>
      ) : (
        <div className="grid-cards">
          {centers.map((center) => (
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
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '8px', color: 'var(--text-main)' }}>{center.name}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: '1.5' }}>
                  {center.description || 'Ta\'lim yo\'nalishlari va professional darslar.'}
                </p>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--border-glass)' }}>
                {center.address && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <MapPin size={16} color="#818cf8" /> {center.address}
                  </div>
                )}
                {center.phone && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Phone size={16} color="#10b981" /> {center.phone}
                  </div>
                )}
                {center.telegram && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Send size={16} color="#06b6d4" /> Telegram: {center.telegram}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal for Creating New Learning Center */}
      {isModalOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '500px', padding: '32px', position: 'relative' }}>
            
            <button onClick={() => setIsModalOpen(false)} style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
              <X size={24} />
            </button>

            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '20px' }}>Yangi O'quv Markazi Qo'shish</h2>

            {error && (
              <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171', padding: '10px 14px', borderRadius: 'var(--radius-md)', fontSize: '0.85rem', marginBottom: '16px' }}>
                {error}
              </div>
            )}

            <form onSubmit={handleCreateCenter} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Markaz Nomi</label>
                <input type="text" value={newCenter.name} onChange={(e) => setNewCenter({ ...newCenter, name: e.target.value })} placeholder="masalan: Real Science IT Academy" className="input-field" required />
              </div>

              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Tavsif / Ma'lumot</label>
                <textarea value={newCenter.description} onChange={(e) => setNewCenter({ ...newCenter, description: e.target.value })} placeholder="O'quv markazining afzalliklari..." className="input-field" style={{ minHeight: '80px', resize: 'vertical' }} />
              </div>

              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Manzil</label>
                <input type="text" value={newCenter.address} onChange={(e) => setNewCenter({ ...newCenter, address: e.target.value })} placeholder="Toshkent sh., Yunusobod t." className="input-field" required />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Telefon</label>
                  <input type="text" value={newCenter.phone} onChange={(e) => setNewCenter({ ...newCenter, phone: e.target.value })} placeholder="+998 90 123 45 67" className="input-field" />
                </div>
                <div>
                  <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '4px', display: 'block' }}>Telegram Username</label>
                  <input type="text" value={newCenter.telegram} onChange={(e) => setNewCenter({ ...newCenter, telegram: e.target.value })} placeholder="@center_admin" className="input-field" />
                </div>
              </div>

              <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '12px' }}>
                Saqlash va Yaratish
              </button>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
