import React from 'react';
import { GraduationCap, Heart, Send, Globe, Mail, Phone } from 'lucide-react';

export const Footer = () => {
  return (
    <footer style={{ marginTop: '80px', borderTop: '1px solid var(--border-glass)', background: 'var(--bg-secondary)', padding: '60px 0 30px 0' }}>
      <div className="container">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '40px', marginBottom: '40px' }}>
          
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <GraduationCap size={28} color="#818cf8" />
              <span style={{ fontFamily: 'var(--font-heading)', fontWeight: 800, fontSize: '1.4rem' }}>
                EDUQASH <span className="gradient-text">PRO</span>
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
              O'zbekistondagi eng zamonaviy va intellektual ta'lim platformasi. AI yordamida IELTS Mock, onlayn va offlayn ta'lim hamda real-vaqtli muloqot tizimi.
            </p>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-main)', marginBottom: '16px', fontSize: '1.1rem' }}>Platforma Xizmatlari</h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              <li>• O'quv Markazlari Katalogi</li>
              <li>• Onlayn va Offlayn Kurslar</li>
              <li>• IELTS Mock & CEFR Imtihonlar</li>
              <li>• AI Essay Checker & Grammar Fixer</li>
              <li>• QR-kodli Xalqaro Sertifikatlar</li>
            </ul>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-main)', marginBottom: '16px', fontSize: '1.1rem' }}>Bog'lanish va Telegram Bot</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Send size={18} color="#06b6d4" /> Telegram Bot: <a href="https://t.me/eduqash_bot" target="_blank" rel="noreferrer" style={{ color: '#818cf8', textDecoration: 'none' }}>@eduqash_bot</a>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Mail size={18} color="#a855f7" /> Email: support@eduqash.uz
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Phone size={18} color="#10b981" /> Qo'llab-quvvatlash: +998 (71) 200-00-00
              </div>
            </div>
          </div>

        </div>

        <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '24px', textAlign: 'center', fontSize: '0.85rem', color: 'var(--text-dim)' }}>
          © 2026 EDUQASH PRO V2.0. Barcha huquqlar himoyalangan. Ishlab chiqildi: <span style={{ color: '#818cf8', fontWeight: 600 }}>DeepMind Agentic AI Team</span>
        </div>
      </div>
    </footer>
  );
};
