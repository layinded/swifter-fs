# Swifter-FS Release Notes

## Version 1.0.0 - Initial Release

### Overview
Swifter-FS is a production-ready FastAPI full-stack template with modern tooling and architecture, including social login integrations, modular project structure, and support for deployment with Docker.

---

### Features

- **Full Stack FastAPI Backend** with SQLModel, Alembic migrations, and PostgreSQL.
- **Social Login Integration**: Google and Facebook authentication.
- **Modular Architecture**: Organized codebase with clear separation between core app logic and user customizations.
- **Docker Support**: Docker and Docker Compose files for easy local development and production deployments.
- **Environment-based Configurations**: `.env` and `.env.example` for managing environment variables.
- **CORS Support**: Configurable origins for secure cross-domain requests.
- **Email Support**: Email service integration with configurable SMTP settings.
- **Pre-configured OAuth2 and JWT Authentication**.
- **Scripts for Database Migrations, Tests, and Linting**.
- **Customizable CRUD modules** in the `custom/` folder without affecting core updates.

---

### Folder Structure Highlights

- **backend/**
  - `app/`: Core FastAPI application.
  - `custom/`: User-defined modules and extensions.
  - `scripts/`: Utilities and management scripts.
  - `.env.example`: Environment variables template.

---

### Installation

- Clone the repository.
- Copy `.env.example` to `.env` and configure it.
- Run `uv sync` to install dependencies.
- Start the app with Docker Compose or directly with `uvicorn`.

---

### Changelog

- **Added**: Full FastAPI backend with JWT and OAuth2.
- **Added**: Google and Facebook login integrations.
- **Added**: Docker configuration for development and production.
- **Added**: Custom modules directory for user-defined extensions.

---

### Known Issues

- Ensure Docker builds include the `custom/` directory.

---

### Next Steps

- **Planned Features**:
  - CAPTCHA support for forms.
  - Additional social login providers.
  - CI/CD pipeline integration.

---

Thank you for using Swifter-FS! Please report issues and contribute via the [GitHub repository](https://github.com/layinded/swifter-fs.git).
