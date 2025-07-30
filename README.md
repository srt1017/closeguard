# CloseGuard

AI-powered analysis for home closing documents. Upload PDF closing documents and get instant analysis for potential red flags and issues.

## Project Structure

```
mortgagebuddy/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend  
└── infra/           # Infrastructure configs
```

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone git@github.com:srt1017/closeguard.git
   cd closeguard
   ```

2. **Start the Backend (Terminal 1)**
   ```bash
   cd backend
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install missing dependency for file uploads
   pip install python-multipart
   
   # Start the FastAPI server
   python3.11 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   
   Backend will be available at: `http://127.0.0.1:8000`
   API docs available at: `http://127.0.0.1:8000/docs`

3. **Start the Frontend (Terminal 2)**
   ```bash
   cd frontend
   
   # Install Node.js dependencies
   npm install
   
   # Start the Next.js development server
   npm run dev
   ```
   
   Frontend will be available at: `http://localhost:3000`

4. **Test the Application**
   - Open `http://localhost:3000` in your browser
   - Upload the test PDF (`backend/test_closing_document.pdf`)
   - View the analysis results with detected flags

### Backend (FastAPI)

#### API Endpoints
- `POST /upload` - Upload PDF for analysis
- `GET /report/{report_id}` - Get analysis results
- `GET /docs` - Interactive API documentation

#### Rules Engine
Rules are defined in `rules-config.yaml`:
- **numeric_threshold**: Compare dollar amounts/percentages
- **regex_absence**: Check for missing required patterns
- **regex_amount**: Find amounts exceeding thresholds

### Frontend (Next.js + Tailwind)

#### Features
- Drag-and-drop PDF upload
- Real-time analysis results
- Professional UI with error handling
- TypeScript support

#### Development
```bash
cd frontend
npm run dev     # Start development server
npm run build   # Build for production
npm run start   # Start production server
```

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