/**
 * Custom hook for managing flag verification state
 */

import { useState, useCallback } from 'react';
import { VerificationState, VerificationResponse, Flag } from '@/types';

export const useVerification = () => {
  const [flagVerifications, setFlagVerifications] = useState<VerificationState>({});

  const setVerification = useCallback((flagRule: string, response: VerificationResponse) => {
    setFlagVerifications(prev => ({
      ...prev,
      [flagRule]: response
    }));
  }, []);

  const getVerification = useCallback((flagRule: string): VerificationResponse | undefined => {
    return flagVerifications[flagRule];
  }, [flagVerifications]);

  const clearVerifications = useCallback(() => {
    setFlagVerifications({});
  }, []);

  const getVerificationColor = useCallback((response: VerificationResponse): string => {
    switch (response) {
      case 'yes': return 'bg-green-100 text-green-800 border-green-300';
      case 'no': return 'bg-red-100 text-red-800 border-red-300';
      case 'unsure': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  }, []);

  const getConfirmedFlags = useCallback((flags: Flag[]): Flag[] => {
    return flags.filter(flag => flagVerifications[flag.rule] === 'no');
  }, [flagVerifications]);

  const getDismissedFlags = useCallback((flags: Flag[]): Flag[] => {
    return flags.filter(flag => flagVerifications[flag.rule] === 'yes');
  }, [flagVerifications]);

  const getUnverifiedFlags = useCallback((flags: Flag[]): Flag[] => {
    return flags.filter(flag => !flagVerifications[flag.rule] || flagVerifications[flag.rule] === 'unsure');
  }, [flagVerifications]);

  const hasVerifications = useCallback((): boolean => {
    return Object.keys(flagVerifications).length > 0;
  }, [flagVerifications]);

  const getVerificationSummary = useCallback((flags: Flag[]) => {
    const confirmed = getConfirmedFlags(flags);
    const dismissed = getDismissedFlags(flags);
    const unverified = getUnverifiedFlags(flags);

    return {
      confirmed: confirmed.length,
      dismissed: dismissed.length,
      unverified: unverified.length,
      total: flags.length,
      completionRate: flags.length > 0 ? ((confirmed.length + dismissed.length) / flags.length) * 100 : 0
    };
  }, [getConfirmedFlags, getDismissedFlags, getUnverifiedFlags]);

  const shouldShowLegalWarning = useCallback((flags: Flag[]): boolean => {
    const confirmedFlags = getConfirmedFlags(flags);
    return confirmedFlags.some(flag => 
      flag.message.toLowerCase().includes('🚨') || 
      flag.message.toLowerCase().includes('critical') ||
      flag.message.toLowerCase().includes('fraud')
    );
  }, [getConfirmedFlags]);

  return {
    flagVerifications,
    setVerification,
    getVerification,
    clearVerifications,
    getVerificationColor,
    getConfirmedFlags,
    getDismissedFlags,
    getUnverifiedFlags,
    hasVerifications,
    getVerificationSummary,
    shouldShowLegalWarning,
  };
};