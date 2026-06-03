# Engineering - Synthetic Data Generator - Middleware Service

[![CodeQL Advanced](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/codeql.yml/badge.svg)](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/codeql.yml)

[![Docker Build and Push (DEV)](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/docker-dev.yml/badge.svg?branch=middleware)](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/docker-dev.yml)

[![Python Lint and Security Middleware](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/python-lint-middleware.yml/badge.svg)](https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware/actions/workflows/python-lint-middleware.yml)

## Overview

The GENESIS Middleware service is a critical component of the GENErative System for Intelligent Synthetic data generation (GENESIS) project. This middleware layer serves as the persistent storage and orchestration backbone that enables the synthetic data generation pipeline to function efficiently. The primary role of this service is to provide a centralized database and API interface that manages machine learning algorithms, trained models, data processing functions, and their associated metadata.

The middleware acts as an intermediary between client applications and the core generator service, handling data validation, storage, and retrieval operations. It maintains a comprehensive registry of supported algorithms (such as RandomForestClassifier, MLPClassifier, SVC, and LogisticRegression), their compatible data types, and the functions required for data preprocessing and transformation. By abstracting these complexities, the middleware allows the generator service to focus on the actual synthetic data generation logic while ensuring data consistency and integrity across the system.

## Architecture and Component Interactions

The GENESIS Middleware service operates within a distributed microservices architecture and interacts with several key components:

### Generator Service
The middleware communicates with the upstream generator service via HTTP REST API calls. When users submit synthetic data generation requests, the middleware validates the input, retrieves relevant model and function metadata from the database, and forwards processed requests to the generator service at configurable endpoints:
- `/train` for new model training
- `/infer` for inference on existing models
- `/generate` for feature-based generation

The generator service URL is configurable via the `GENERATOR_URL` environment variable (default: `http://localhost:8010`).

### Database Layer
The service uses Peewee ORM with support for both PostgreSQL and SQLite databases:
- **Production**: PostgreSQL using credentials provided through environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_PORT`)
- **Testing**: In-memory SQLite database for automated testing

The database schema includes tables for algorithms, data types, trained models, model versions, functions, parameters, and their relationships through foreign key constraints.

### Client Applications
Through CORS-enabled endpoints, the middleware serves web and API clients. CORS origins are configurable via the `ALLOWED_ORIGINS` environment variable, allowing controlled access from specified domains. The service enforces UTF-8 encoding on all incoming requests and provides comprehensive error handling with appropriate HTTP status codes.

### Bootstrap Data System
On startup, if the `BOOTSTRAP_DATA` environment variable is set, the middleware populates the database with sample data including:
- Algorithms (RandomForestClassifier, MLPClassifier, SVC, LogisticRegression)
- Data types (integer, float, string, boolean, image)
- Trained models with versions
- Preprocessing functions from scikit-learn (StandardScaler, CountVectorizer, MinMaxScaler, OneHotEncoder) with their parameters and compatible data types

## Features

- **Algorithm Management**: CRUD operations for machine learning algorithms with their compatible data types
- **Function Registry**: Management of preprocessing functions with parameters and data type compatibility
- **Trained Model Storage**: Persistent storage of trained models with versioning, training metrics, and feature schemas
- **Data Type System**: Comprehensive data type classification with categorical/continuous categorization
- **Input Validation**: Robust validation of user inputs with detailed error messages
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation available at `/docs`

## Supported Data Types

The middleware supports the following data types for synthetic data generation:

### Basic Data Types
| Type | Description | Is Categorical |
|------|-------------|----------------|
| `integer` | Integer numbers (int32) | No |
| `float` | Floating point numbers (float32) | No |
| `string` | Text/string data | Yes |
| `boolean` | Boolean values | Yes |
| `image` | Image data | No |

### Data Type Categories
| Category | Description |
|----------|-------------|
| `continuous` | Continuous numerical data |
| `categorical` | Categorical data |
| `primary_key` | Primary key fields |
| `group_index` | Grouping/index fields |

### Supported Dataset Types
| Type | Description |
|------|-------------|
| `table` | Tabular data |
| `time_series` | Time series data |

## API Documentation

The middleware exposes a RESTful API through FastAPI with four main router modules:

### Endpoints Overview

| Router | Prefix | Endpoints |
|--------|--------|-----------|
| Synthetic Data Generator Input | `/sdg_input` | POST `/` - Collect user input for generation |
| Algorithms | `/algorithms` | GET `/`, POST `/`, GET `/{id}`, DELETE `/{id}` |
| Functions | `/functions` | GET `/`, POST `/`, GET `/{id}`, DELETE `/{id}` |
| Trained Models | `/trained_models` | GET `/`, POST `/`, GET `/{id}`, DELETE `/{id}` |

### HTTP Status Codes
| Status Code | Description |
|-------------|-------------|
| 200 OK | Success for GET requests |
| 201 Created | Resource created successfully |
| 204 No Content | Success for DELETE requests |
| 400 Bad Request | Invalid input or validation errors |
| 404 Not Found | Resource not found |
| 503 Service Unavailable | Backend connection error |

For detailed API documentation including request/response schemas, validation rules, and examples, see [docs/API_TABLE.md](docs/API_TABLE.md).

Interactive API documentation is available at `/docs` when the service is running.

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (for production) or SQLite (for development/testing)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Engineering-Research-and-Development/synthetic_data_generator_middleware.git
cd synthetic_data_generator_middleware
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
export POSTGRES_USER=your_user
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_DB=genesis_db
export POSTGRES_PORT=5432
export GENERATOR_URL=http://localhost:8010
export ALLOWED_ORIGINS=*
export BOOTSTRAP_DATA=true
```

4. Run the service:
```bash
cd src/server
python main.py
```

The service will start on `http://0.0.0.0:8001`

## Docker Deployment

A Dockerfile is provided for containerized deployment:

```bash
docker build -t genesis-middleware .
docker run -p 8001:8001 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_HOST=postgres \
  -e POSTGRES_DB=genesis_db \
  -e POSTGRES_PORT=5432 \
  -e GENERATOR_URL=http://generator:8010 \
  genesis-middleware
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | - |
| `POSTGRES_PASSWORD` | PostgreSQL password | - |
| `POSTGRES_HOST` | PostgreSQL host | - |
| `POSTGRES_DB` | PostgreSQL database name | - |
| `POSTGRES_PORT` | PostgreSQL port | - |
| `GENERATOR_URL` | Generator service URL | `http://localhost:8010` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `*` |
| `BOOTSTRAP_DATA` | Enable bootstrap data on startup | `false` |
| `TESTING` | Enable testing mode (SQLite) | `false` |

## Development

### Running Tests

```bash
pytest src/test/
```

### Code Style

The project uses automated linting and security checks. See GitHub Actions for details.

### Database Schema

The database schema is defined in `src/server/database/schema.py` and includes:
- `Algorithm`: Machine learning algorithms
- `DataType`: Supported data types
- `AlgorithmDataType`: Algorithm-data type relationships
- `TrainedModel`: Trained model metadata
- `TrainModelDatatype`: Feature schema for trained models
- `ModelVersion`: Model versioning with training metrics
- `Function`: Preprocessing functions
- `Parameter`: Function parameters
- `FunctionParameter`: Function-parameter relationships
- `FunctionDataType`: Function-data type compatibility

## License

See [LICENSE](LICENSE) file for details.