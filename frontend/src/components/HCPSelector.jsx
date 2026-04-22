import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchHCPs, selectHCP } from '../store/hcpSlice';

export default function HCPSelector() {
  const dispatch = useDispatch();
  const { list, selectedHCP, loading } = useSelector((s) => s.hcps);

  useEffect(() => {
    dispatch(fetchHCPs());
  }, [dispatch]);

  return (
    <div className="hcp-selector">
      <label htmlFor="hcp-select">Select Healthcare Professional</label>
      <select
        id="hcp-select"
        className="form-select"
        value={selectedHCP?.id || ''}
        onChange={(e) => {
          const hcp = list.find((h) => h.id === parseInt(e.target.value));
          dispatch(selectHCP(hcp || null));
        }}
        disabled={loading}
      >
        <option value="">— Choose an HCP —</option>
        {list.map((hcp) => (
          <option key={hcp.id} value={hcp.id}>
            Dr. {hcp.first_name} {hcp.last_name} — {hcp.specialty} ({hcp.institution})
          </option>
        ))}
      </select>
      {selectedHCP && (
        <div className="hcp-info-card">
          <div className="hcp-name">Dr. {selectedHCP.first_name} {selectedHCP.last_name}</div>
          <div className="hcp-details">
            <span className="hcp-tag specialty">{selectedHCP.specialty}</span>
            <span className="hcp-tag institution">{selectedHCP.institution}</span>
            <span className={`hcp-tag tier tier-${selectedHCP.tier?.toLowerCase()}`}>Tier {selectedHCP.tier}</span>
          </div>
          {selectedHCP.city && (
            <div className="hcp-location">📍 {selectedHCP.city}, {selectedHCP.state}</div>
          )}
        </div>
      )}
    </div>
  );
}
