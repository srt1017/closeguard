/**
 * Wizard layout component that wraps the step indicator and content
 */

import React from 'react';
import { WizardStep } from '@/types';
import { StepIndicator } from './StepIndicator';

interface WizardLayoutProps {
  currentStep: WizardStep;
  children: React.ReactNode;
}

export const WizardLayout: React.FC<WizardLayoutProps> = ({ currentStep, children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
          <StepIndicator currentStep={currentStep} />
          <div className="p-8">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};