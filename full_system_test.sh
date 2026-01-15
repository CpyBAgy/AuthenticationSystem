#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS_COUNT=0
FAIL_COUNT=0

check_result() {
    local test_name=$1
    local expected=$2
    local result=$3

    if [[ "$result" == *"$expected"* ]]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((PASS_COUNT++))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        echo -e "${RED}  Expected: $expected${NC}"
        echo -e "${RED}  Got: $result${NC}"
        ((FAIL_COUNT++))
        return 1
    fi
}

echo -e "${BLUE}System Test${NC}"
echo ""
echo -e "${YELLOW}Environment${NC}"

SERVER_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/products/ 2>/dev/null || echo "000")
if [ "$SERVER_CHECK" == "401" ]; then
    echo -e "${GREEN}✓${NC} Server running"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Server not responding (code: $SERVER_CHECK)"
    ((FAIL_COUNT++))
fi

DB_CHECK=$(source venv/bin/activate && python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.users.models import User
print(User.objects.count())
" 2>&1)

if [[ "$DB_CHECK" =~ ^[0-9]+$ ]]; then
    echo -e "${GREEN}✓${NC} Database ($DB_CHECK users)"
    ((PASS_COUNT++))
else
    echo -e "${RED}✗${NC} Database error"
    ((FAIL_COUNT++))
fi

echo ""
echo -e "${YELLOW}Authentication${NC}"

TIMESTAMP=$(date +%s)
REGISTER_RESULT=$(curl -s -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"test_${TIMESTAMP}@example.com\",\"password\":\"Test123!\",\"password_confirm\":\"Test123!\",\"first_name\":\"Test\",\"last_name\":\"User\"}")

check_result "Register user" "success" "$REGISTER_RESULT"
ADMIN_LOGIN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"admin@test.com","password":"Admin123!"}')
ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
echo -e "${GREEN}✓${NC} Login: admin"
((PASS_COUNT++))

MANAGER_LOGIN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"manager@test.com","password":"Manager123!"}')
MANAGER_TOKEN=$(echo "$MANAGER_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
echo -e "${GREEN}✓${NC} Login: manager"
((PASS_COUNT++))

USER_LOGIN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"user1@test.com","password":"User123!"}')
USER_TOKEN=$(echo "$USER_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
echo -e "${GREEN}✓${NC} Login: user"
((PASS_COUNT++))

GUEST_LOGIN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"guest@test.com","password":"Guest123!"}')
GUEST_TOKEN=$(echo "$GUEST_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
echo -e "${GREEN}✓${NC} Login: guest"
((PASS_COUNT++))
REFRESH_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"admin@test.com","password":"Admin123!"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['refresh_token'])" 2>/dev/null)
REFRESH_RESULT=$(curl -s -X POST http://127.0.0.1:8000/api/auth/refresh/ -H 'Content-Type: application/json' -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}")
check_result "Refresh token" "success" "$REFRESH_RESULT"

echo ""
echo -e "${YELLOW}Profile${NC}"

PROFILE_RESULT=$(curl -s -X GET http://127.0.0.1:8000/api/users/me/ -H "Authorization: Bearer $ADMIN_TOKEN")
check_result "Get profile" "admin@test.com" "$PROFILE_RESULT"

UPDATE_RESULT=$(curl -s -X PATCH http://127.0.0.1:8000/api/users/me/ -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' -d '{"first_name":"AdminUpdated"}')
check_result "Update profile" "success" "$UPDATE_RESULT"

echo ""
echo -e "${YELLOW}RBAC - Products${NC}"
ADMIN_CREATE=$(curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $ADMIN_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Test Product","price":1000}')
check_result "Admin create product" "success" "$ADMIN_CREATE"

MANAGER_CREATE=$(curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $MANAGER_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Manager Product","price":2000}')
check_result "Manager create product" "success" "$MANAGER_CREATE"

USER_READ=$(curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $USER_TOKEN")
check_result "User read products" "success" "$USER_READ"

USER_CREATE=$(curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Fake","price":1}')
check_result "User create denied (403)" "permission" "$USER_CREATE"

GUEST_READ=$(curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $GUEST_TOKEN")
check_result "Guest read products" "success" "$GUEST_READ"

GUEST_CREATE=$(curl -s -X POST http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer $GUEST_TOKEN" -H 'Content-Type: application/json' -d '{"name":"Fake","price":1}')
check_result "Guest create denied (403)" "permission" "$GUEST_CREATE"

echo ""
echo -e "${YELLOW}RBAC - Orders${NC}"

ADMIN_ORDERS=$(curl -s -X GET http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $ADMIN_TOKEN")
check_result "Admin read orders" "success" "$ADMIN_ORDERS"

USER_ORDER=$(curl -s -X POST http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $USER_TOKEN" -H 'Content-Type: application/json' -d '{"product":"Laptop","quantity":1}')
check_result "User create order" "success" "$USER_ORDER"

GUEST_ORDER=$(curl -s -X POST http://127.0.0.1:8000/api/orders/ -H "Authorization: Bearer $GUEST_TOKEN" -H 'Content-Type: application/json' -d '{"product":"Laptop","quantity":1}')
check_result "Guest create denied (403)" "permission" "$GUEST_ORDER"

echo ""
echo -e "${YELLOW}Admin API${NC}"

ADMIN_ROLES=$(curl -s -X GET http://127.0.0.1:8000/api/admin/roles/ -H "Authorization: Bearer $ADMIN_TOKEN")
check_result "Admin get roles" "success" "$ADMIN_ROLES"

ADMIN_ELEMENTS=$(curl -s -X GET http://127.0.0.1:8000/api/admin/business-elements/ -H "Authorization: Bearer $ADMIN_TOKEN")
check_result "Admin get elements" "success" "$ADMIN_ELEMENTS"

ADMIN_RULES=$(curl -s -X GET http://127.0.0.1:8000/api/admin/access-rules/ -H "Authorization: Bearer $ADMIN_TOKEN")
check_result "Admin get rules" "success" "$ADMIN_RULES"

USER_RULES=$(curl -s -X GET http://127.0.0.1:8000/api/admin/access-rules/ -H "Authorization: Bearer $USER_TOKEN")
check_result "User access denied (403)" "permission" "$USER_RULES"

echo ""
echo -e "${YELLOW}Security${NC}"

NO_TOKEN=$(curl -s -X GET http://127.0.0.1:8000/api/products/)
check_result "No token denied (401)" "Authentication required" "$NO_TOKEN"

INVALID_TOKEN=$(curl -s -X GET http://127.0.0.1:8000/api/products/ -H "Authorization: Bearer invalid_token_here")
check_result "Invalid token denied" "Invalid" "$INVALID_TOKEN"

echo ""
echo -e "${BLUE}Results${NC}"
TOTAL=$((PASS_COUNT + FAIL_COUNT))
SUCCESS_RATE=$((PASS_COUNT * 100 / TOTAL))

echo -e "${GREEN}Passed: $PASS_COUNT${NC}"
echo -e "${RED}Failed: $FAIL_COUNT${NC}"
echo "Total: $TOTAL ($SUCCESS_RATE%)"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All tests passed${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    exit 1
fi
