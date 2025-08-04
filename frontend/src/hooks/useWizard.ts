/**
 * Custom hook for managing wizard step navigation
 */

import { useState, useCallback } from 'react';
import { WizardStep } from '@/types';

export const useWizard = (initialStep: WizardStep = 'context') => {
  const [currentStep, setCurrentStep] = useState<WizardStep>(initialStep);

  const goToStep = useCallback((step: WizardStep) => {
    setCurrentStep(step);
  }, []);

  const goToContext = useCallback(() => {
    setCurrentStep('context');
  }, []);

  const goToUpload = useCallback(() => {
    setCurrentStep('upload');
  }, []);

  const goToResults = useCallback(() => {
    setCurrentStep('results');
  }, []);

  const nextStep = useCallback(() => {
    switch (currentStep) {
      case 'context':
        setCurrentStep('upload');
        break;
      case 'upload':
        setCurrentStep('results');
        break;
      case 'results':
        // Already at final step
        break;
    }
  }, [currentStep]);

  const previousStep = useCallback(() => {
    switch (currentStep) {
      case 'results':
        setCurrentStep('upload');
        break;
      case 'upload':
        setCurrentStep('context');
        break;
      case 'context':
        // Already at first step
        break;
    }
  }, [currentStep]);

  const reset = useCallback(() => {
    setCurrentStep('context');
  }, []);

  const isFirstStep = currentStep === 'context';
  const isLastStep = currentStep === 'results';
  const canGoNext = !isLastStep;
  const canGoPrevious = !isFirstStep;

  const getStepNumber = useCallback((step: WizardStep): number => {
    switch (step) {
      case 'context': return 1;
      case 'upload': return 2;
      case 'results': return 3;
    }
  }, []);

  const getCurrentStepNumber = useCallback((): number => {
    return getStepNumber(currentStep);
  }, [currentStep, getStepNumber]);

  const getStepLabel = useCallback((step: WizardStep): string => {
    switch (step) {
      case 'context': return 'Your Situation';
      case 'upload': return 'Upload Document';
      case 'results': return 'Results';
    }
  }, []);

  const getCurrentStepLabel = useCallback((): string => {
    return getStepLabel(currentStep);
  }, [currentStep, getStepLabel]);

  const isStepActive = useCallback((step: WizardStep): boolean => {
    return currentStep === step;
  }, [currentStep]);

  const isStepCompleted = useCallback((step: WizardStep): boolean => {
    const currentStepNumber = getCurrentStepNumber();
    const stepNumber = getStepNumber(step);
    return stepNumber < currentStepNumber;
  }, [getCurrentStepNumber, getStepNumber]);

  return {
    currentStep,
    goToStep,
    goToContext,
    goToUpload,
    goToResults,
    nextStep,
    previousStep,
    reset,
    isFirstStep,
    isLastStep,
    canGoNext,
    canGoPrevious,
    getCurrentStepNumber,
    getCurrentStepLabel,
    getStepNumber,
    getStepLabel,
    isStepActive,
    isStepCompleted,
  };
};