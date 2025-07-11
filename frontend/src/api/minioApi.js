import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000', // ✅ Backend URL
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return await API.post('/upload', formData);
};

export const listFiles = async () => {
  return await API.get('/list');
};

export const deleteFile = async (filename) => {
  return await API.delete(`/delete/${filename}`);
};

export const getPresignedUrl = async (filename) => {
  return await API.get(`/get-url?filename=${filename}`);
};

export const getFileInfo = async (filename) => {
  return await API.get(`/files?filename=${filename}`);
};