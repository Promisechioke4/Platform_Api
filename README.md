🚀 Django REST API with JWT Authentication & Redis Caching

This project is a scalable Django REST Framework (DRF) API that implements:

✅ JWT Authentication using djangorestframework-simplejwt

✅ User registration & profile endpoints

✅ Role-based access control (admin/staff vs regular users)

✅ Redis caching for high-performance API responses

✅ Dynamic cache-busting based on URL parameters, user roles, and TTL

✅ Dockerized Redis setup for local development

📌 Features

Authentication & Security

Register new users with JWT token issuance (access & refresh tokens)

Secure endpoints using IsAuthenticated permissions

Role-aware caching for staff vs. normal users

Caching with Redis

Configured via django-redis

Response-level caching using a custom @cache_response decorator

Cache-busting strategy:

🔑 Cache keys vary by user role (staff vs normal user)

🔑 Cache keys vary by authenticated user ID

🔑 Cache keys vary by query parameters

⏳ Cache entries automatically expire based on TTL

Dockerized Redis

Run Redis locally with one command:

docker run -p 6379:6379 -d --name redis redis:7


Verified with:

docker exec -it redis redis-cli ping
# PONG