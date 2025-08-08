# CloseGuard - Build & Run Instructions

## 🚀 Quick Start (Recommended)

### Option 1: Automated Build & Run
```bash
# Build everything
./build.sh

# Start both frontend and backend
./start.sh
```

### Option 2: Manual Setup

#### Frontend Setup
```bash
cd frontend
npm install
npm run build    # for production
npm run dev      # for development
```

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 🔧 Common Build Issues & Solutions

### Issue 1: ESLint Version Conflicts
**Error**: `Error while loading rule '@typescript-eslint/no-unused-expressions'`

**Solution**: The package.json has been fixed to use ESLint 8.x instead of 9.x
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue 2: TypeScript Property Errors
**Error**: `Property 'verifications' does not exist`

**Solution**: Hook interfaces have been aligned. If you see this:
- Check that you're using `flagVerifications` from the verification hook
- Make sure all imports are correct

### Issue 3: Multiple Lockfiles
**Error**: `Found multiple lockfiles`

**Solution**: Remove conflicting lockfiles
```bash
rm -f /Users/$(whoami)/package-lock.json
cd frontend && npm install
```

### Issue 4: Python Virtual Environment Issues
**Error**: Various Python import errors

**Solution**: Always use virtual environment
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📁 Project Structure

```
mortgagebuddy/
├── build.sh          # Automated build script
├── start.sh          # Automated startup script
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # Next.js 15 app router
│   │   ├── components/# React components
│   │   ├── hooks/     # Custom React hooks
│   │   ├── types/     # TypeScript definitions
│   │   └── utils/     # Utility functions
│   ├── package.json   # Frontend dependencies
│   └── tsconfig.json  # TypeScript config
├── backend/           # FastAPI application
│   ├── main.py        # API server
│   ├── models/        # Data models
│   ├── services/      # Business logic
│   ├── rules/         # Rule handlers
│   ├── config/        # Configuration
│   ├── requirements.txt
│   └── venv/          # Python virtual environment
└── CLAUDE.md          # Project documentation
```

## 🌐 URLs & Ports

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔍 Troubleshooting

### Build Script Not Working
```bash
# Make sure scripts are executable
chmod +x build.sh start.sh

# Run from root directory
cd /path/to/mortgagebuddy
./build.sh
```

### Port Already in Use
```bash
# Kill processes on ports
lsof -ti:3000 | xargs kill
lsof -ti:8000 | xargs kill
```

### Node.js Version Issues
```bash
# Check Node version (requires 18+)
node --version

# Use nvm if needed
nvm use 18
```

### Python Version Issues
```bash
# Check Python version (requires 3.8+)
python3 --version

# Use pyenv if needed
pyenv install 3.11
pyenv local 3.11
```

## ✅ Verification Steps

After building, verify everything works:

1. **Frontend loads**: Visit http://localhost:3000
2. **API responds**: Visit http://localhost:8000/docs
3. **Upload works**: Try uploading a PDF file
4. **Analysis runs**: Check that results appear

## 🎯 Development Workflow

```bash
# Daily development
cd mortgagebuddy

# Start development servers
./start.sh

# In separate terminals for development:
# Frontend changes
cd frontend && npm run dev

# Backend changes  
cd backend && source venv/bin/activate && python3 main.py

# Build for production
./build.sh
```

## 🚨 Known Issues

1. **ESLint warnings**: Some deprecation warnings are expected, build still succeeds
2. **PDF processing**: Requires system dependencies for OCR (optional)
3. **Memory usage**: Large PDFs may take time to process

---

**Need help?** Check the issues in the repository or run the automated scripts first.