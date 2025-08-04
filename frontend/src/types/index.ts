/**
 * Core type definitions for CloseGuard frontend
 */

export interface Flag {
  rule: string;
  message: string;
  snippet: string;
}

export interface ReportAnalytics {
  forensic_score: number;
  total_flags: number;
  high_severity: number;
  medium_severity: number;
  low_severity: number;
}

export interface ReportMetadata {
  filename: string;
  text_length: number;
}

export interface Report {
  status: string;
  flags: Flag[];
  analytics?: ReportAnalytics;
  metadata?: ReportMetadata;
}

export interface UserContext {
  // Basic loan expectations
  expectedLoanType: 'FHA' | 'Conventional' | 'VA' | 'USDA' | 'Not sure';
  expectedInterestRate?: number;
  expectedClosingCosts?: number;
  
  // Purchase details
  expectedPurchasePrice?: number;
  expectedLoanAmount?: number;
  
  // Promises made by builder/lender
  promisedZeroClosingCosts: boolean;
  promisedLenderCredit?: number;
  promisedSellerCredit?: number;
  promisedRebate?: number;
  
  // Builder/lender relationships
  usedBuildersPreferredLender: boolean;
  builderName?: string;
  
  // Specific promises about fees
  builderPromisedToCoverTitleFees: boolean;
  builderPromisedToCoverEscrowFees: boolean;
  builderPromisedToCoverInspection: boolean;
  
  // Representation
  hadBuyerAgent: boolean;
  buyerAgentName?: string;
  
  // Mortgage insurance expectations
  expectedMortgageInsurance: boolean;
  expectedMortgageInsuranceAmount?: number;
}

export type WizardStep = 'context' | 'upload' | 'results';

export type VerificationResponse = 'yes' | 'no' | 'unsure';

export type SeverityLevel = 'high' | 'medium' | 'low';

export interface VerificationState {
  [flagRule: string]: VerificationResponse;
}