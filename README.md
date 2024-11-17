# KapasityGO - Smart Waste Management System

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Assumptions Made](#assumptions-made)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Database Creation and Data Insertion](#database-creation-and-data-insertion)
  - [Backend](#backend)
  - [IoT Simulator](#iot-simulator)
  - [Frontend](#frontend)
- [License](#license)

## Project Overview

KapasityGO is a Smart Waste Management System designed to monitor trash compactor fullness levels and display data on a web dashboard.
- Deployed backend is accessible here: http://135.181.101.90:8060/ with OpenAPI documentation here http://135.181.101.90:8060/docs
- Deployed Frontend/Dashboard: http://135.181.101.90:8081/

  

## Repository Structure

- [**backend/**](/backend/README.md): Backend API built with Python and FastAPI.
- [**frontend/**](/frontend/README.md): Frontend application built with Next.js, React, and TypeScript.
- [**iot-simulator/**](/iot-simulator/README.md): IoT simulation scripts to mimic trash compactors.
- [**database/**](/database/README.md): Database scripts and schema definitions.
- [**docs/**](/docs/README.md): Architecture diagram & Other documentation.

## Assumptions Made

1. **Coding Language**: Python was chosen for the backend and IoT simulator because it is the language I have recently worked with, and it is easy to code and understand while being powerful enough to serve as a backend core.
2. **Security**: The security implementation is very schematic (no HTTPS, API-KEY-based), but the approach of using x509 certificates on the IoT device side could be usable in a real-life scenario with further improvements.
3. **Simulation Containers**: Running each simulated device as a separate container can be beneficial when testing at scale, as it allows deploying many containers of different types to simulate a real-life workload.
4. **Container Deployment**: Everything is deployed as Docker containers because I am most familiar with this approach, and it is still suitable for use in a production environment.
5. **Hosting Environment**: The project is deployed to an Ubuntu server running in the Hetzner datacenter VPC. This hosting provides great value for money and is well-suited for startups.
6. **HTTP vs. MQTT**: HTTP was chosen over MQTT as it is a simpler solution to implement. Since compactors send data infrequently (every 15 minutes), HTTP works well without the need for advanced QoS, keep-alive connectivity, etc.

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

