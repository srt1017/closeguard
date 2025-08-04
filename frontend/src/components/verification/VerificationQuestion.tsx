/**
 * Verification question component for confirming or dismissing flags
 */

import React from 'react';
import { VerificationResponse } from '@/types';
import { generateVerificationQuestion } from '@/utils/explanations';

interface VerificationQuestionProps {
  flagRule: string;
  flagMessage: string;
  currentResponse?: VerificationResponse;
  onResponse: (response: VerificationResponse) => void;
}

export const VerificationQuestion: React.FC<VerificationQuestionProps> = ({
  flagRule,
  flagMessage,
  currentResponse,
  onResponse
}) => {
  const question = generateVerificationQuestion(flagRule, flagMessage);

  const getButtonStyle = (responseType: VerificationResponse) => {
    const isSelected = currentResponse === responseType;
    
    const baseClasses = 'px-4 py-2 text-sm font-medium rounded-lg border-2 transition-all';
    
    if (isSelected) {
      switch (responseType) {
        case 'yes':
          return `${baseClasses} bg-green-100 text-green-800 border-green-300`;
        case 'no':
          return `${baseClasses} bg-red-100 text-red-800 border-red-300`;
        case 'unsure':
          return `${baseClasses} bg-yellow-100 text-yellow-800 border-yellow-300`;
      }
    }
    
    return `${baseClasses} bg-white text-slate-700 border-slate-300 hover:border-slate-400`;
  };

  const getFeedbackMessage = () => {
    switch (currentResponse) {
      case 'no':
        return (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm font-medium text-red-800">
              🚨 Issue Confirmed: This indicates a potential violation that may warrant further investigation or legal consultation.
            </p>
          </div>
        );
      case 'yes':
        return (
          <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm font-medium text-green-800">
              ✅ Issue Dismissed: This appears to be a false positive for your specific situation.
            </p>
          </div>
        );
      case 'unsure':
        return (
          <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm font-medium text-yellow-800">
              ⚠️ Needs Review: Consider consulting with a professional to clarify this issue.
            </p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
      <div className="mb-3">
        <p className="font-medium text-sm text-blue-800 mb-2">🔍 Verification Question:</p>
        <p className="text-sm text-blue-700 mb-4">
          {question}
        </p>
      </div>
      
      <div className="flex flex-wrap gap-3">
        <button 
          onClick={() => onResponse('yes')}
          className={getButtonStyle('yes')}
        >
          ✓ Yes {currentResponse === 'yes' && '(Dismisses Issue)'}
        </button>
        <button 
          onClick={() => onResponse('no')}
          className={getButtonStyle('no')}
        >
          ✗ No {currentResponse === 'no' && '(Confirms Issue)'}
        </button>
        <button 
          onClick={() => onResponse('unsure')}
          className={getButtonStyle('unsure')}
        >
          ? Unsure
        </button>
      </div>
      
      {getFeedbackMessage()}
    </div>
  );
};