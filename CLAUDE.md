# CloseGuard - AI-Powered Real Estate Closing Document Fraud Detection System

## Project Overview

CloseGuard is a web application that analyzes home closing documents to detect predatory lending practices, fraud, and deceptive cost-shifting. Built for Texas homebuyers, it combines pattern matching with forensic scoring to identify violations and provide legal guidance. The system uses a FastAPI backend for document analysis and a Next.js frontend with a multi-step wizard interface.

## Architecture Overview

### Backend (FastAPI + Python)
- **Location**: `/backend/`
- **Core**: FastAPI with modular service architecture
- **Processing**: pdfplumber for PDF extraction, YAML-based rule engine
- **Key Services**: Rule engine, document parser, scoring service, validation

### Frontend (Next.js + TypeScript)
- **Location**: `/frontend/`
- **Framework**: Next.js 15 with TypeScript and Tailwind CSS
- **Architecture**: Modular components organized by feature area
- **State**: Custom hooks for specialized state management

## Development Guidelines

### Making Changes - Follow This Order
1. **Identify the component/service** affected by the change
2. **Check existing patterns** in similar components before creating new approaches
3. **Update types first** in `/frontend/src/types/index.ts` if data structures change
4. **Update backend models** in `/backend/models/` if API changes
5. **Follow the modular architecture** - don't bypass the organized structure

### Common Development Tasks

#### Adding New Fraud Detection Rules
1. Add rule to `rules-config.yaml` with proper type and thresholds
2. If new rule type needed, create class in `/backend/rules/`
3. Update TypeScript types if new flag structure needed

#### Modifying UI Components
1. Locate component in `/frontend/src/components/[feature]/`
2. Check if state management in related hook needs updates
3. Follow existing component patterns and prop interfaces

#### Backend API Changes
1. Update endpoint in `main.py`
2. Update Pydantic models in `/backend/models/`
3. Update frontend API service in `/frontend/src/services/api.ts`
4. Update TypeScript types to match new API structure

#### Adding New Analysis Features
1. **Backend**: Create service in `/backend/services/` → Update rule engine
2. **Frontend**: Create hook in `/frontend/src/hooks/` → Create UI component
3. **Integration**: Update API service → Update main app state

## Key Files for Development

### Backend (Python/FastAPI)
- `rules-config.yaml` - All fraud detection rules (modify here first)
- `services/rule_engine.py` - Core rule processing logic
- `services/scoring_service.py` - Forensic score calculations
- `models/` - Pydantic data structures (update when changing APIs)
- `main.py` - API endpoints and FastAPI app configuration

### Frontend (Next.js/TypeScript)  
- `src/types/index.ts` - All TypeScript interfaces (update first for data changes)
- `src/hooks/useCloseGuardApp.ts` - Main app state management
- `src/components/[feature]/` - Components organized by feature area
- `src/services/api.ts` - Backend communication layer
- `src/utils/explanations.ts` - Layman explanations for detected issues

### Rule Processing Architecture
```
rules-config.yaml → Rule classes in /backend/rules/ → Services in /backend/services/ → API endpoints → Frontend hooks → UI components
```

## Code Change Guidelines - CRITICAL

### Before Making Any Changes
- **Understand the existing pattern** - Look at similar components/services first
- **Make minimal changes** - Don't refactor unless specifically needed
- **Follow the modular structure** - Don't bypass organized directories
- **Check TypeScript types** - Ensure data structures match between frontend/backend

### What NOT to Do
- ❌ Don't add new dependencies without justification
- ❌ Don't bypass the organized component structure
- ❌ Don't modify multiple unrelated files in one change
- ❌ Don't ignore TypeScript errors or add `any` types
- ❌ Don't hardcode values that should be configurable in rules-config.yaml
- ❌ Don't add random optimizations without understanding root cause
- ❌ Don't add complexity to solve simple configuration issues

### Problem-Solving Approach
1. **Identify root cause** through logs, error messages, systematic testing
2. **Try simple solutions first**: Configuration, settings, environment variables
3. **Only code when infrastructure solutions are insufficient**
4. **Keep changes minimal and focused**

## Core Features Overview

### 1. Forensic Score Dashboard
- 0-100 scoring system with risk categorization (HIGH/MODERATE/LOW)
- Statistics cards showing total flags, critical issues, protection level
- Color-coded indicators based on severity

### 2. Context-Aware Document Analysis
- User questionnaire captures expectations and promises
- Enhanced detection based on user context vs document reality
- Context comparison rules for broken promises

### 3. Interactive Verification System
- Smart Yes/No/Unsure questions for each detected flag
- Color-coded responses with legal guidance
- Confirmation logic where "No" answers confirm issues exist

### 4. Texas Cost Breakdown Analysis
- Line-by-line cost examination with payment responsibility
- Unexpected charge detection for seller/builder-paid items
- Market comparison with typical cost ranges

### 5. Layman Explanations System
- Plain English explanations for every red flag
- Three-part structure: What it means, Why it matters, What to do
- Impact prioritization with action guidance

## Rule Engine Types

The system supports multiple rule types in `rules-config.yaml`:

- `numeric_threshold`: Dollar amount limits
- `calculated_percentage`: Ratio-based detection (e.g., origination fee %)
- `regex_presence`: Pattern detection in document text
- `regex_absence`: Missing required patterns
- `compound_rule`: Multiple conditions must be met
- `cross_reference_pattern`: Related field matching
- `context_comparison`: User expectation vs document reality

## File Structure (Key Development Areas)

```
mortgagebuddy/
├── backend/
│   ├── models/              # Pydantic data models
│   ├── rules/               # Rule processing modules  
│   ├── services/            # Business logic services
│   ├── main.py             # FastAPI application
│   └── rules-config.yaml   # Rule definitions
├── frontend/src/
│   ├── components/         # Modular React components
│   │   ├── analysis/       # Document analysis UI
│   │   ├── dashboard/      # Results dashboard
│   │   ├── ui/            # Reusable UI components
│   │   ├── verification/   # Interactive verification
│   │   └── wizard/        # Multi-step wizard
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API communication
│   ├── types/             # TypeScript definitions
│   └── utils/             # Utility functions
└── testfiles/             # Sample documents for testing
```

## Development Workflow

### Typical Change Process
1. **Identify affected area** (rule engine, UI component, API endpoint)
2. **Check existing patterns** in similar code
3. **Make focused changes** following established conventions  
4. **Update types/interfaces** if data structures change
5. **Test with sample documents** in `/testfiles/`

### State Management Flow
```
User Action → Component → Hook → API Service → Backend Endpoint → Rule Engine → Response → Hook → Component Update
```

---

This guide focuses on practical development patterns for working efficiently with the CloseGuard codebase. Follow the modular architecture and established conventions to maintain code quality and consistency.