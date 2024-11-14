# KapasityGO - Smart Waste Management System

## Project Overview

KapasityGO is a Smart Waste Management System designed to monitor trash compactor fullness levels and display data on a web dashboard.

## Repository Structure

- [**backend/**](/backend/README.md): Backend API built with Python and FastAPI.
- [**frontend/**](/frontend/README.md): Frontend application built with Next.js, React, and TypeScript.
- [**iot-simulator/**](/iot-simulator/README.md): IoT simulation scripts to mimic trash compactors.
- [**database/**](/database/README.md): Database scripts and schema definitions.
- [**docs/**](/docs/README.md): Other documentation and diagrams.

## Getting Started

### Prerequisites
- **PostgreSQL**: Ensure PostgreSQL is installed and set up with proper access rights. You'll need a database with the appropriate permissions for creating tables, users, and managing data.
- **Docker Host**: Docker and Docker Compose must be installed on your local or remote host to deploy services such as the backend, frontend, and simulated IoT devices.

### Database Creation and Data Insertion
To set up the database, follow these steps:
1. Create a PostgreSQL database.
2. Run the schema creation scripts provided.
3. Insert initial data as needed.

Detailed instructions are available in the [database README](/database/README.md).

### Backend
The backend service is responsible for handling API requests from simulated IoT devices and the frontend. It is built using FastAPI.
- Set up the backend environment, including environment variables, dependencies, and running the service.

Refer to the [backend README](/backend/README.md) for more detailed steps.

### IoT Simulator
The IoT Simulator emulates trash compactors, sending periodic updates to the backend API. Each simulated device runs independently as a Docker container, allowing scalable testing of multiple devices.
- Set up Docker containers for each simulated device.
- Configure environment variables and certificates for secure communication.

See the [iot-simulator README](/iot-simulator/README.md) for detailed steps.

### Frontend
The frontend application is currently **in progress**. It will provide a web dashboard to visualize the data collected from trash compactors.

More information can be found in the [frontend README](/frontend/README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

