# SMAK AI API

A FastAPI application for SMAK AI.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── api/           # API routes
│   ├── core/          # Core functionality (config, security, etc.)
│   ├── models/        # Database models
│   └── schemas/       # Pydantic schemas
├── main.py            # Main application entry point
├── requirements.txt   # Python dependencies
├── env.example        # Environment variables example
└── README.md         # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit .env file with your configuration
```

### 4. Run the Application

```bash
# Development server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Development

### Adding New Routes

1. Create route files in `app/api/`
2. Import and include them in `main.py`
3. Use the existing structure for consistency

### Adding Models

1. Create model files in `app/models/`
2. Create corresponding schemas in `app/schemas/`

### Configuration

Update `app/core/config.py` for application settings and environment variables.

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management
- **python-multipart**: For handling form data

## Next Steps

- Add database integration (SQLAlchemy, etc.)
- Implement authentication and authorization
- Add API versioning
- Set up logging and monitoring
- Add tests
- Configure production deployment
