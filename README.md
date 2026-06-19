# AgroVision Full Stack

This project is a full stack agriculture AI platform with a Django REST backend and a React/Vite frontend.

## Backend

- Django REST framework with JWT auth
- PostgreSQL database support via `DATABASE_URL`
- Admin panel at `/admin/`
- API docs at `/api/docs/`

### Run locally with Docker

```powershell
cd Backend
docker compose up --build
```

### Local environment setup

1. Copy `.env.example` to `.env`
2. Set `DATABASE_URL=postgres://agro_user:agro_pass@localhost:5432/agro_db`
3. Run migrations:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

## Frontend

- Vite + React application
- API client configured from `Frontend/src/api/client.js`
- Frontend environment sample in `Frontend/.env.example`

### Run frontend

```powershell
cd Frontend
npm install
npm run dev
```

## Notes

- The backend uses PostgreSQL for production and local full-stack development.
- The frontend can be toggled out of mock mode with `VITE_USE_MOCKS=false`.
