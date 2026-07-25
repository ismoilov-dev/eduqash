import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AuthModal } from './components/AuthModal';
import { NotificationCenter } from './components/NotificationCenter';

import { Home } from './pages/Home';
import { Centers } from './pages/Centers';
import { Courses } from './pages/Courses';
import { CourseDetail } from './pages/CourseDetail';
import { Exams } from './pages/Exams';
import { ExamAttempt } from './pages/ExamAttempt';
import { Quizzes } from './pages/Quizzes';
import { AiAssistant } from './pages/AiAssistant';
import { Payments } from './pages/Payments';
import { Chat } from './pages/Chat';
import { AdminDashboard } from './pages/AdminDashboard';

export function AppContent() {
  const [activeTab, setActiveTab] = useState('home');
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedExam, setSelectedExam] = useState(null);
  
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);

  const handleSelectCourse = (course) => {
    setSelectedCourse(course);
    setActiveTab('course-detail');
  };

  const handleStartExam = (exam) => {
    setSelectedExam(exam);
    setActiveTab('exam-attempt');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      
      {/* Navigation Header */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        openAuthModal={() => setIsAuthOpen(true)}
        openNotifications={() => setIsNotifOpen(true)}
      />

      {/* Main View Area */}
      <main className="container" style={{ flex: 1, paddingTop: '40px' }}>
        {activeTab === 'home' && <Home setActiveTab={setActiveTab} openAuthModal={() => setIsAuthOpen(true)} />}
        {activeTab === 'centers' && <Centers />}
        {activeTab === 'courses' && <Courses onSelectCourse={handleSelectCourse} />}
        {activeTab === 'course-detail' && selectedCourse && (
          <CourseDetail course={selectedCourse} onBack={() => setActiveTab('courses')} />
        )}
        {activeTab === 'exams' && <Exams onStartExam={handleStartExam} />}
        {activeTab === 'exam-attempt' && selectedExam && (
          <ExamAttempt exam={selectedExam} onFinish={() => setActiveTab('exams')} />
        )}
        {activeTab === 'quizzes' && <Quizzes />}
        {activeTab === 'ai' && <AiAssistant />}
        {activeTab === 'payments' && <Payments />}
        {activeTab === 'chat' && <Chat />}
        {activeTab === 'admin' && <AdminDashboard />}
      </main>

      {/* Footer */}
      <Footer />

      {/* Global Modals */}
      <AuthModal isOpen={isAuthOpen} onClose={() => setIsAuthOpen(false)} />
      <NotificationCenter isOpen={isNotifOpen} onClose={() => setIsNotifOpen(false)} />

    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
