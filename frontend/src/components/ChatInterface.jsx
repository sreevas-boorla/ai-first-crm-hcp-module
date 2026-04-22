import { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addUserMessage, sendMessage, clearChat } from '../store/chatSlice';

export default function ChatInterface() {
  const dispatch = useDispatch();
  const { messages, loading } = useSelector((s) => s.chat);
  const { selectedHCP } = useSelector((s) => s.hcps);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || loading) return;
    dispatch(addUserMessage(text));
    dispatch(sendMessage({ message: text, hcpId: selectedHCP?.id || null }));
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-title">
          <span className="chat-icon">🤖</span>
          <span>AI CRM Assistant</span>
          <span className="chat-model">gemma2-9b-it</span>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={() => dispatch(clearChat())}>
          🗑 Clear
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-bubble ${msg.role}`}>
            <div className="bubble-avatar">
              {msg.role === 'assistant' ? '🤖' : '👤'}
            </div>
            <div className="bubble-content">
              <div className="bubble-text">{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-bubble assistant">
            <div className="bubble-avatar">🤖</div>
            <div className="bubble-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="suggested-prompts">
          {[
            'Log a meeting with the selected HCP about CardioMax',
            'Show interaction history',
            'Suggest follow-up actions',
            'Search for cardiologists',
          ].map((prompt, i) => (
            <button key={i} className="prompt-chip" onClick={() => { setInput(prompt); }}>
              {prompt}
            </button>
          ))}
        </div>
        <div className="chat-input-row">
          <textarea
            className="chat-input"
            placeholder={selectedHCP
              ? `Message about Dr. ${selectedHCP.first_name} ${selectedHCP.last_name}...`
              : 'Type a message to the AI assistant...'}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button className="btn btn-primary btn-send" onClick={handleSend} disabled={loading || !input.trim()}>
            {loading ? '⏳' : '➤'}
          </button>
        </div>
      </div>
    </div>
  );
}
