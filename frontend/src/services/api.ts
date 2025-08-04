/**
 * API service layer for CloseGuard frontend
 */

import { Report, UserContext } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

export const api = {
  /**
   * Upload PDF file with user context for analysis
   */
  async uploadDocument(file: File, context: UserContext): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('context', JSON.stringify(context));

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Upload failed');
      throw new ApiError(errorText, response.status);
    }

    const result = await response.json();
    return result.report_id;
  },

  /**
   * Get analysis report by ID
   */
  async getReport(reportId: string): Promise<Report> {
    const response = await fetch(`${API_BASE_URL}/report/${reportId}`);
    
    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Failed to get report');
      throw new ApiError(errorText, response.status);
    }

    return response.json();
  },

  /**
   * Delete a report
   */
  async deleteReport(reportId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/report/${reportId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Failed to delete report');
      throw new ApiError(errorText, response.status);
    }
  },

  /**
   * Get list of all reports (admin endpoint)
   */
  async listReports(): Promise<{ reports: string[]; count: number }> {
    const response = await fetch(`${API_BASE_URL}/reports`);
    
    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Failed to list reports');
      throw new ApiError(errorText, response.status);
    }

    return response.json();
  },

  /**
   * Get API health status
   */
  async getHealth(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Health check failed');
      throw new ApiError(errorText, response.status);
    }

    return response.json();
  }
};