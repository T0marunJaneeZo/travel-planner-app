# Backend

Python/FastAPI backend for the travel planner app.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set `OPENAI_API_KEY` in `backend/.env` before calling `POST /api/generate-trip`.

## Endpoints

- `GET /health`
- `POST /api/generate-trip`

## Example request

```bash
curl -X POST http://127.0.0.1:8000/api/generate-trip \
  -H "Content-Type: application/json" \
  -d '{"prompt":"明日、東京から日帰りで鎌倉に行きたい。海とカフェと寺を入れて。"}'
```
