# Quick Start Guide - AgriCure API

## Start Server (Windows)

```batch
cd "P:\Latest AgriCure\Backend"
start-api.bat
```

## Server URLs

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Main Endpoint (Add Farm Form)

```http
POST http://localhost:8000/soil-data
Content-Type: application/json

{
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

## Frontend Configuration

Create/Update `Frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

## Test API

```bash
python test_api.py
```

## Stop Server

Press `Ctrl+C` in the terminal window

---

**That's it!** The API is integrated with your Add Farm form and ready to use! 🚀
