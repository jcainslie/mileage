# Mileage Tracker Web App

A simple, secure, self-hosted web application for tracking vehicle mileage against lease allowances. Built with Python, Flask, SQLAlchemy, and deployed via Docker.

---

## 📦 Features

- Track odometer entries over time
- Automatically calculates average daily usage
- Compares usage to allowed lease mileage
- Login-required access (Flask-Login)
- SQLite-backed database
- Environment-configurable settings
- Designed for Docker + Portainer deployment
- Volume-mounted persistent database (NAS/NFS or local)

---

## 📊 Lease Tracking Logic

- **Start Date:** Sept 8, 2024  
- **Lease Length:** 12,000 miles/year  
- **Monthly Allowance:** 1,000 miles  
- **Starting Odometer:** 17 miles  
- Uses Central Timezone (America/Chicago)

---

## 🚀 Deployment (via Docker + Portainer)

This app is intended to run as a single-container Docker service with volume and environment variables managed through **Portainer**.

### 📁 Volume

Mount a Docker volume named `mileage` to persist the database:

```yaml
volumes:
  - mileage:/app/instance
