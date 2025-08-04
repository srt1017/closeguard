/**
 * Statistics cards component showing report analytics
 */

import React from 'react';
import { Card } from '@/components/ui';
import { ReportAnalytics } from '@/types';
import { formatNumber } from '@/utils';

interface StatisticsCardsProps {
  analytics: ReportAnalytics;
}

export const StatisticsCards: React.FC<StatisticsCardsProps> = ({ analytics }) => {
  const getProtectionLevel = () => {
    const score = analytics.forensic_score;
    if (score < 30) return { text: '🚨 URGENT', subtext: 'Action needed', color: 'text-red-600' };
    if (score < 70) return { text: '⚠️ REVIEW', subtext: 'Monitor closely', color: 'text-yellow-600' };
    return { text: '✅ SECURE', subtext: 'Well protected', color: 'text-green-600' };
  };

  const protection = getProtectionLevel();

  return (
    <div className="grid md:grid-cols-4 gap-6">
      {/* Total Flags */}
      <Card className="shadow-lg border border-slate-200">
        <div className="flex items-center">
          <div className="p-3 rounded-lg mr-4 bg-gradient-to-br from-blue-500 to-blue-600">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L5.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Total Issues</p>
            <p className="text-2xl font-bold text-slate-900">{formatNumber(analytics.total_flags)}</p>
            <p className="text-xs text-slate-500">Found in document</p>
          </div>
        </div>
      </Card>

      {/* Critical Issues */}
      <Card className="shadow-lg border border-slate-200">
        <div className="flex items-center">
          <div className="p-3 rounded-lg mr-4 bg-gradient-to-br from-red-500 to-red-600">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L5.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Critical Issues</p>
            <p className="text-2xl font-bold text-red-600">{formatNumber(analytics.high_severity)}</p>
            <p className="text-xs text-slate-500">Immediate attention</p>
          </div>
        </div>
      </Card>

      {/* Warnings */}
      <Card className="shadow-lg border border-slate-200">
        <div className="flex items-center">
          <div className="p-3 rounded-lg mr-4 bg-gradient-to-br from-yellow-500 to-orange-500">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L5.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Warnings</p>
            <p className="text-2xl font-bold text-yellow-600">{formatNumber(analytics.medium_severity)}</p>
            <p className="text-xs text-slate-500">Review needed</p>
          </div>
        </div>
      </Card>

      {/* Protection Level */}
      <Card className="shadow-lg border border-slate-200">
        <div className="flex items-center">
          <div className={`p-3 rounded-lg mr-4 ${
            analytics.forensic_score < 30 
              ? 'bg-gradient-to-br from-red-500 to-red-600' 
              : analytics.forensic_score < 70 
              ? 'bg-gradient-to-br from-yellow-500 to-orange-500' 
              : 'bg-gradient-to-br from-green-500 to-green-600'
          }`}>
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <p className="text-sm text-slate-600 font-medium">Protection Level</p>
            <p className={`text-lg font-bold ${protection.color}`}>
              {protection.text}
            </p>
            <p className="text-xs text-slate-500">
              {protection.subtext}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};