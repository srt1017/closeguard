/**
 * Action Priority Guide component showing impact summary and critical actions
 */

import React from 'react';
import { Flag } from '@/types';
import { getLaymanExplanation } from '@/utils/explanations';
import { Card } from '@/components/ui';

interface ActionPriorityGuideProps {
  flags: Flag[];
}

export const ActionPriorityGuide: React.FC<ActionPriorityGuideProps> = ({ flags }) => {
  const flagsByImpact = flags.reduce((acc, flag) => {
    const explanation = getLaymanExplanation(flag.rule, flag.message);
    acc[explanation.impact].push(flag);
    return acc;
  }, { high: [] as Flag[], medium: [] as Flag[], low: [] as Flag[] });

  const criticalCount = flagsByImpact.high.length;
  const importantCount = flagsByImpact.medium.length;
  const minorCount = flagsByImpact.low.length;

  if (flags.length === 0) {
    return null;
  }

  return (
    <Card className="shadow-lg border border-slate-200">
      <h3 className="text-xl font-bold text-slate-900 mb-4 flex items-center">
        <svg className="w-5 h-5 text-orange-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        Action Priority Guide
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
          <div className="text-2xl font-bold text-red-600">
            {criticalCount}
          </div>
          <div className="text-sm font-medium text-red-700">Critical Issues</div>
          <div className="text-xs text-red-600 mt-1">Act immediately</div>
        </div>
        <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">
            {importantCount}
          </div>
          <div className="text-sm font-medium text-yellow-700">Important Issues</div>
          <div className="text-xs text-yellow-600 mt-1">Address soon</div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-600">
            {minorCount}
          </div>
          <div className="text-sm font-medium text-green-700">Minor Issues</div>
          <div className="text-xs text-green-600 mt-1">Review when convenient</div>
        </div>
      </div>

      {criticalCount > 0 && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <h4 className="font-semibold text-red-800 mb-2">🚨 Critical Actions Needed</h4>
          <p className="text-sm text-red-700 mb-3">
            You have {criticalCount} critical issue(s) that require immediate attention before proceeding with this closing.
          </p>
          <ul className="text-sm text-red-700 space-y-1">
            <li>• Do not sign any documents until these issues are resolved</li>
            <li>• Contact your lender immediately to discuss corrections</li>
            <li>• Consider consulting with a real estate attorney</li>
            <li>• Document all communications about these issues</li>
            <li>• You may have 60 days after closing to file TRID violation complaints</li>
          </ul>
        </div>
      )}

      {importantCount > 0 && criticalCount === 0 && (
        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h4 className="font-semibold text-yellow-800 mb-2">⚠️ Important Issues to Address</h4>
          <p className="text-sm text-yellow-700 mb-3">
            You have {importantCount} important issue(s) that should be resolved before closing.
          </p>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• Discuss these issues with your lender or real estate agent</li>
            <li>• Get written explanations for any unusual fees or terms</li>
            <li>• Compare costs with market standards</li>
            <li>• Consider delaying closing until issues are clarified</li>
          </ul>
        </div>
      )}

      {minorCount > 0 && criticalCount === 0 && importantCount === 0 && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-800 mb-2">ℹ️ Minor Issues for Review</h4>
          <p className="text-sm text-blue-700 mb-3">
            You have {minorCount} minor issue(s) that are worth reviewing but not urgent.
          </p>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Review these items when convenient</li>
            <li>• Ask questions about anything unclear</li>
            <li>• Keep documentation for future reference</li>
          </ul>
        </div>
      )}
    </Card>
  );
};