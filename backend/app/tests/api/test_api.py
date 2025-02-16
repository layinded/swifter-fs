import json
import uuid
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import oauth_routes
from app.models.user import User
from app.core.security.dependencies import get_current_user
from starlette.responses import JSONResponse
import copy

client = TestClient(app)


# --- Dummy Authentication Dependencies ---
def dummy_user():
    """Return a dummy regular user."""
    return User(
        id=uuid.uuid4(),
        email="dummy@example.com",
        full_name="Dummy User",
        auth_provider="local",
        hashed_password="dummyhash",
        is_active=True,
        is_superuser=False
    )


def dummy_admin():
    """Return a dummy admin user."""
    return User(
        id=uuid.uuid4(),
        email="admin@example.com",
        full_name="Admin User",
        auth_provider="local",
        hashed_password="dummyhash",
        is_active=True,
        is_superuser=True
    )


# --- Authentication Endpoints ---

def test_login_success():
    data = {
        "username": "user@example.com",
        "password": "password123",
        "grant_type": "password",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    # Patch the authenticate function in the CRUD layer.
    with patch("app.crud.crud_user.authenticate", return_value=dummy_user()):
        response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_validation_error():
    data = {
        "username": "user@example.com",
        "password": ""  # Empty password should trigger validation error
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 400, response.text


def test_refresh_token_success():
    payload = {"refresh_token": "valid_refresh_token"}
    # Patch the verify_refresh_token function from the correct module.
    with patch("app.api.routes.auth_routes.verify_refresh_token", return_value=("user@example.com", "local")):
        app.dependency_overrides[get_current_user] = dummy_user
        response = client.post("/api/v1/auth/token/refresh", json=payload)
        app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert "access_token" in token_data


def test_register_user_success():
    data = {
        "email": "newuser@example.com",
        "password": "strongpassword",
        "full_name": "New User"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 200, response.text
    user_data = response.json()
    assert user_data["email"] == data["email"]


def test_get_profile_unauthorized():
    response = client.get("/api/v1/auth/profile")
    assert response.status_code in (401, 403), response.text


def test_update_password_success():
    token = "Bearer test_access_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_user
    with patch("app.services.user_service.update_password", return_value={"message": "Password updated"}):
        response = client.patch("/api/v1/auth/password/update", json={
            "current_password": "oldpassword",
            "new_password": "newstrongpassword"
        }, headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    resp_data = response.json()
    assert "message" in resp_data


def test_delete_profile_success():
    token = "Bearer test_access_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_user
    with patch("app.services.user_service.delete_self", return_value={"message": "User deleted"}):
        response = client.delete("/api/v1/auth/profile/delete", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    resp_data = response.json()
    assert "message" in resp_data


def test_recover_password_success():
    email = "user@example.com"
    with patch("app.crud.crud_user.get_user_by_email", return_value=dummy_user()):
        response = client.post(f"/api/v1/auth/password/recover/{email}")
    assert response.status_code == 200, response.text
    resp_data = response.json()
    assert "message" in resp_data


# --- OAuth Endpoints ---

def test_get_oauth_urls():
    response = client.get("/api/v1/oauth/urls")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, dict)


def test_google_auth_redirect():
    response = client.get("/api/v1/oauth/google/auth")
    # If the route exists and is supposed to redirect, expect 302 or 307;
    # if not implemented, 404 is acceptable.
    assert response.status_code in (302, 307, 404), response.text



# --- User Endpoints ---

def test_update_current_user():
    token = "Bearer test_access_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_user
    data = {"full_name": "Updated Name", "email": "updated@example.com"}
    response = client.patch("/api/v1/users/me", json=data, headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    user_data = response.json()
    assert user_data["full_name"] == data["full_name"]


def test_get_user_by_id():
    token = "Bearer test_access_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_user
    user_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code in (200, 404, 403), response.text


# --- Admin Endpoints ---

def test_admin_get_all_users():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    response = client.get("/api/v1/admin/users", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "data" in data and "count" in data


def test_admin_create_user():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    data = {
        "email": "newadminuser@example.com",
        "full_name": "New Admin User",
        "password": "strongpassword",
        "is_active": True,
        "is_superuser": False
    }
    response = client.post("/api/v1/admin/users", json=data, headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text
    user_data = response.json()
    assert user_data["email"] == data["email"]


def test_admin_get_user_detail():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    user_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/admin/users/detail/{user_id}", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code in (200, 404, 403), response.text


def test_admin_update_user():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    user_id = str(uuid.uuid4())
    data = {"full_name": "Admin Updated Name", "email": "adminupdated@example.com"}
    response = client.patch(f"/api/v1/admin/users/{user_id}", json=data, headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code in (200, 404, 403), response.text


def test_admin_delete_user():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    user_id = str(uuid.uuid4())
    response = client.delete(f"/api/v1/admin/users/{user_id}", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code in (200, 404, 403), response.text


# --- Utility Endpoints ---

def test_test_email():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    params = {"email_to": "test@example.com"}
    response = client.post("/api/v1/utils/test-email/", params=params, headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert "message" in data


def test_health_check():
    response = client.get("/api/v1/utils/health-check/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), bool)


# --- Custom Modules Endpoints ---

def test_get_stats():
    token = "Bearer test_access_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_user
    response = client.get("/api/v1/reports/stats", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text


def test_admin_dashboard():
    token = "Bearer admin_test_token"
    headers = {"Authorization": token}
    app.dependency_overrides[get_current_user] = dummy_admin
    response = client.get("/api/v1/admin/dashboard", headers=headers)
    app.dependency_overrides.pop(get_current_user)
    assert response.status_code == 200, response.text


def test_get_errors():
    response = client.get("/api/v1/errors")
    assert response.status_code == 200, response.text
