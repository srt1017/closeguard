/**
 * Dashboard layout component for results display
 */

import React from 'react';
import { Report } from '@/types';
import { ForensicScoreCard } from './ForensicScoreCard';
import { StatisticsCards } from './StatisticsCards';
import { FlagsList } from './FlagsList';

interface DashboardLayoutProps {
  report: Report;
  onStartOver: () => void;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ report, onStartOver }) => {
  if (!report.analytics) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-600">Report data incomplete</p>
      </div>
    );
  }

  return (
    <div className="animate-in slide-in-from-bottom duration-300">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Analysis Complete</h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          We've analyzed your closing document. Here's what we found:
        </p>
      </div>

      <div className="space-y-8">
        {/* Forensic Score - Main focal point */}
        <div className="flex justify-center">
          <ForensicScoreCard score={report.analytics.forensic_score} className="max-w-md" />
        </div>

        {/* Statistics Cards */}
        <StatisticsCards analytics={report.analytics} />

        {/* Flags List */}
        <FlagsList flags={report.flags} />

        {/* Document Metadata */}
        {report.metadata && (
          <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Document Information</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium text-slate-600">Filename:</span>
                <span className="ml-2 text-slate-900">{report.metadata.filename}</span>
              </div>
              <div>
                <span className="font-medium text-slate-600">Document Size:</span>
                <span className="ml-2 text-slate-900">{report.metadata.text_length.toLocaleString()} characters</span>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-center pt-4">
          <button
            onClick={onStartOver}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Analyze Another Document
          </button>
        </div>
      </div>
    </div>
  );
};