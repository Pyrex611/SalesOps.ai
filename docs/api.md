# API Guide

Authentication uses bearer tokens from `/api/v1/auth/login`.

## Example Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"rep@example.com","password":"StrongPass123"}'
```

## Upload Call
```bash
curl -X POST http://localhost:8000/api/v1/calls/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@sample.mp3"
```
