/**
 * Reusable Badge component for severity indicators
 */

import React from 'react';
import { SeverityLevel } from '@/types';
import { getSeverityBadgeColor } from '@/utils/severity';

interface BadgeProps {
  severity: SeverityLevel;
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  severity,
  children,
  className = ''
}) => {
  const baseClasses = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium';
  const severityClasses = getSeverityBadgeColor(severity);
  
  return (
    <span className={`${baseClasses} ${severityClasses} ${className}`}>
      {children}
    </span>
  );
};