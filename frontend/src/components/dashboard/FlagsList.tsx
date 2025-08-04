/**
 * Flags list component displaying detected issues with expandable details
 */

import React, { useState } from 'react';
import { Flag } from '@/types';
import { getSeverityLevel, getSeverityIcon, getSeverityColor } from '@/utils';
import { Badge } from '@/components/ui';

interface FlagsListProps {
  flags: Flag[];
  title?: string;
}

export const FlagsList: React.FC<FlagsListProps> = ({ flags, title = 'Issues Found' }) => {
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
      <h3 className="text-xl font-semibold text-slate-900">{title}</h3>
      
      <div className="space-y-3">
        {flags.map((flag, index) => {
          const severity = getSeverityLevel(flag.message);
          const icon = getSeverityIcon(flag.message);
          const isExpanded = expandedFlags.has(flag.rule);
          
          return (
            <div
              key={`${flag.rule}-${index}`}
              className={`rounded-lg border-2 transition-all duration-200 ${getSeverityColor(flag.message)}`}
            >
              <button
                onClick={() => toggleFlag(flag.rule)}
                className="w-full p-4 text-left focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    <span className="text-lg flex-shrink-0 mt-0.5">{icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge severity={severity}>
                          {severity.toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-sm font-medium text-slate-900 leading-relaxed">
                        {flag.message}
                      </p>
                    </div>
                  </div>
                  <svg
                    className={`w-5 h-5 text-slate-400 transition-transform flex-shrink-0 ml-2 ${isExpanded ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>
              
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-slate-200 bg-slate-50/50">
                  <div className="pt-3">
                    <h4 className="text-sm font-medium text-slate-700 mb-2">Evidence from document:</h4>
                    <div className="bg-white p-3 rounded border text-xs font-mono text-slate-600 leading-relaxed overflow-x-auto">
                      {flag.snippet}
                    </div>
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