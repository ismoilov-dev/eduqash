import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  GraduationCap, 
  BookOpen, 
  Building2, 
  BrainCircuit, 
  FileCheck2, 
  Trophy, 
  MessageSquare, 
  ShieldCheck, 
  LogOut, 
  User, 
  Bell,
  Sparkles,
  Menu,
  X
} from 'lucide-react';

export const Navbar = ({ activeTab, setActiveTab, openAuthModal, openNotifications }) => {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Bosh Sahifa', icon: GraduationCap },
    { id: 'centers', label: 'Markazlar', icon: Building2 },
    { id: 'courses', label: 'Kurslar', icon: BookOpen },
    { id: 'exams', label: 'IELTS & Imtihonlar', icon: FileCheck2 },
    { id: 'quizzes', label: 'Quiz & Reyting', icon: Trophy },
    { id: 'ai', label: 'AI Yordamchi', icon: BrainCircuit, badge: 'AI' },
    { id: 'chat', label: 'Suhbatlar', icon: MessageSquare },
  ];

  if (user?.role === 'super_admin' || user?.role === 'admin' || user?.is_staff) {
    navItems.push({ id: 'admin', label: 'Analitika', icon: ShieldCheck, badge: 'Admin' });
  }

  return (
    <header className="glass-panel" style={{ position: 'sticky', top: 0, zIndex: 50, borderRadius: 0, borderTop: 'none', borderLeft: 'none', borderRight: 'none' }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '76px' }}>
        
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('home')}
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
        >
          <div style={{
            background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)'
          }}>
            <GraduationCap size={26} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 800, fontSize: '1.4rem', letterSpacing: '-0.03em' }}>
              EDUQASH <span className="gradient-text">PRO</span>
            </div>
            <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.05em' }}>
              V2.0 PLATFORM
            </div>
          </div>
        </div>

        {/* Desktop Nav Items */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '6px' }} className="desktop-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{
                  background: isActive ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
                  color: isActive ? '#818cf8' : 'var(--text-muted)',
                  border: isActive ? '1px solid rgba(99, 102, 241, 0.3)' : '1px solid transparent',
                  padding: '8px 14px',
                  borderRadius: 'var(--radius-md)',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  fontWeight: isActive ? 600 : 500,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Icon size={18} color={isActive ? '#818cf8' : 'currentColor'} />
                {item.label}
                {item.badge && (
                  <span className="badge badge-purple" style={{ fontSize: '0.65rem', padding: '2px 6px' }}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* User Auth Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {user ? (
            <>
              {/* Notification Button */}
              <button 
                onClick={openNotifications}
                style={{
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid var(--border-glass)',
                  width: '40px',
                  height: '40px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-main)',
                  cursor: 'pointer',
                  position: 'relative'
                }}
              >
                <Bell size={20} />
                <span style={{
                  position: 'absolute',
                  top: '8px',
                  right: '8px',
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#10b981'
                }} />
              </button>

              {/* Profile Card */}
              <div 
                onClick={() => setActiveTab('profile')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '6px 14px',
                  background: 'rgba(30, 41, 59, 0.5)',
                  border: '1px solid var(--border-glass)',
                  borderRadius: 'var(--radius-full)',
                  cursor: 'pointer'
                }}
              >
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.85rem'
                }}>
                  {user.first_name?.[0] || user.username?.[0] || 'U'}
                </div>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-main)' }}>
                    {user.first_name || user.username}
                  </div>
                  <div style={{ fontSize: '0.7rem', color: '#818cf8', fontWeight: 500, textTransform: 'capitalize' }}>
                    {user.role?.replace('_', ' ')}
                  </div>
                </div>
              </div>

              <button 
                onClick={logout}
                style={{
                  background: 'rgba(239, 68, 68, 0.1)',
                  border: '1px solid rgba(239, 68, 68, 0.2)',
                  color: '#ef4444',
                  width: '38px',
                  height: '38px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer'
                }}
                title="Tizimdan chiqish"
              >
                <LogOut size={18} />
              </button>
            </>
          ) : (
            <button className="btn-primary" onClick={openAuthModal}>
              <User size={18} /> Kirish / Ro'yxatdan O'tish
            </button>
          )}
        </div>

      </div>
    </header>
  );
};
