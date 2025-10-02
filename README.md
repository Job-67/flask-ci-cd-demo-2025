# Flask CI/CD Demo 2025

A comprehensive Flask application demonstrating modern CI/CD practices with GitHub Actions.

## Features

- **Flask REST API** with user management
- **PostgreSQL** database integration
- **Redis** caching support
- **Comprehensive testing** with pytest
- **Docker containerization**
- **CI/CD pipeline** with GitHub Actions
- **Security scanning** with multiple tools
- **Code coverage** reporting

## Project Structure

```
flask-ci-cd-demo-2025/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── tests/             # Test suite
│       ├── __init__.py
│       ├── conftest.py    # Test configuration
│       ├── test_app.py    # API endpoint tests
│       └── test_models.py # Model tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions workflow
├── Dockerfile             # Container configuration
├── .dockerignore          # Docker ignore rules
└── README.md              # This file
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /users` - List all users
- `POST /users` - Create new user
- `GET /users/<id>` - Get user by ID
- `GET /cache/<key>` - Get cached value
- `POST /cache/<key>` - Set cached value

## Local Development

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, SQLite used as fallback)
- Redis (optional, fake Redis used as fallback)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd flask-ci-cd-demo-2025
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Run tests:
   ```bash
   pytest tests/ -v --cov=.
   ```

## Docker

Build and run with Docker:

```bash
docker build -t flask-ci-cd-demo .
docker run -p 5000:5000 flask-ci-cd-demo
```

## CI/CD Pipeline

The GitHub Actions workflow includes:

1. **Testing** - Run pytest with coverage
2. **Security Scanning** - Snyk, Safety, Bandit, Semgrep, TruffleHog
3. **Docker Build** - Build and push container image
4. **Notifications** - PR comments with results

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - Flask secret key
- `SNYK_TOKEN` - Snyk API token (for security scanning)

## Testing

The test suite includes:

- **Unit tests** for models and business logic
- **Integration tests** for API endpoints
- **Error handling** tests
- **Database operations** tests
- **Caching functionality** tests

Run tests with coverage:

```bash
pytest tests/ -v --cov=. --cov-report=html
```

## Security

Multiple security tools are integrated:

- **Snyk** - Dependency and code vulnerability scanning
- **Safety** - Python package vulnerability checking
- **Bandit** - Static security analysis
- **Semgrep** - Code pattern analysis
- **TruffleHog** - Secret detection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is for demonstration purposes.
"# Test PR" 
