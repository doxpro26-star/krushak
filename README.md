# Krushak — Farmer Crop Damage Reporting (Flask)

Enterprise-level, farmer-friendly portal to report crop damage due to Heavy Monsoon / Flood / Drought / Pollution / Pest / Hailstorm.

## Features
- **Farmer:** Register (mobile+village), Login, Dashboard, Report damage with photo, Track status (Pending → Verified → Approved/Rejected → Compensation Initiated)
- **Admin:** Login, KPI dashboard (Chart.js), Reports list with search/filter, Status update with remark, Delete
- **UI:** Professional green agri theme, Bootstrap 5, large buttons, simple language, Marathi toggle, voice-help placeholder, mobile responsive

## Quick Start
```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```
DB auto-creates at `instance/krishi.db`.

Demo accounts:
- Admin: `admin / admin123` → http://127.0.0.1:5000/admin/login
- Farmer: `ramesh / farmer123` → http://127.0.0.1:5000/farmer/login

## Project Structure
```
app.py              # Flask app + models + routes
config.py
requirements.txt
templates/
  base.html, index.html, about.html
  farmer/ register, login, dashboard, report, report_detail
  admin/ login, dashboard, reports, report_detail
static/css/style.css, js/main.js, uploads/
instance/krishi.db
```

## Enterprise Notes
- SQLAlchemy + Flask-Login, secure password hashing
- Photo upload validated (png/jpg/jpeg/webp, 5MB max)
- Admin guard decorator, SEO-friendly URLs
# krushak
