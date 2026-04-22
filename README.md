# 🚀 Advanced Web Solutions

## 📌 Overview
This project is a Django-based web application designed for data analytics, reporting, and pressure monitoring. It follows the MVT architecture and integrates multiple modules for authentication, analytics, and reporting.

---

# Graphene Trace - MedTech Pressure Monitoring Platform

Production-oriented Django + MySQL web app for ingesting 32x32 pressure mat data, computing ulcer-risk metrics, and presenting clinician/patient dashboards.

## Tech Stack
- Frontend: HTML, CSS, JavaScript (Chart.js)
- Backend: Django
- Database: MySQL
- Security: Django CSRF + auth middleware + ORM-based query protection + RBAC

## Project Structure
- `graphenetrace/` - Django project config
- `auth_app/` - login, profile, RBAC, admin assignment flows
- `data_app/` - sensor data, metrics, alerts, comments/replies, APIs
- `analytics_app/` - reusable pressure analytics services
- `reporting_app/` - report UI (today vs yesterday)
- `templates/` + `static/` - dashboard/reporting frontend
- `mysql_schema.sql` - schema notes/index strategy

## User Stories Coverage
Implemented all required streams:
- Member 1: secure auth, role separation, admin user creation, clinician assignment, profile update
- Member 2: CSV processing, PPI/contact-area analytics, high-pressure detection, dashboard heatmap/charts
- Member 3: reporting view, comments/replies, human-readable alerts

## Setup
1. Install Python 3.11+ and MySQL.
2. Create virtual env and install dependencies:
   - `pip install -r requirements.txt`
   - Optional MySQL driver (only if using MySQL): `pip install -r requirements-mysql.txt`
3. Copy `.env.example` to `.env` and fill values.
4. Run migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
5. Create admin:
   - `python manage.py createsuperuser`
6. Load dataset:
   - `python manage.py load_sensor_csv --data-dir "GTLB-Data"`
7. Start app:
   - `python manage.py runserver`

## Key APIs
- `GET /data/api/summary/?hours=1|6|24&user_id=<id>`
- `GET|POST /data/api/comments/`
- `POST /data/api/comments/<comment_id>/reply/`
- `GET /analytics/api/overview/`
- `GET /reports/`

## Security Notes
- Password hashing via Django auth
- CSRF enabled on forms and JSON POSTs
- ORM-only DB operations (SQLi-safe approach)
- Role checks via explicit decorator
- Template auto-escaping active for XSS mitigation

## Testing
- `python manage.py test`
- Includes initial unit tests for auth and analytics services.
- Add integration tests for CSV edge cases:
  - Empty CSV
  - Corrupt row counts
  - Extreme pressure values near 4095

## No-Admin Local Mode (Recommended for restricted machines)
- Keep `USE_SQLITE_FALLBACK=True` in `.env`
- Run `run_all.bat`
- This avoids needing local MySQL service/admin privileges
