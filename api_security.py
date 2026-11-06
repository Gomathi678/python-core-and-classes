
import os
import hmac
import hashlib
import requests

from pathlib import Path
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 1. Load environment variables

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("API_KEY or WEBHOOK_SECRET missing in .env")


# 2. Create requests Session with retry logic

def create_session() -> requests.Session:

    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={"GET"}
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


# 3. Fetch users from REST API

def fetch_users() -> None:

    url = "https://jsonplaceholder.typicode.com/users"

    session = create_session()

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()

        users = response.json()

        print("===== FIRST 5 USERS =====")

        for user in users[:5]:
            print(
                f"{user.get('id')} - "
                f"{user.get('name')} - "
                f"{user.get('email')}"
            )

        # 4. Access nested JSON using .get() only

        if users:
            first_user = users[0]

            address = first_user.get("address", {})
            geo = address.get("geo", {})
            company = first_user.get("company", {})

            city = address.get("city") or "Not Available"
            latitude = geo.get("lat") or "Not Available"
            zip_code = address.get("zip") or "Not Available"
            company_name = company.get("name") or "Not Available"

            print("\n===== FIRST USER DETAILS =====")
            print(f"City: {city}")
            print(f"Latitude: {latitude}")
            print(f"Zip: {zip_code}")
            print(f"Company: {company_name}")

    except requests.RequestException as error:
        print("API request failed:", error)

    finally:
        session.close()


# 5. Verify HMAC-SHA256 signature

def verify_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# 6. Test valid, tampered and wrong-secret cases

def test_webhook() -> None:

    payload = b'{"employee_id": 101, "event": "employee_created"}'

    secret = WEBHOOK_SECRET

    # Generate correct signature
    valid_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Valid payload
    valid = verify_signature(
        payload,
        valid_signature,
        secret
    )

    # Tampered payload
    tampered_payload = (
        b'{"employee_id": 102, "event": "employee_created"}'
    )

    tampered = verify_signature(
        tampered_payload,
        valid_signature,
        secret
    )

    # Wrong secret
    wrong_secret = verify_signature(
        payload,
        valid_signature,
        "wrong_secret"
    )

    print("\n===== WEBHOOK SECURITY =====")

    print(
        f"Valid: {valid} | "
        f"Tampered: {tampered} | "
        f"Wrong secret: {wrong_secret}"
    )


# 7. Main program

if __name__ == "__main__":

    fetch_users()

    test_webhook()
