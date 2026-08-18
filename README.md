# MIK

Estrutura igual ao projeto Trust (backend + frontend separados).

```
MIK/
├── api/              # App Django (models, views, serializers, API)
├── config/           # Settings, urls, wsgi
├── frontend/         # HTML/CSS/JS estático
│   ├── CSS/
│   ├── SCRIPT/
│   ├── IMG/
│   ├── login.html
│   ├── index.html
│   └── ...
├── media/            # Uploads
├── manage.py
├── requirements.txt
└── README.md
```

## Backend

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/`

## Frontend

Edita `frontend/SCRIPT/config.js`:

```js
window.MIK_API_URL = 'http://127.0.0.1:8000';
```

Serve a pasta `frontend/`:

```bash
npx serve frontend
```

## Hospedagem

| Parte | Onde |
|-------|------|
| Backend (`api` + `config`) | Render, Railway, PythonAnywhere |
| Frontend | Netlify, Vercel, Cloudflare Pages |
