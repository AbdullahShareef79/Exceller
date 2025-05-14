import axios from 'axios';
import { Document } from '../types';

const API_URL = '/api/v1';

export const uploadDocument = async (file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post<Document>(
    `${API_URL}/documents`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};

export const fetchDocuments = async (): Promise<Document[]> => {
  const response = await axios.get<Document[]>(`${API_URL}/documents`);
  return response.data;
};

export const downloadDocument = async (documentId: number): Promise<void> => {
  const response = await axios.get(`${API_URL}/documents/${documentId}/download`, {
    responseType: 'blob',
  });

  // Create a download link and trigger it
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute(
    'download',
    response.headers['content-disposition']?.split('filename=')[1] ||
      'document.xlsx'
  );
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}; 