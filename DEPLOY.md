# Krushak - Deploy Guide (Render Backend + Vercel Frontend)

## Architecture
This repo is a Flask monolith. You can deploy the **same codebase** to both:
- **Render** → Production backend (Web Service, gunicorn, persistent)
- **Vercel** → Frontend CDN + Serverless Python (instant, global edge)

> For a pure Jamstack split (React frontend on Vercel + Flask API on Render), see Option B at bottom.

---

### Option A: Monolith on both (Recommended - 5 mins)

#### 1) Push to GitHub (already done)
https://github.com/doxpro26-star/krushak

#### 2) Backend on Render
1. Go to https://dashboard.render.com → New → **Web Service**
2. Connect repo `doxpro26-star/krushak` → Branch `main`
3. Render auto-detects `render.yaml`:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Python:** 3.11.9
4. Env Vars (Add in Render Dashboard):
   - `SECRET_KEY` → generate (or let Render generate via render.yaml)
   - `FLASK_ENV=production`
   - Optional for Postgres: add Render PostgreSQL and set `DATABASE_URL` (auto-injected). `config.py` handles `postgres://` → `postgresql://` conversion. If empty, falls back to SQLite (`instance/krishi.db`)
5. Create → Deploy. URL e.g. `https://krushak-backend.onrender.com`
   - Test: `/`, `/api/stats`, admin login `admin / admin123`

> **Uploads on Render:** Free tier disk is ephemeral. Use `static/uploads` for demo; for production switch to Cloudinary/S3 and replace `photo` save logic.

#### 3) Frontend on Vercel (same Flask on serverless)
1. Go to https://vercel.com/new → Import `doxpro26-star/krushak`
2. Framework: **Other** (Vercel detects `vercel.json`)
3. No build command needed. Vercel uses:
   - `api/index.py` → `@vercel/python` serverless (wraps `app`)
   - `vercel.json` routes: `/static/*` → static, `/(.*)` → `api/index.py`
4. Env Vars in Vercel → Settings → Environment Variables:
   - `SECRET_KEY` = same as Render
   - `FLASK_ENV=production`
   - `DATABASE_URL` = if using shared Postgres, paste same connectionString; else leave empty for SQLite (ephemeral but fine for demo)
5. Deploy → URL e.g. `https://krushak.vercel.app`

You now have:
- **Render:** https://krushak-backend.onrender.com  (primary API, admin heavy ops)
- **Vercel:** https://krushak.vercel.app  (CDN frontend, serverless)

Both point to same GitHub `main`; push → auto-deploy both.

---

### Option B: Real Split (Vercel static + Render API)
If you want Vercel to host only static HTML/JS that calls Render API:
1. Create `/frontend` React/Vite app that fetches `https://krushak-backend.onrender.com/api/*`
2. Enable CORS in `app.py` (already added: `Flask-Cors`)
3. Deploy `/frontend` to Vercel, set `VITE_API_URL` env to Render URL.

---

### Files Added
- `Procfile` - Render start
- `runtime.txt` - Python 3.11.9
- `render.yaml` - Infra as Code
- `vercel.json` + `api/index.py` + `.vercelignore` - Vercel Python serverless
- `config.py` - `DATABASE_URL` support
- `requirements.txt` + `gunicorn`, `psycopg2-binary`, `Flask-Cors`

### Local Test Production Build
```bash
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:8000
# open http://localhost:8000
```

### Demo Accounts (both envs)
- Admin: `admin / admin123` → `/admin/login`
- Farmer: `ramesh / farmer123` → `/farmer/login`
