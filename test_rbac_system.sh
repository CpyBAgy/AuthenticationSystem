#!/bin/bash

ADMIN_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"admin@test.com","password":"Admin123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
MANAGER_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"manager@test.com","password":"Manager123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
USER_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"user1@test.com","password":"User123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")
GUEST_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"guest@test.com","password":"Guest123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])")

echo "Products:"
curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Admin read: ✓' if d.get('success') else '  Admin read: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' -d '{"name":"MacBook Pro M4","price":350000}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Admin create: ✓' if d.get('success') else '  Admin create: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $MANAGER_TOKEN" -H 'Content-Type: application/json' -d '{"name":"iPhone 16 Pro","price":120000}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Manager create: ✓' if d.get('success') else '  Manager create: ✗')"
curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $USER_TOKEN" | python3 -c "import sys, json; d=json.load(sys.stdin); print('  User read: ✓' if d.get('success') else '  User read: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Fake","price":1}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  User create denied: ✓' if not d.get('success') else '  User create denied: ✗')"
curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $GUEST_TOKEN" | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Guest read: ✓' if d.get('success') else '  Guest read: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $GUEST_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Fake","price":1}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Guest create denied: ✓' if not d.get('success') else '  Guest create denied: ✗')"

echo "Orders:"
curl -s -X GET http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Admin read: ✓' if d.get('success') else '  Admin read: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' -d '{"product":"Laptop","quantity":1}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  User create: ✓' if d.get('success') else '  User create: ✗')"
curl -s -X POST http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $GUEST_TOKEN" -H 'Content-Type: application/json' -d '{"product":"Laptop","quantity":1}' | python3 -c "import sys, json; d=json.load(sys.stdin); print('  Guest create denied: ✓' if not d.get('success') else '  Guest create denied: ✗')"
