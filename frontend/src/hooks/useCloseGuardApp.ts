/**
 * Main composite hook that combines all app state management
 * This provides a single interface for components to use
 */

import { useCallback } from 'react';
import { useWizard } from './useWizard';
import { useUserContext } from './useUserContext';
import { useFileUpload } from './useFileUpload';
import { useReport } from './useReport';
import { useVerification } from './useVerification';

export const useCloseGuardApp = () => {
  const wizard = useWizard();
  const userContext = useUserContext();
  const fileUpload = useFileUpload();
  const report = useReport();
  const verification = useVerification();

  // Combined actions that involve multiple hooks
  const handleContextSubmit = useCallback(() => {
    if (userContext.isContextValid()) {
      wizard.goToUpload();
    }
  }, [userContext, wizard]);

  const handleBackToContext = useCallback(() => {
    wizard.goToContext();
  }, [wizard]);

  const handleUpload = useCallback(async () => {
    if (!fileUpload.selectedFile || !userContext.isContextValid()) {
      return;
    }

    fileUpload.setUploading(true);
    fileUpload.clearError();
    
    const analysisResult = await report.analyzeDocument(
      fileUpload.selectedFile, 
      userContext.userContext
    );

    fileUpload.setUploading(false);

    if (analysisResult) {
      wizard.goToResults();
      // Clear verifications when new report is loaded
      verification.clearVerifications();
    } else {
      // Error is already set by the report hook
      fileUpload.setError(report.error || 'Analysis failed');
    }
  }, [fileUpload, userContext, report, wizard, verification]);

  const resetApp = useCallback(() => {
    wizard.reset();
    userContext.resetContext();
    fileUpload.clearFile();
    report.clearReport();
    verification.clearVerifications();
  }, [wizard, userContext, fileUpload, report, verification]);

  const hasData = useCallback(() => {
    return userContext.userContext !== null || 
           fileUpload.selectedFile !== null || 
           report.hasReport;
  }, [userContext, fileUpload, report]);

  // Expose all hook interfaces
  return {
    // Individual hook interfaces
    wizard,
    userContext,
    fileUpload,
    report,
    verification,

    // Combined actions
    handleContextSubmit,
    handleBackToContext,
    handleUpload,
    resetApp,
    hasData,

    // Convenience getters for commonly used values
    get currentStep() { return wizard.currentStep; },
    get isUploading() { return fileUpload.uploading; },
    get hasError() { return !!(fileUpload.error || report.error); },
    get errorMessage() { return fileUpload.error || report.error; },
    get isAnalyzing() { return report.loading; },
  };
};