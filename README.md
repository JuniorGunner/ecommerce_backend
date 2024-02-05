# E-Commerce Backend API

This repository contains the backend code for an e-commerce platform. The service is written in Python, using FastAPI as the web framework, and SQLAlchemy for ORM, with PostgreSQL as the database. It includes a RESTful API for users, carts, orders, and products.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: The Python SQL toolkit and Object-Relational Mapper that gives application developers the full power and flexibility of SQL.
- **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- **Black**: The uncompromising Python code formatter.
- **Docker**: A set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
- **PostgreSQL**: A powerful, open source object-relational database system.

## Project Structure

```plaintext
ecommerce_backend/
|-- alembic/            # Database migration scripts
|-- models/             # Data models
|-- routes/             # API route definitions
|-- schemas/            # Pydantic models for request and response data validation
|-- services/           # Business logic
|-- tests/              # Unit and integration tests
|-- .env                # Environment variables
|-- .gitignore          # Specifies intentionally untracked files to ignore
|-- alembic.ini         # Configuration for Alembic
|-- database.py         # Database connection setup
|-- dependencies.py     # Dependency injection for FastAPI
|-- docker-compose.yml  # Docker Compose configuration
|-- Dockerfile          # Docker configuration for building the image
|-- main.py             # Entry point of the application
|-- Makefile            # Makefile with commands to manage the Docker containers
|-- README.md           # README file
|-- requirements.txt    # List of dependencies


Getting Started
Prerequisites
Make sure you have Docker and Docker Compose installed on your system.

Running the Application
Start the Application:

Use the Makefile for managing the lifecycle of the application.

make up

This command will build the Docker images and start the services defined in docker-compose.yml.

Apply Database Migrations:

After starting the application, you'll need to apply database migrations. Run the following command:

docker-compose exec web alembic upgrade head

This command runs Alembic's upgrade command inside the web container to apply the database migrations.

Stopping the Application:

To stop the application and remove containers, networks, volumes, and images created by up, run:

make down

Restarting the Application:

If you need to restart the application, use:

make restart

Running Tests
To run the automated tests for this system, execute the following command inside the root folder:

pytest

or for verbode mode:

pytest -v
