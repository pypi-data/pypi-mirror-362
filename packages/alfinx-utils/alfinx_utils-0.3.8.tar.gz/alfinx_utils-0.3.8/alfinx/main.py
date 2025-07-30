import os
from dotenv import load_dotenv
import httpx
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException, Request

load_dotenv()

X_SERVICE_ORIGIN_CODE = os.getenv("X_SERVICE_ORIGIN_CODE")
AUTHENTICATION_API_URL = os.getenv("AUTHENTICATION_API_URL")
DECREACE_USER_TOKEN_API_URL = os.getenv("DECREACE_USER_TOKEN_API_URL")
MONGO_API_URL = os.getenv("MONGO_API_URL")
MONGO_API_USERNAME = os.getenv("MONGO_API_USERNAME")
MONGO_API_PASSWORD = os.getenv("MONGO_API_PASSWORD")

if not AUTHENTICATION_API_URL:
    raise RuntimeError("AUTHENTICATION_API_URL env var not set")
if not X_SERVICE_ORIGIN_CODE:
    raise RuntimeError("X_SERVICE_ORIGIN_CODE env var not set")

async def check_authentication(request: Request):
    headers = dict(request.headers)

    if "x-api-key" not in headers:
        return  HTTPException(401, detail="API key is missing")
    if "x-service-code" not in headers:
        return  HTTPException(401, detail="Service code is missing")

    auth_headers = {
        "x-api-key": headers["x-api-key"],
        "x-service-code": headers["x-service-code"],
        "x-service-origin-code": X_SERVICE_ORIGIN_CODE,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AUTHENTICATION_API_URL, headers=auth_headers)
    except httpx.RequestError as exc:
        raise HTTPException(503, detail="Authentication service is unavailable") from exc

    if response.status_code != 200:
        try:
            error_detail = response.json().get("detail", "Authentication failed")
        except Exception:
            error_detail = "Authentication failed"
        return HTTPException(response.status_code, detail=error_detail)

    masked_key = f"{auth_headers['x-api-key'][:6]}{auth_headers['x-api-key'][-6:]}"
    return masked_key, auth_headers["x-service-code"]



async def decrease_user_limit(headers: dict, input_text_length: str):
    if "x-api-key" not in headers or "x-service-code" not in headers:
        return Exception("API key or Service code is missing")

    auth_headers = {
        "x-api-key": headers["x-api-key"],
        "x-service-code": headers["x-service-code"],
        "x-token-count": input_text_length,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(DECREACE_USER_TOKEN_API_URL, headers=auth_headers)

    if response.status_code != 200:
        try:
            error_detail = response.json().get("detail", None)
            if not error_detail:
                error_detail = f"Authentication failed (Status: {response.status_code})"
        except Exception:
            error_detail = f"Authentication failed (Status: {response.status_code}, raw: {response.text})"

        raise HTTPException(response.status_code, detail=error_detail)


    return response.json()


def save_data_on_mongo(collection_name: str, data: dict, celery_app=None):
    
    def _post_to_mongo(collection_name, data):
        response = httpx.post(
            MONGO_API_URL,
            json={"collection_name": collection_name, "data": data},
            auth=HTTPBasicAuth(MONGO_API_USERNAME, MONGO_API_PASSWORD),
        )
        if response.status_code != 201:
            response.raise_for_status()
        return response.json()

    if celery_app:
        @celery_app.task
        def _task(collection_name, data):
            return _post_to_mongo(collection_name, data)
        return _task.delay(collection_name, data)
    else:
        return _post_to_mongo(collection_name, data)
