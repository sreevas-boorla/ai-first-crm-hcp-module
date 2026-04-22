import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({ baseURL: API_BASE });

// ─── HCP API ────────────────────────────────────────────────────────
export const hcpAPI = {
  getAll: (search = '') => api.get(`/hcps/${search ? `?search=${search}` : ''}`),
  getById: (id) => api.get(`/hcps/${id}`),
};

// ─── Interaction API ────────────────────────────────────────────────
export const interactionAPI = {
  getAll: (hcpId = null) => api.get(`/interactions/${hcpId ? `?hcp_id=${hcpId}` : ''}`),
  getById: (id) => api.get(`/interactions/${id}`),
  create: (data) => api.post('/interactions/', data),
  update: (id, data) => api.put(`/interactions/${id}`, data),
  delete: (id) => api.delete(`/interactions/${id}`),
};

// ─── Products API ───────────────────────────────────────────────────
export const productAPI = {
  getAll: () => api.get('/products'),
};

// ─── Agent Chat API ─────────────────────────────────────────────────
export const agentAPI = {
  chat: (message, hcpId = null) =>
    api.post('/agent/chat', { message, hcp_id: hcpId }),
};

export default api;
