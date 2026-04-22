import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { createInteraction, fetchInteractions } from '../store/interactionSlice';

const INTERACTION_TYPES = [
  'Detail Aid', 'Sample Drop', 'Speaker Program', 'Lunch and Learn',
  'Virtual Meeting', 'Phone Call', 'Email', 'Conference', 'Other',
];

const SENTIMENTS = ['Positive', 'Neutral', 'Negative'];
const PRIORITIES = ['LOW', 'MEDIUM', 'HIGH'];

export default function StructuredForm() {
  const dispatch = useDispatch();
  const { selectedHCP } = useSelector((s) => s.hcps);
  const { successMessage } = useSelector((s) => s.interactions);
  const [products, setProducts] = useState([]);

  const [form, setForm] = useState({
    interaction_type: 'Detail Aid',
    duration_minutes: 15,
    products_discussed: '',
    key_topics: '',
    hcp_feedback: '',
    sentiment: 'Neutral',
    follow_up_actions: '',
    raw_notes: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/api/products')
      .then((r) => r.json())
      .then((data) => setProducts(data))
      .catch(() => {});
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedHCP) return alert('Please select an HCP first.');
    setSubmitting(true);
    try {
      await dispatch(createInteraction({ ...form, hcp_id: selectedHCP.id })).unwrap();
      dispatch(fetchInteractions(selectedHCP.id));
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
      setForm({
        interaction_type: 'Detail Aid',
        duration_minutes: 15,
        products_discussed: '',
        key_topics: '',
        hcp_feedback: '',
        sentiment: 'Neutral',
        follow_up_actions: '',
        raw_notes: '',
      });
    } catch (err) {
      alert('Failed to log interaction: ' + (err.message || 'Unknown error'));
    }
    setSubmitting(false);
  };

  return (
    <form className="structured-form" onSubmit={handleSubmit}>
      {showSuccess && (
        <div className="alert alert-success">✓ Interaction logged successfully!</div>
      )}

      <div className="form-row">
        <div className="form-group">
          <label>Interaction Type</label>
          <select name="interaction_type" className="form-select" value={form.interaction_type} onChange={handleChange}>
            {INTERACTION_TYPES.map((t) => (<option key={t} value={t}>{t}</option>))}
          </select>
        </div>
        <div className="form-group">
          <label>Duration (minutes)</label>
          <input type="number" name="duration_minutes" className="form-input" value={form.duration_minutes} onChange={handleChange} min={1} max={480} />
        </div>
        <div className="form-group">
          <label>Sentiment</label>
          <select name="sentiment" className="form-select" value={form.sentiment} onChange={handleChange}>
            {SENTIMENTS.map((s) => (<option key={s} value={s}>{s}</option>))}
          </select>
        </div>
      </div>

      <div className="form-group">
        <label>Products Discussed</label>
        <input type="text" name="products_discussed" className="form-input" placeholder="e.g., CardioMax, OncoShield" value={form.products_discussed} onChange={handleChange} />
        {products.length > 0 && (
          <div className="product-chips">
            {products.map((p) => (
              <button type="button" key={p.id} className={`chip ${form.products_discussed.includes(p.name) ? 'active' : ''}`}
                onClick={() => {
                  const current = form.products_discussed.split(',').map((s) => s.trim()).filter(Boolean);
                  const updated = current.includes(p.name)
                    ? current.filter((n) => n !== p.name)
                    : [...current, p.name];
                  setForm({ ...form, products_discussed: updated.join(', ') });
                }}>
                {p.name}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="form-group">
        <label>Key Topics Discussed</label>
        <textarea name="key_topics" className="form-input" rows={2} placeholder="Clinical data, dosing, safety profile..." value={form.key_topics} onChange={handleChange} />
      </div>

      <div className="form-group">
        <label>HCP Feedback / Concerns</label>
        <textarea name="hcp_feedback" className="form-input" rows={2} placeholder="What did the doctor say?" value={form.hcp_feedback} onChange={handleChange} />
      </div>

      <div className="form-group">
        <label>Follow-Up Actions</label>
        <textarea name="follow_up_actions" className="form-input" rows={2} placeholder="Send brochure, schedule follow-up call..." value={form.follow_up_actions} onChange={handleChange} />
      </div>

      <div className="form-group">
        <label>Raw Notes</label>
        <textarea name="raw_notes" className="form-input" rows={3} placeholder="Free-text notes from the meeting..." value={form.raw_notes} onChange={handleChange} />
      </div>

      <button type="submit" className="btn btn-primary btn-full" disabled={submitting || !selectedHCP}>
        {submitting ? '⏳ Logging...' : '📝 Log Interaction'}
      </button>
    </form>
  );
}
