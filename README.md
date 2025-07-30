# CloseGuard

AI-powered analysis for home closing documents. Upload PDF closing documents and get instant analysis for potential red flags and issues.

## Project Structure

```
mortgagebuddy/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend  
└── infra/           # Infrastructure configs
```

## Backend (FastAPI)

### Setup
```bash
cd backend
pip install -r requirements.txt
python3.11 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### API Endpoints
- `POST /upload` - Upload PDF for analysis
- `GET /report/{report_id}` - Get analysis results
- `GET /docs` - API documentation

### Rules Engine
Rules are defined in `rules-config.yaml`:
- **numeric_threshold**: Compare dollar amounts/percentages
- **regex_absence**: Check for missing required patterns
- **regex_amount**: Find amounts exceeding thresholds

## Frontend (Next.js + Tailwind)

### Setup
```bash
cd frontend
npm install
npm run dev
```

### Features
- Drag-and-drop PDF upload
- Real-time analysis results
- Professional UI with error handling
- TypeScript support

## Usage

1. **Start Backend**: `http://127.0.0.1:8000`
2. **Start Frontend**: `http://localhost:3000`
3. **Upload PDF**: Use the web interface to upload closing documents
4. **View Results**: Get instant analysis with flagged issues

## Sample Rules

- High closing costs (>$5,000)
- Excessive loan amounts (>$500,000)
- High interest rates (>7%)
- Missing title insurance
- Large wire transfers (>$10,000)

## Tech Stack

**Backend**: FastAPI, Python, pdfplumber, PyPDF2, YAML
**Frontend**: Next.js, React, TypeScript, Tailwind CSS
**Analysis**: Custom rule engine with regex and numeric validation