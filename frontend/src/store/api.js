import axios from 'axios';
import store from './index';

const api = axios.create({
  baseURL: 'http://localhost:5009/api',
});

api.interceptors.request.use((config) => {
  const token = store.state.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
