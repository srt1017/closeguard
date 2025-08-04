/**
 * Refactored CloseGuard main page using extracted components and hooks
 * This is the new, clean version using our modular architecture
 */

'use client';

import React from 'react';
import { useCloseGuardApp } from '@/hooks';
import { WizardLayout, UserContextForm, FileUpload } from '@/components/wizard';
import { DashboardLayout } from '@/components/dashboard';
import { ErrorBoundary } from '@/components/ui';

export default function CloseGuardRefactored() {
  const app = useCloseGuardApp();

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
            <WizardLayout currentStep={app.currentStep}>
              {/* Context Step */}
              {app.currentStep === 'context' && (
                <ErrorBoundary>
                  <UserContextForm
                    userContext={app.userContext.userContext}
                    onUpdateContext={app.userContext.updateContext}
                    onSubmit={app.handleContextSubmit}
                  />
                </ErrorBoundary>
              )}

              {/* Upload Step */}
              {app.currentStep === 'upload' && (
                <ErrorBoundary>
                  <FileUpload
                    selectedFile={app.fileUpload.selectedFile}
                    uploading={app.isUploading}
                    error={app.fileUpload.error}
                    onFileSelect={app.fileUpload.handleFileSelect}
                    onFileDrop={app.fileUpload.handleFileDrop}
                    onDragOver={app.fileUpload.handleDragOver}
                    onUpload={app.handleUpload}
                    onBackToContext={app.handleBackToContext}
                  />
                </ErrorBoundary>
              )}

              {/* Results Step */}
              {app.currentStep === 'results' && app.report.report && (
                <ErrorBoundary>
                  <DashboardLayout
                    report={app.report.report}
                    onStartOver={app.resetApp}
                    verifications={app.verification.verifications}
                    onVerificationResponse={app.verification.setVerificationResponse}
                    showVerification={true}
                  />
                </ErrorBoundary>
              )}
            </WizardLayout>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}