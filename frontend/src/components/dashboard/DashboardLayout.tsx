/**
 * Clean dashboard layout with organized tabs to reduce clutter
 */

import React from 'react';
import { Report, VerificationResponse } from '@/types';
import { ForensicScoreCard } from './ForensicScoreCard';
import { StatisticsCards } from './StatisticsCards';
import { FlagsList } from './FlagsList';
import { ActionPriorityGuide, CostBreakdown } from '@/components/analysis';
import { Tabs } from '@/components/ui';

interface DashboardLayoutProps {
  report: Report;
  onStartOver: () => void;
  verifications?: Record<string, VerificationResponse>;
  onVerificationResponse?: (flagRule: string, response: VerificationResponse) => void;
  showVerification?: boolean;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ 
  report, 
  onStartOver, 
  verifications = {},
  onVerificationResponse,
  showVerification = false
}) => {
  if (!report.analytics) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-600">Report data incomplete</p>
      </div>
    );
  }

  const verifiedIssuesCount = Object.keys(verifications).filter(key => verifications[key] === 'no').length;

  const tabs = [
    {
      id: 'overview',
      label: 'Overview',
      content: (
        <div className="space-y-6">
          {/* Forensic Score - Main focal point */}
          <div className="flex justify-center">
            <ForensicScoreCard score={report.analytics.forensic_score} className="max-w-md" />
          </div>

          {/* Statistics Cards */}
          <StatisticsCards analytics={report.analytics} />

          {/* Action Priority Guide - Only show if user has verified issues */}
          {showVerification && verifiedIssuesCount > 0 && (
            <ActionPriorityGuide flags={report.flags} />
          )}
        </div>
      )
    },
    {
      id: 'issues',
      label: 'Issues Found',
      badge: report.flags.length,
      content: (
        <FlagsList 
          flags={report.flags}
          verifications={verifications}
          onVerificationResponse={onVerificationResponse}
          showVerification={showVerification}
        />
      )
    },
    {
      id: 'costs',
      label: 'Cost Analysis',
      content: <CostBreakdown report={report} />
    },
    {
      id: 'details',
      label: 'Document Details',
      content: report.metadata ? (
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
      ) : (
        <div className="text-center py-8 text-slate-500">
          No document metadata available
        </div>
      )
    }
  ];

  return (
    <div className="animate-in slide-in-from-bottom duration-300">
      {/* Clean Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Analysis Complete</h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          We've analyzed your closing document. Review the results below:
        </p>
      </div>

      {/* Tabbed Content */}
      <Tabs tabs={tabs} defaultTab="overview" />

      {/* Actions - Fixed at bottom */}
      <div className="flex justify-center pt-8 mt-8 border-t border-slate-200">
        <button
          onClick={onStartOver}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Analyze Another Document
        </button>
      </div>
    </div>
  );
};