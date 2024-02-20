#!/usr/bin/env python3
""" main file"""
import requests


BASE_URL = "http://localhost:5000/api/v1"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(
        f"{BASE_URL}/users",
        json={"email": email, "password": password}
    )
    assert response.status_code == 201


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password."""
    response = requests.post(
        f"{BASE_URL}/auth_session/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with correct email and password."""
    response = requests.post(
        f"{BASE_URL}/auth_session/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.cookies["_my_session_id"]


def profile_unlogged() -> None:
    """Attempt to access profile while not logged in."""
    response = requests.get(f"{BASE_URL}/users/me")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access profile while logged in."""
    cookies = {"_my_session_id": session_id}
    response = requests.get(f"{BASE_URL}/users/me", cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Log out."""
    cookies = {"_my_session_id": session_id}
    response = requests.delete(f"{BASE_URL}/auth_session/logout", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Reset password and obtain reset token."""
    response = requests.post(f"{BASE_URL}/auth_session/reset_password", json={"email": email})
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using reset token."""
    response = requests.put(
        f"{BASE_URL}/auth_session/reset_password",
        json={"email": email, "reset_token": reset_token, "new_password": new_password}
    )
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
