/**
 * Wizard step progress indicator component
 */

import React from 'react';
import { WizardStep } from '@/types';

interface StepIndicatorProps {
  currentStep: WizardStep;
}

export const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep }) => {
  const steps = [
    { id: 'context', label: 'Your Details', number: 1 },
    { id: 'upload', label: 'Upload & Analyze', number: 2 },
    { id: 'results', label: 'Results', number: 3 }
  ] as const;

  const getStepClasses = (stepId: WizardStep) => {
    if (currentStep === stepId) {
      return 'bg-blue-600 text-white shadow-lg scale-110';
    } else if (isStepCompleted(stepId)) {
      return 'bg-green-500 text-white';
    } else {
      return 'bg-slate-200 text-slate-500';
    }
  };

  const getStepTextClasses = (stepId: WizardStep) => {
    if (currentStep === stepId) {
      return 'text-blue-600';
    } else if (isStepCompleted(stepId)) {
      return 'text-green-600';
    } else {
      return 'text-slate-400';
    }
  };

  const isStepCompleted = (stepId: WizardStep): boolean => {
    const stepOrder = { context: 1, upload: 2, results: 3 };
    const currentOrder = stepOrder[currentStep];
    const checkOrder = stepOrder[stepId];
    return checkOrder < currentOrder;
  };

  const getConnectorClasses = (fromStep: WizardStep) => {
    return isStepCompleted(fromStep) || currentStep === 'results' 
      ? 'bg-green-500' 
      : 'bg-slate-200';
  };

  return (
    <div className="bg-white border-b border-slate-200">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex items-center justify-center">
          {steps.map((step, index) => (
            <React.Fragment key={step.id}>
              <div className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 ${getStepClasses(step.id as WizardStep)}`}>
                  {isStepCompleted(step.id as WizardStep) ? '✓' : step.number}
                </div>
                <div className="ml-3">
                  <div className={`text-sm font-medium transition-colors ${getStepTextClasses(step.id as WizardStep)}`}>
                    {step.label}
                  </div>
                </div>
              </div>
              
              {index < steps.length - 1 && (
                <div className={`w-16 h-0.5 transition-colors mx-4 ${
                  index === 0 
                    ? getConnectorClasses('context')
                    : getConnectorClasses('upload')
                }`}></div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
};