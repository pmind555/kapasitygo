# Database Setup for KapasityGO

## Overview

This directory contains SQL scripts to set up the PostgreSQL database for KapasityGO.

## Scripts

- `create_database.sql`: Creates the database and a dedicated user (optional).
- `insert_deviced.sql`: Inserts initial sample devices (optional).
- `insert_cetrtificates.sql`: Inserts sample certificates (optional).

## Prerequisites

- PostgreSQL installed and running.
- Access to a PostgreSQL superuser account (e.g., `postgres`) to create databases and users.

## Setup Instructions

### 1. Create the Database and User (Optional)

**Note**: This step requires superuser privileges.

```bash
psql -U postgres -f create_database.sql
```

### 2. Insert Sample Data (Optional)

```bash
psql -U kapasitygo_user -d kapasitygo_db -f insert_deviced.sql
psql -U kapasitygo_user -d kapasitygo_db -f insert_cetrtificates.sql
```




