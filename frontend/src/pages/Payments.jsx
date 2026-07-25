import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { jsPDF } from 'jspdf';
import QRCode from 'qrcode';
import { CreditCard, CheckCircle2, Award, Download, Tag, ArrowRight, ShieldCheck } from 'lucide-react';

export const Payments = () => {
  const [payments, setPayments] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  const [promoCode, setPromoCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const [promoSuccess, setPromoSuccess] = useState('');

  useEffect(() => {
    fetchPaymentsAndCertificates();
  }, []);

  const fetchPaymentsAndCertificates = async () => {
    setLoading(true);
    try {
      const pRes = await apiClient.get('/payments/');
      setPayments(pRes.data.results || pRes.data || []);

      const cRes = await apiClient.get('/certificates/');
      setCertificates(cRes.data.results || cRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyPromo = async () => {
    if (!promoCode) return;
    try {
      const res = await apiClient.post('/payments/apply-promo/', { code: promoCode });
      setDiscount(res.data.discount_percent || 20);
      setPromoSuccess(`Promokod qabul qilindi! ${res.data.discount_percent || 20}% chegirma berildi.`);
    } catch (err) {
      alert(err.response?.data?.error || 'Promokod yaroqsiz.');
    }
  };

  const downloadCertificatePDF = async (cert) => {
    const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
    
    // Background gradient style
    doc.setFillColor(11, 15, 25);
    doc.rect(0, 0, 297, 210, 'F');

    // Golden Border
    doc.setDrawColor(245, 158, 11);
    doc.setLineWidth(3);
    doc.rect(10, 10, 277, 190);

    // Title
    doc.setTextColor(248, 250, 252);
    doc.setFontSize(28);
    doc.text('EDUQASH PRO CERTIFICATE OF COMPLETION', 148, 45, { align: 'center' });

    doc.setFontSize(16);
    doc.setTextColor(148, 163, 184);
    doc.text('This is to certify that', 148, 70, { align: 'center' });

    // Student Name
    doc.setFontSize(24);
    doc.setTextColor(99, 102, 241);
    doc.text(cert.user_name || 'STUDENT NAME', 148, 90, { align: 'center' });

    doc.setFontSize(14);
    doc.setTextColor(248, 250, 252);
    doc.text(`has successfully completed the course: ${cert.title || 'IELTS Masterclass'}`, 148, 115, { align: 'center' });

    // Date & Unique ID
    doc.setFontSize(10);
    doc.setTextColor(100, 116, 139);
    doc.text(`Certificate ID: ${cert.unique_id || 'EDUQASH-2026-X912'}`, 30, 175);
    doc.text(`Issued Date: ${new Date().toLocaleDateString()}`, 30, 182);

    // Generate Verification QR Code
    try {
      const qrDataUrl = await QRCode.toDataURL(`http://169.58.72.177/certificates/verify/${cert.unique_id || 'EDUQASH-2026'}/`);
      doc.addImage(qrDataUrl, 'PNG', 230, 145, 35, 35);
    } catch (e) {
      console.error(e);
    }

    doc.save(`Certificate_${cert.unique_id || 'EDUQASH'}.pdf`);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '2.2rem', fontWeight: 800 }}>To'lovlar & Sertifikatlar</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '4px' }}>
          Tranzaksiyalar tarixi va avtomatik QR-kodli xalqaro sertifikatlarni yuklab olish
        </p>
      </div>

      {/* Main Layout: Promo + Certificates + Payment History */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '28px' }}>
        
        {/* Certificates & Promo Code */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          {/* Promo Code Box */}
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Tag size={20} color="#34d399" /> Promokodni Qo'llash
            </h3>

            {promoSuccess && (
              <div style={{ color: '#34d399', fontSize: '0.85rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={16} /> {promoSuccess}
              </div>
            )}

            <div style={{ display: 'flex', gap: '10px' }}>
              <input 
                type="text" 
                value={promoCode}
                onChange={(e) => setPromoCode(e.target.value)}
                placeholder="masalan: PROMO20"
                className="input-field"
                style={{ uppercase: 'true' }}
              />
              <button className="btn-accent" onClick={handleApplyPromo}>
                Tekshirish
              </button>
            </div>
          </div>

          {/* Certificates List */}
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Award size={22} color="#fbbf24" /> Sizning Sertifikatlaringiz ({certificates.length})
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {certificates.length > 0 ? (
                certificates.map((cert) => (
                  <div key={cert.id} className="glass-card" style={{ padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{cert.title || 'IELTS Graduation Certificate'}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>ID: {cert.unique_id || 'EDUQASH-2026'}</div>
                    </div>

                    <button 
                      className="btn-primary" 
                      style={{ padding: '8px 14px', fontSize: '0.8rem' }}
                      onClick={() => downloadCertificatePDF(cert)}
                    >
                      <Download size={14} /> PDF Yuklash
                    </button>
                  </div>
                ))
              ) : (
                <div className="glass-card" style={{ padding: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>IELTS Graduation Certificate</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>ID: EDUQASH-SAMPLE-2026</div>
                  </div>
                  <button className="btn-primary" style={{ padding: '8px 14px', fontSize: '0.8rem' }} onClick={() => downloadCertificatePDF({ title: 'IELTS Graduation Certificate', unique_id: 'EDUQASH-SAMPLE-2026' })}>
                    <Download size={14} /> PDF Yuklash
                  </button>
                </div>
              )}
            </div>
          </div>

        </div>

        {/* Payments History */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CreditCard size={22} color="#818cf8" /> To'lovlar Tarixi
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {payments.length > 0 ? (
              payments.map((p) => (
                <div key={p.id} className="glass-card" style={{ padding: '14px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{p.course_title || 'Kurs To\'lovi'}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Provayder: {p.provider?.toUpperCase()}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontWeight: 700, color: '#34d399' }}>{Number(p.amount).toLocaleString()} so'm</div>
                    <span className="badge badge-green" style={{ fontSize: '0.65rem' }}>{p.status || 'Success'}</span>
                  </div>
                </div>
              ))
            ) : (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', marginTop: '20px' }}>To'lovlar tarixi bo'sh</p>
            )}
          </div>
        </div>

      </div>

    </div>
  );
};
