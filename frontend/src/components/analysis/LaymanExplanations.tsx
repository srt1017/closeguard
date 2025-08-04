/**
 * Layman explanations component for user-friendly issue descriptions
 */

import React from 'react';
import { Flag } from '@/types';
import { getLaymanExplanation } from '@/utils/explanations';
import { Badge } from '@/components/ui';

interface LaymanExplanationsProps {
  flag: Flag;
}

export const LaymanExplanations: React.FC<LaymanExplanationsProps> = ({ flag }) => {
  const explanation = getLaymanExplanation(flag.rule, flag.message);

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-blue-600';
      default: return 'text-slate-600';
    }
  };

  const getImpactBadgeColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="space-y-4 mt-4">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-slate-700">Impact Level:</span>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getImpactBadgeColor(explanation.impact)}`}>
          {explanation.impact.toUpperCase()}
        </span>
      </div>

      <div className="grid gap-4">
        {/* What it means */}
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
          <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
            <svg className="w-4 h-4 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            What it means
          </h4>
          <p className="text-blue-800 text-sm">{explanation.whatItMeans}</p>
        </div>

        {/* Why it matters */}
        <div className="bg-orange-50 p-4 rounded-lg border border-orange-100">
          <h4 className="font-semibold text-orange-900 mb-2 flex items-center">
            <svg className="w-4 h-4 text-orange-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L5.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            Why it matters
          </h4>
          <p className="text-orange-800 text-sm">{explanation.whyItMatters}</p>
        </div>

        {/* What to do */}
        <div className="bg-green-50 p-4 rounded-lg border border-green-100">
          <h4 className="font-semibold text-green-900 mb-2 flex items-center">
            <svg className="w-4 h-4 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            What to do
          </h4>
          <p className="text-green-800 text-sm">{explanation.whatToDo}</p>
        </div>
      </div>
    </div>
  );
};