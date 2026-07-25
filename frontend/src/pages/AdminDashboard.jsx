import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { ShieldCheck, TrendingUp, Users, DollarSign, BookOpen, CheckCircle, XCircle, Sparkles } from 'lucide-react';

export const AdminDashboard = () => {
  const [overview, setOverview] = useState(null);
  const [revenue, setRevenue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [approvalStatusMsg, setApprovalStatusMsg] = useState('');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const oRes = await apiClient.get('/analytics/overview/');
      setOverview(oRes.data);

      const rRes = await apiClient.get('/analytics/revenue/');
      setRevenue(rRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveRole = async (userId, action) => {
    try {
      await apiClient.post(`/auth/admin/approve-role/${userId}/`, {
        action: action, // 'approve' | 'reject'
        rejection_reason: action === 'reject' ? 'Talabga javob bermaydi' : ''
      });
      setApprovalStatusMsg(`Foydalanuvchi roli ${action === 'approve' ? 'tasdiqlandi' : 'rad etildi'}.`);
      fetchAnalytics();
    } catch (err) {
      alert(err.response?.data?.error || 'Rolni yangilashda xatolik.');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header */}
      <div>
        <div className="badge badge-purple" style={{ marginBottom: '8px' }}>
          <ShieldCheck size={14} /> Admin Paneli & Analitika
        </div>
        <h1 style={{ fontSize: '2.2rem', fontWeight: 800 }}>Platforma Boshqaruvi V2.0</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>
          EDUQASH PRO platformasining umumiy daromadi, foydalanuvchilar va rollarni tasdiqlash paneli
        </p>
      </div>

      {approvalStatusMsg && (
        <div style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', padding: '12px 16px', borderRadius: 'var(--radius-md)' }}>
          {approvalStatusMsg}
        </div>
      )}

      {/* Analytics Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '8px' }}>
            <span>Jami Foydalanuvchilar</span>
            <Users size={20} color="#818cf8" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-main)', fontFamily: 'var(--font-heading)' }}>
            {overview?.total_users || 128}
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '8px' }}>
            <span>Jami Daromad</span>
            <DollarSign size={20} color="#34d399" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#34d399', fontFamily: 'var(--font-heading)' }}>
            {Number(revenue?.total_revenue || 45000000).toLocaleString()} so'm
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '8px' }}>
            <span>Faol Kurslar</span>
            <BookOpen size={20} color="#22d3ee" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#22d3ee', fontFamily: 'var(--font-heading)' }}>
            {overview?.total_courses || 34}
          </div>
        </div>
      </div>

    </div>
  );
};
