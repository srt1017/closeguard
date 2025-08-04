/**
 * Formatting utilities for numbers, currency, and text
 */

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatPercentage = (value: number, decimals: number = 1): string => {
  return `${value.toFixed(decimals)}%`;
};

export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US').format(value);
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

export const getRiskLevelText = (score: number): string => {
  if (score >= 70) return 'LOW RISK';
  if (score >= 30) return 'MODERATE RISK';
  return 'HIGH RISK';
};

export const getRiskLevelColor = (score: number): string => {
  if (score >= 70) return 'text-green-600 bg-green-50 border-green-200';
  if (score >= 30) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
  return 'text-red-600 bg-red-50 border-red-200';
};