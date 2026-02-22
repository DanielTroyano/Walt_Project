#!/usr/bin/env bash
# Create a mail.tm email account via their public API

echo ""
echo "========================================"
echo "  mail.tm Email Creator - Starting..."
echo "========================================"
echo ""

API="https://api.mail.tm"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/email_accounts.csv"

# 1. Fetch an available domain
echo "🔍 Fetching available domains..."
DOMAIN=$(curl -s "$API/domains" | python3 -c "
import sys, json
data = json.load(sys.stdin)
# Handle both possible response formats
if isinstance(data, list):
    domains = data
elif 'hydra:member' in data:
    domains = data['hydra:member']
elif 'member' in data:
    domains = data['member']
else:
    domains = data.get('results', data.get('data', []))
if not domains:
    print('ERROR: No domains available', file=sys.stderr)
    sys.exit(1)
print(domains[0]['domain'])
")

if [ -z "$DOMAIN" ]; then
    echo "❌ Failed to get domain"
    exit 1
fi
echo "✅ Domain: $DOMAIN"

# 2. Pick a random name + create account (retry up to 5 times if name is taken)
NAMES_CSV="$SCRIPT_DIR/names.csv"
MAX_RETRIES=5
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_RETRIES ]; do
    ATTEMPT=$((ATTEMPT + 1))

    # Capture both username and names for logging
    PYTHON_RESULT=$(python3 -c "
import csv, random, sys

firsts = []
lasts = []
with open('$NAMES_CSV') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['type'] in ('male_first', 'female_first'):
            firsts.append(row['name'].lower())
        elif row['type'] == 'last':
            lasts.append(row['name'].lower())

first = random.choice(firsts)
last = random.choice(lasts)

# Always append random digits to keep it unique
num = random.randint(10, 9999)
style = random.choice(['dot', 'plain', 'underscore'])
if style == 'dot':
    username = f'{first}.{last}{num}'
elif style == 'plain':
    username = f'{first}{last}{num}'
else:
    username = f'{first}_{last}{num}'

# Output username on stdout, names on stderr
print(username)
print(f'{first.title()}|{last.title()}', file=sys.stderr)
" 2>&1)

    # Extract username and names from the combined output
    EMAIL_USER=$(echo "$PYTHON_RESULT" | grep -v '|' | head -1)
    NAMES_FOR_LOG=$(echo "$PYTHON_RESULT" | grep '|' | head -1)
    ADDRESS="${EMAIL_USER}@${DOMAIN}"
    PASSWORD="$(python3 -c "import random, string; print(''.join(random.choices(string.ascii_letters + string.digits + '!@#', k=16)))")"

    echo ""
    echo "📧 Attempt $ATTEMPT: Creating account $ADDRESS"

    # 3. Create the account
    RESULT=$(curl -s -w "\n%{http_code}" -X POST "$API/accounts" \
      -H "Content-Type: application/json" \
      -d "{\"address\":\"$ADDRESS\",\"password\":\"$PASSWORD\"}")

    HTTP_CODE=$(echo "$RESULT" | tail -1)
    BODY=$(echo "$RESULT" | sed '$d')

    if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
        echo "✅ Account created successfully! (HTTP $HTTP_CODE)"
        ACTUAL_ADDRESS=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('address','unknown'))" 2>/dev/null)
        ACCOUNT_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','unknown'))" 2>/dev/null)
        echo "   ↳ API confirmed address: $ACTUAL_ADDRESS"
        echo "   ↳ Account ID: $ACCOUNT_ID"
        
        # Log the account details
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        FIRST_NAME=$(echo "$NAMES_FOR_LOG" | cut -d'|' -f1)
        LAST_NAME=$(echo "$NAMES_FOR_LOG" | cut -d'|' -f2)
        
        # Create log file header if it doesn't exist
        if [ ! -f "$LOG_FILE" ]; then
            echo "timestamp,email,first_name,last_name,account_id,password" > "$LOG_FILE"
        fi
        
        # Append the new account to the log
        echo "$TIMESTAMP,$ACTUAL_ADDRESS,$FIRST_NAME,$LAST_NAME,$ACCOUNT_ID,$PASSWORD" >> "$LOG_FILE"
        echo "   ↳ Account logged to: email_accounts.csv"
        
        break
    elif echo "$BODY" | grep -q "already used"; then
        echo "⚠️  Address already taken, picking a new name..."
    else
        echo "❌ Failed to create account (HTTP $HTTP_CODE)"
        echo "   ↳ Response: $BODY"
        exit 1
    fi

    if [ $ATTEMPT -eq $MAX_RETRIES ]; then
        echo "❌ Failed after $MAX_RETRIES attempts. Try again later."
        exit 1
    fi
done

# 4. Get auth token to verify it works (use the confirmed address from the API)
LOGIN_ADDRESS="${ACTUAL_ADDRESS:-$ADDRESS}"
echo ""
echo "🔑 Verifying login with: $LOGIN_ADDRESS"
TOKEN_RESULT=$(curl -s -w "\n%{http_code}" -X POST "$API/token" \
  -H "Content-Type: application/json" \
  -d "{\"address\":\"$LOGIN_ADDRESS\",\"password\":\"$PASSWORD\"}")

TOKEN_HTTP=$(echo "$TOKEN_RESULT" | tail -1)
TOKEN_BODY=$(echo "$TOKEN_RESULT" | sed '$d')

if [ "$TOKEN_HTTP" -ge 200 ] && [ "$TOKEN_HTTP" -lt 300 ]; then
    TOKEN=$(echo "$TOKEN_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
    echo "✅ Login verified! (HTTP $TOKEN_HTTP)"
    echo "   ↳ Auth token received (${#TOKEN} chars)"
else
    echo "⚠️  Account created but login verification failed (HTTP $TOKEN_HTTP)"
    echo "   ↳ Response: $TOKEN_BODY"
fi

# 5. Print summary
echo ""
echo "════════════════════════════════════════════"
echo "  📬 YOUR NEW EMAIL ACCOUNT"
echo "════════════════════════════════════════════"
echo "  Requested: $ADDRESS"
echo "  Confirmed: ${ACTUAL_ADDRESS:-$ADDRESS}"
echo "  Password:  $PASSWORD"
echo "  Acct ID:   ${ACCOUNT_ID:-N/A}"
echo "  Web UI:    https://mail.tm"
echo "════════════════════════════════════════════"
echo ""
echo "👉 Log in at https://mail.tm with the CONFIRMED address above."
echo "   Or use the API with your token to read messages programmatically."

# 6. Show all accounts in a formatted table
echo ""
echo "📋 ALL GENERATED ACCOUNTS:"
echo ""
python3 -c "
import csv

with open('$LOG_FILE') as f:
    rows = list(csv.DictReader(f))

if not rows:
    print('  (no accounts yet)')
else:
    # Print header
    print(f'{\"#\":<4} {\"First\":<14} {\"Last\":<14} {\"Email\":<40} {\"Password\":<20} {\"Created\"}')
    print('─' * 115)
    for i, r in enumerate(rows, 1):
        print(f'{i:<4} {r[\"first_name\"]:<14} {r[\"last_name\"]:<14} {r[\"email\"]:<40} {r[\"password\"]:<20} {r[\"timestamp\"]}')
    print()
    print(f'  Total accounts: {len(rows)}')
"
