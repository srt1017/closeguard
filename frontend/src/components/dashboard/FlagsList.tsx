/**
 * Flags list component displaying detected issues with expandable details
 */

import React, { useState } from 'react';
import { Flag, VerificationResponse } from '@/types';
import { getSeverityLevel, getSeverityIcon, getSeverityColor } from '@/utils';
import { Badge } from '@/components/ui';
import { VerificationQuestion } from '@/components/verification';
import { LaymanExplanations } from '@/components/analysis';

interface FlagsListProps {
  flags: Flag[];
  title?: string;
  verifications?: Record<string, VerificationResponse>;
  onVerificationResponse?: (flagRule: string, response: VerificationResponse) => void;
  showVerification?: boolean;
  showExplanations?: boolean;
}

export const FlagsList: React.FC<FlagsListProps> = ({ 
  flags, 
  title = 'Issues Found',
  verifications = {},
  onVerificationResponse,
  showVerification = false,
  showExplanations = true
}) => {
  const [expandedFlags, setExpandedFlags] = useState<Set<string>>(new Set());

  const toggleFlag = (flagRule: string) => {
    const newExpanded = new Set(expandedFlags);
    if (newExpanded.has(flagRule)) {
      newExpanded.delete(flagRule);
    } else {
      newExpanded.add(flagRule);
    }
    setExpandedFlags(newExpanded);
  };

  if (flags.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
        <svg className="mx-auto h-12 w-12 text-green-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="text-lg font-medium text-green-900 mb-2">No Issues Found</h3>
        <p className="text-green-700">Your document appears to be clean with no detected problems.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Cleaner header with issue count */}
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-slate-900">{title}</h3>
        <span className="text-sm text-slate-500">{flags.length} issue{flags.length !== 1 ? 's' : ''} detected</span>
      </div>
      
      <div className="space-y-3">
        {flags.map((flag, index) => {
          const severity = getSeverityLevel(flag.message);
          const icon = getSeverityIcon(flag.message);
          const isExpanded = expandedFlags.has(flag.rule);
          const userResponse = verifications[flag.rule];
          
          return (
            <div
              key={`${flag.rule}-${index}`}
              className={`rounded-lg border transition-all duration-200 ${
                userResponse === 'no' 
                  ? 'border-red-300 bg-red-50'
                  : userResponse === 'yes'
                    ? 'border-green-300 bg-green-50'
                    : getSeverityColor(flag.message)
              }`}
            >
              <button
                onClick={() => toggleFlag(flag.rule)}
                className="w-full p-4 text-left focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset rounded-lg"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-1">
                    <span className="text-lg flex-shrink-0">{icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge severity={severity}>
                          {severity.toUpperCase()}
                        </Badge>
                        {userResponse && (
                          <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                            userResponse === 'no' 
                              ? 'bg-red-100 text-red-700'
                              : userResponse === 'yes'
                                ? 'bg-green-100 text-green-700'
                                : 'bg-yellow-100 text-yellow-700'
                          }`}>
                            {userResponse === 'no' ? 'Confirmed Issue' : 
                             userResponse === 'yes' ? 'Dismissed' : 
                             'Needs Review'}
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-medium text-slate-900 leading-relaxed line-clamp-2">
                        {flag.message}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-slate-500">
                      {isExpanded ? 'Hide details' : 'Show details'}
                    </span>
                    <svg
                      className={`w-4 h-4 text-slate-400 transition-transform flex-shrink-0 ${isExpanded ? 'rotate-180' : ''}`}
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </button>
              
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-slate-200/50">
                  <div className="pt-4 space-y-4">
                    {/* Verification Questions - Show first for user action */}
                    {showVerification && onVerificationResponse && (
                      <VerificationQuestion
                        flagRule={flag.rule}
                        flagMessage={flag.message}
                        currentResponse={verifications[flag.rule]}
                        onResponse={(response) => onVerificationResponse(flag.rule, response)}
                      />
                    )}

                    {/* Layman Explanations - Second priority */}
                    {showExplanations && (
                      <LaymanExplanations flag={flag} />
                    )}

                    {/* Evidence - Last, for technical reference */}
                    <details className="group">
                      <summary className="cursor-pointer text-sm font-medium text-slate-700 hover:text-slate-900">
                        📄 View document evidence
                      </summary>
                      <div className="mt-2 bg-white p-3 rounded border text-xs font-mono text-slate-600 leading-relaxed overflow-x-auto">
                        {flag.snippet}
                      </div>
                    </details>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};