import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,  // 10 saniye timeout
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
API.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = token.startsWith("Bearer ") ? token : `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Response interceptor
API.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response) {
    console.error('API Error:', error.response.status, error.response.data);
  } else {
    console.error('Network Error:', error.message);
  }
  return Promise.reject(error);
});

export default API;