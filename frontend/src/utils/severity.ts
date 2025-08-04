/**
 * Severity utilities for analyzing flag messages
 */

import { SeverityLevel } from '@/types';

export const getSeverityIcon = (message: string): string => {
  if (message.includes('🚨') || message.includes('CRITICAL') || message.includes('ERROR') || message.includes('FRAUD')) {
    return '🚨';
  } else if (message.includes('⚠️') || message.includes('WARNING') || message.includes('DANGEROUS')) {
    return '⚠️';
  } else {
    return 'ℹ️';
  }
};

export const getSeverityLevel = (message: string): SeverityLevel => {
  if (message.includes('🚨') || message.includes('CRITICAL') || message.includes('ERROR') || message.includes('FRAUD')) {
    return 'high';
  } else if (message.includes('⚠️') || message.includes('WARNING') || message.includes('DANGEROUS') || message.includes('EXCESSIVE')) {
    return 'medium';
  } else {
    return 'low';
  }
};

export const getSeverityColor = (message: string): string => {
  const severity = getSeverityLevel(message);
  switch(severity) {
    case 'high': return 'border-red-300 bg-red-100';
    case 'medium': return 'border-yellow-300 bg-yellow-100';
    case 'low': return 'border-blue-300 bg-blue-100';
    default: return 'border-gray-300 bg-gray-100';
  }
};

export const getSeverityTextColor = (message: string): string => {
  const severity = getSeverityLevel(message);
  switch(severity) {
    case 'high': return 'text-red-700';
    case 'medium': return 'text-yellow-700';
    case 'low': return 'text-blue-700';
    default: return 'text-gray-700';
  }
};

export const getSeverityBadgeColor = (severity: SeverityLevel): string => {
  switch(severity) {
    case 'high': 
      return 'bg-red-100 text-red-800 border border-red-200';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
    case 'low':
      return 'bg-blue-100 text-blue-800 border border-blue-200';
    default:
      return 'bg-gray-100 text-gray-800 border border-gray-200';
  }
};