/**
 * Forensic score display card component
 */

import React from 'react';
import { Card } from '@/components/ui';
import { formatNumber, getRiskLevelText, getRiskLevelColor } from '@/utils';

interface ForensicScoreCardProps {
  score: number;
  className?: string;
}

export const ForensicScoreCard: React.FC<ForensicScoreCardProps> = ({ score, className = '' }) => {
  const getScoreColor = () => {
    if (score < 30) return 'text-red-600';
    if (score < 70) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getIconGradient = () => {
    if (score < 30) return 'bg-gradient-to-br from-red-500 to-red-600';
    if (score < 70) return 'bg-gradient-to-br from-yellow-500 to-orange-500';
    return 'bg-gradient-to-br from-green-500 to-green-600';
  };

  return (
    <Card className={`shadow-lg border border-slate-200 ${className}`}>
      <div className="flex items-center">
        <div className={`p-3 rounded-lg mr-4 ${getIconGradient()}`}>
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div>
          <p className="text-sm text-slate-600 font-medium">Forensic Score</p>
          <p className={`text-2xl font-bold ${getScoreColor()}`}>
            {formatNumber(score)}/100
          </p>
          <p className={`text-xs font-medium ${getScoreColor()}`}>
            {getRiskLevelText(score)}
          </p>
        </div>
      </div>
    </Card>
  );
};