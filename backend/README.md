# KapasityGO Backend

The KapasityGO Backend is a FastAPI application designed to manage IoT devices, collect readings, and handle certificates for secure communication. This backend provides RESTful API endpoints secured with API keys and client certificates to ensure secure data transmission and device authentication.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Running Locally](#running-locally)
  - [Running Using Docker](#running-using-docker)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
- [Deployment](#deployment)
  - [Staging Environment](#staging-environment)
  - [Production Environment](#production-environment)
- [Contributing](#contributing)
- [License](#license)
- [Additional Information](#additional-information)
  - [Security Considerations](#security-considerations)
  - [Testing](#testing)
  - [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Features

- **Device Management**: Create, update, retrieve, and delete IoT devices.
- **Readings Collection**: Collect and retrieve readings from IoT devices.
- **Certificate Handling**: Issue, revoke, and manage certificates for devices.
- **Secure Communication**:
  - **API Key Authentication**: All endpoints require an API key passed in the `X-API-KEY` header.
  - **Client Certificate Authentication**: The `/readings` endpoint requires a client certificate passed in the `X-Client-Cert` header.
- **Database Integration**: Uses PostgreSQL for data storage.
- **Dockerized Deployment**: Easily deployable using Docker and Docker Compose.

---

## Technologies Used

- **Python 3.10**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Docker & Docker Compose**

---

## Prerequisites

- **Git**: To clone the repository.
- **Python 3.10**: Ensure Python is installed.
- **Docker & Docker Compose**: For containerized deployment.
- **OpenSSL**: For generating certificates (optional for development).

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/kapasitygo-backend.git
cd kapasitygo-backend
```

### 2. Create a Virtual Environment

```bash
python3.10 -m venv venv
```

### 3. Activate the Virtual Environment

- **Linux/MacOS:**
```bash
source venv/bin/activate
```
- **On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
---

## Configuration
### Environment Variables

Create a .env file in the root directory to store environment-specific variables. Do not commit this file to version control.

Example .env file:
```bash 
# Database configuration
DATABASE_URL=postgresql://your_user:your_secure_password@localhost/kapasitygo_db

# Secret key for encryption, etc.
SECRET_KEY=your_secret_key

# API key for authentication
API_KEY=your_secure_api_key
```

## Running the Application

### Running Locally
1. Initialize the Database

Make sure PostgreSQL is running and accessible. Update the DATABASE_URL in your .env file accordingly.

2. Apply Migrations

If you're using Alembic for database migrations, run:
```bash
alembic upgrade head
```

3. Start the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000.

### Running Using Docker
#### 1. Build the Docker Image

```bash
docker build -t kapasitygo-backend .
```

#### 2. Run the Docker Container

```bash
docker run -d -p 8000:8000 --env-file .env kapasitygo-backend
```
--- 

## API Documentation
### Authentication
#### API Key Authentication

    Header: X-API-KEY: your_secure_api_key
    All endpoints require the API key.

#### Client Certificate Authentication

    Header: X-Client-Cert: <client_certificate>
    The /readings endpoint requires a client certificate for authentication.
    Certificates are stored in the database and validated on each request.

### Endpoints
#### Devices

    Create Device
        POST /devices/
    Get Devices
        GET /devices/
    Get Device by ID
        GET /devices/{device_id}
    Update Device
        PUT /devices/{device_id}
    Delete Device
        DELETE /devices/{device_id}

#### Readings

    Create Reading
        POST /readings/
        Requires client certificate authentication.
    Get Readings
        GET /readings/
    Get Reading by ID
        GET /readings/{reading_id}

#### Certificates

    Create Certificate
        POST /certificates/
    Get Certificates
        GET /certificates/
    Get Certificate by ID
        GET /certificates/{certificate_id}
    Revoke Certificate
        PUT /certificates/{certificate_id}/revoke

---

## Deployment

Deployment is managed via Docker Compose with separate configurations for staging and production environments.
### Staging Environment

-   Compose File: docker-compose.staging.yml

-   Command:
```bush
 docker-compose -f docker-compose.staging.yml up -d
```

### Production Environment

- Compose File: docker-compose.prod.yml

- Command:
```bash
    docker-compose -f docker-compose.prod.yml up -d
```

Note: Ensure that environment variables and secrets are properly configured in the respective Docker Compose files or provided via external means.

---

## Contributing

This is a test project so contributions not needed!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Additional Information
### Security Considerations

    API Keys: Keep your API keys secure. Do not commit them to version control.
    Client Certificates: Ensure client certificates are securely generated and distributed to IoT devices.
    HTTPS: Use HTTPS in production environments to encrypt data in transit.

### Testing

    Unit Tests: Implement unit tests for your code.
    Integration Tests: Use tools like Postman to test API endpoints.

### Contact

For questions or support, please contact pavel.melekhof@gmail.com.

