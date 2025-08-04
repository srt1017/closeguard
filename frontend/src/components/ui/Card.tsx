/**
 * Reusable Card component with consistent styling
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  gradient?: 'blue' | 'slate' | 'green' | 'purple' | 'none';
  padding?: 'sm' | 'md' | 'lg';
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  gradient = 'none',
  padding = 'md'
}) => {
  const baseClasses = 'rounded-xl border';
  
  const gradientClasses = {
    blue: 'bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-100',
    slate: 'bg-gradient-to-br from-slate-50 to-slate-100 border-slate-200',
    green: 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-100',
    purple: 'bg-gradient-to-br from-purple-50 to-indigo-50 border-purple-100',
    none: 'bg-white border-slate-200'
  };
  
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };
  
  const combinedClasses = `${baseClasses} ${gradientClasses[gradient]} ${paddingClasses[padding]} ${className}`;
  
  return (
    <div className={combinedClasses}>
      {children}
    </div>
  );
};