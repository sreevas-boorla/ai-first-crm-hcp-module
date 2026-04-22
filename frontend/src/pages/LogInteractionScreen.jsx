import { useState } from 'react';
import HCPSelector from '../components/HCPSelector';
import StructuredForm from '../components/StructuredForm';
import ChatInterface from '../components/ChatInterface';
import InteractionHistory from '../components/InteractionHistory';

export default function LogInteractionScreen() {
  const [mode, setMode] = useState('form'); // 'form' or 'chat'

  return (
    <div className="log-screen">
      {/* ─── Header ─────────────────────────────────────────────── */}
      <header className="screen-header">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">⚕</span>
            <span className="logo-text">HCP CRM</span>
          </div>
          <h1>Log Interaction</h1>
        </div>
        <div className="header-right">
          <span className="powered-by">Powered by LangGraph + Groq</span>
        </div>
      </header>

      {/* ─── HCP Selection ──────────────────────────────────────── */}
      <section className="hcp-section">
        <HCPSelector />
      </section>

      {/* ─── Mode Toggle ────────────────────────────────────────── */}
      <div className="mode-toggle">
        <button
          className={`toggle-btn ${mode === 'form' ? 'active' : ''}`}
          onClick={() => setMode('form')}
        >
          <span className="toggle-icon">📋</span>
          Structured Form
        </button>
        <button
          className={`toggle-btn ${mode === 'chat' ? 'active' : ''}`}
          onClick={() => setMode('chat')}
        >
          <span className="toggle-icon">💬</span>
          AI Chat Assistant
        </button>
      </div>

      {/* ─── Main Content ───────────────────────────────────────── */}
      <div className="main-content">
        <div className="input-panel">
          {mode === 'form' ? <StructuredForm /> : <ChatInterface />}
        </div>
        <div className="sidebar-panel">
          <InteractionHistory />
        </div>
      </div>
    </div>
  );
}
