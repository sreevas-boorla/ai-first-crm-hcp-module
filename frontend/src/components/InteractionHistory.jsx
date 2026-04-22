import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchInteractions } from '../store/interactionSlice';

const SENTIMENT_COLORS = {
  Positive: '#10b981',
  Neutral: '#6366f1',
  Negative: '#ef4444',
};

export default function InteractionHistory() {
  const dispatch = useDispatch();
  const { list, loading } = useSelector((s) => s.interactions);
  const { selectedHCP } = useSelector((s) => s.hcps);

  useEffect(() => {
    dispatch(fetchInteractions(selectedHCP?.id || null));
  }, [dispatch, selectedHCP]);

  if (!selectedHCP) {
    return (
      <div className="history-panel">
        <h3>📋 Interaction History</h3>
        <p className="history-empty">Select an HCP to view their interaction history.</p>
      </div>
    );
  }

  return (
    <div className="history-panel">
      <h3>📋 Interaction History — Dr. {selectedHCP.first_name} {selectedHCP.last_name}</h3>
      {loading ? (
        <div className="history-loading"><div className="spinner" /></div>
      ) : list.length === 0 ? (
        <p className="history-empty">No interactions logged yet.</p>
      ) : (
        <div className="history-list">
          {list.map((item) => (
            <div className="history-card" key={item.id}>
              <div className="history-top">
                <span className="history-type">{item.interaction_type}</span>
                <span className="history-sentiment" style={{ color: SENTIMENT_COLORS[item.sentiment] || '#6366f1' }}>
                  ● {item.sentiment}
                </span>
              </div>
              <div className="history-date">
                {item.interaction_date ? new Date(item.interaction_date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—'}
                {' · '}{item.duration_minutes} min
              </div>
              {item.products_discussed && (
                <div className="history-products">
                  {item.products_discussed.split(',').map((p, i) => (
                    <span key={i} className="product-tag">{p.trim()}</span>
                  ))}
                </div>
              )}
              {item.ai_summary && <p className="history-summary">{item.ai_summary}</p>}
              {item.follow_up_actions && (
                <div className="history-followup">
                  <strong>Follow-up:</strong> {item.follow_up_actions}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
