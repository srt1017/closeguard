/**
 * Layman explanations for flag rules and verification questions
 */

export interface LaymanExplanation {
  whatItMeans: string;
  whyItMatters: string;
  whatToDo: string;
  impact: 'low' | 'medium' | 'high';
}

export const getLaymanExplanation = (flagRule: string, flagMessage: string): LaymanExplanation => {
  const explanations: Record<string, LaymanExplanation> = {
    'high_closing_costs': {
      whatItMeans: "Your closing costs are unusually high compared to your loan amount - over 4% when most people pay 2-3%.",
      whyItMatters: "This could mean you're paying thousands more than necessary, or fees have been shifted to you that should be paid by others.",
      whatToDo: "Ask your lender for a detailed breakdown of each fee and compare with other lenders. Many fees can be negotiated or waived.",
      impact: 'medium'
    },
    'excessive_origination_percentage': {
      whatItMeans: "The lender is charging you more than 1.5% of your loan amount just to process your application - this is above typical rates.",
      whyItMatters: "On a $300,000 loan, every extra 0.5% in origination fees costs you $1,500 more. This adds up quickly.",
      whatToDo: "Shop around with other lenders. Many charge 0.5-1% or waive origination fees entirely. This fee is often negotiable.",
      impact: 'medium'
    },
    'missing_buyer_representation': {
      whatItMeans: "You don't appear to have your own real estate agent representing your interests in this transaction.",
      whyItMatters: "Without your own agent, you lack independent advocacy. The seller's agent works for them, not you.",
      whatToDo: "Consider hiring a buyer's agent for future transactions. For this one, be extra careful reviewing all terms and consider an attorney consultation.",
      impact: 'high'
    },
    'builder_captive_services': {
      whatItMeans: "The same company building your home also controls your mortgage, insurance, or title services - they're all connected.",
      whyItMatters: "When one company controls multiple services, you lose the benefit of competitive pricing and independent oversight.",
      whatToDo: "Get quotes from independent mortgage lenders, insurance agents, and title companies. Compare pricing and terms.",
      impact: 'medium'
    },
    'zero_closing_costs_deception': {
      whatItMeans: "You were likely promised 'zero closing costs' but you're actually paying substantial closing fees anyway.",
      whyItMatters: "This is a bait-and-switch tactic. You expected to pay nothing extra at closing but are being charged thousands.",
      whatToDo: "Reference your original agreement or marketing materials. Demand the builder honor their promise or explain the discrepancy in writing.",
      impact: 'high'
    },
    'loan_type_contradiction': {
      whatItMeans: "Your loan is marked as both FHA and Conventional, which is impossible - it can only be one type.",
      whyItMatters: "This is a serious document error that could affect your loan terms, insurance requirements, and future refinancing options.",
      whatToDo: "Stop the closing immediately. Demand a corrected document before signing anything. This error could have major legal implications.",
      impact: 'high'
    },
    'fha_mip_on_conventional_loan': {
      whatItMeans: "You're being charged FHA mortgage insurance on a conventional loan - these are two different loan types that don't mix.",
      whyItMatters: "You're paying for insurance you don't need and aren't eligible for. This could be hundreds of dollars monthly.",
      whatToDo: "Refuse to pay this fee. Demand immediate correction. If it's truly a conventional loan, no FHA insurance should be charged.",
      impact: 'high'
    },
    'demand_feature_on_purchase_loan': {
      whatItMeans: "Your loan includes a 'demand feature' which allows the lender to demand you pay the full balance at any time, for any reason.",
      whyItMatters: "This gives the lender tremendous power over you. They could force you to pay hundreds of thousands immediately or face foreclosure.",
      whatToDo: "Do not sign this loan. Demand removal of the demand feature. This is extremely risky for homebuyers and unnecessary for purchase loans.",
      impact: 'high'
    },
    'buyer_paying_title_insurance': {
      whatItMeans: "You're paying for Owner's Title Insurance, but in Texas, this is typically the seller's responsibility.",
      whyItMatters: "You're paying for something that should cost you nothing. This could be $800-1,500 of unnecessary expense.",
      whatToDo: "Ask why you're paying this fee when it's typically seller-paid in Texas. Request the seller cover this cost as is customary.",
      impact: 'medium'
    },
    'buyer_paying_survey_fee': {
      whatItMeans: "You're paying for a property survey, but in Texas new construction, builders typically handle and pay for this.",
      whyItMatters: "This is likely a $300-600 fee that's being shifted to you when it should be included in the builder's costs.",
      whatToDo: "Ask the builder why they're not covering the survey cost. This is typically included in new construction pricing.",
      impact: 'low'
    }
  };

  return explanations[flagRule] || {
    whatItMeans: "This flag indicates a potential issue with your closing documents that warrants closer examination.",
    whyItMatters: "Unexpected or excessive charges can cost you thousands of dollars and may indicate deceptive practices.",
    whatToDo: "Review this item carefully with your lender or real estate professional. Consider getting a second opinion if the amounts seem high.",
    impact: 'medium' as const
  };
};

export const generateVerificationQuestion = (flagRule: string, flagMessage: string): string => {
  // Generate questions where "No" confirms the issue exists
  const questions: Record<string, string> = {
    'high_closing_costs': 'Were you told your closing costs would be this high?',
    'excessive_origination_percentage': 'Did your lender clearly explain this origination fee percentage upfront?',
    'zero_closing_costs_deception': 'Did you actually receive zero closing costs as promised?',
    'builder_captive_services': 'Were you given a choice of service providers, or required to use builder-recommended ones?',
    'missing_buyer_representation': 'Did you have independent buyer agent representation throughout the transaction?',
    'loan_type_contradiction': 'Does this loan type match exactly what you applied for?',
    'fha_mip_on_conventional_loan': 'Should you be paying FHA insurance on this conventional loan?',
    'demand_feature_on_purchase_loan': 'Should your lender be able to demand full payment at any time?',
    'extreme_total_interest_percentage': 'Did you understand you would pay more in interest than the loan amount?',
    'purchase_price_mismatch': 'Is this the exact purchase price you agreed to pay?',
    'loan_amount_mismatch': 'Is this the exact loan amount you expected and applied for?'
  };

  return questions[flagRule] || 'Is this how your transaction should have worked?';
};