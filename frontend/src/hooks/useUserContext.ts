/**
 * Custom hook for managing user context state
 */

import { useState, useCallback } from 'react';
import { UserContext } from '@/types';

const DEFAULT_USER_CONTEXT: UserContext = {
  expectedLoanType: 'Not sure',
  promisedZeroClosingCosts: false,
  usedBuildersPreferredLender: false,
  builderPromisedToCoverTitleFees: false,
  builderPromisedToCoverEscrowFees: false,
  builderPromisedToCoverInspection: false,
  hadBuyerAgent: false,
  expectedMortgageInsurance: false,
};

export const useUserContext = () => {
  const [userContext, setUserContext] = useState<UserContext>(DEFAULT_USER_CONTEXT);

  const updateContext = useCallback((updates: Partial<UserContext>) => {
    setUserContext(prev => ({ ...prev, ...updates }));
  }, []);

  const resetContext = useCallback(() => {
    setUserContext(DEFAULT_USER_CONTEXT);
  }, []);

  const updateField = useCallback(<K extends keyof UserContext>(
    field: K, 
    value: UserContext[K]
  ) => {
    setUserContext(prev => ({ ...prev, [field]: value }));
  }, []);

  // Validation helpers
  const isContextValid = useCallback(() => {
    // Basic validation - can be extended based on requirements
    return userContext.expectedLoanType !== undefined;
  }, [userContext]);

  const getContextSummary = useCallback(() => {
    const summary: string[] = [];
    
    if (userContext.expectedPurchasePrice) {
      summary.push(`Purchase Price: $${userContext.expectedPurchasePrice.toLocaleString()}`);
    }
    
    if (userContext.expectedLoanAmount) {
      summary.push(`Loan Amount: $${userContext.expectedLoanAmount.toLocaleString()}`);
    }
    
    if (userContext.promisedZeroClosingCosts) {
      summary.push('Promised zero closing costs');
    }
    
    if (userContext.usedBuildersPreferredLender) {
      summary.push('Used builder\'s preferred lender');
    }
    
    return summary;
  }, [userContext]);

  return {
    userContext,
    setUserContext,
    updateContext,
    updateField,
    resetContext,
    isContextValid,
    getContextSummary,
  };
};