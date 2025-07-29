# Basic Authentication With Flask
This project demonstrates a secure and modular JWT-based authentication system using **Flask**, **Blueprints**, and **SQLite**. It includes features such as user registration, login, token refresh, password change/reset, token revocation, and secure cookie handling.


## Setup

- Create python environment with version `3.12`
- Run pip install -r requirements.txt
- Run the application using `python app.py` ( ensure you are in the current directory)
- Also if you are using a vscode, the configuration of the debugger using flask has been added.

## 🚀 Features Implemented

### ✅ JWT Authentication

- Access & Refresh tokens issued on successful login.
- Access token used for protected routes (expires quickly).
- Refresh token stored as **HTTP-only secure cookie** (longer expiry).

### 🔐 User Authentication

- **Registration**: Creates a new user with hashed password.
- **Login**: Validates credentials and returns tokens.
- **Logout**: Revokes the refresh token.

### 🔁 Token Management

- **Refresh token** endpoint: issues new access token using valid refresh token.
- **Token Revocation**: Implements revocation list to prevent reuse of old refresh tokens.

### 🔄 Password Management

- **Change password**: Authenticated user can update their password.
- **Reset password**: Simulates reset with token (you can integrate email later).

### ⚠️ Security

- Tokens stored securely:
  - Access token returned in response.
  - Refresh token stored as **HTTP-only secure cookie**.
- **Rate Limiting** (optional): Can be added to protect login from brute-force.
- **Password hashing** using Werkzeug.

---

## 🔗 API Endpoints

### 🔐 Auth Routes

| Endpoint                   | Method | Auth Required | Description                       |
|---------------------------|--------|----------------|-----------------------------------|
| `/api/register`           | POST   | ❌             | Register a new user               |
| `/api/login`              | POST   | ❌             | Login user, returns tokens        |
| `/api/logout`             | POST   | ✅             | Logs user out, revokes token      |
| `/api/refresh`            | POST   | ✅ (cookie)    | Refresh access token              |
| `/api/change-password`    | POST   | ✅             | Authenticated user changes password |
| `/api/reset-password`     | POST   | ❌             | Simulate password reset by reset token  |


## 🔐 API Reference

### 📌 Base URL
```
http://localhost:5000/
```

---

### 📤 Register a New User

**Endpoint:**
```
POST /api/register
```

**Request Body (JSON):**
```json
{
  "username": "johndoe",
  "password": "secret"
}
```

**Responses:**
- `201 Created` – User registered successfully
- `400 Bad Request` – Username already exists

---

### 🔑 Login and Get JWT Token

**Endpoint:**
```
POST /api/login
```

**Request Body (JSON):**
```json
{
  "username": "johndoe",
  "password": "secret"
}
```

**Responses:**
- `200 OK` – Returns an access token
```json
{
  "access_token": "your_jwt_token_here"
}
```
- `401 Unauthorized` – Invalid credentials

---

### 🔑 Refresh JWT Token

**Endpoint:**
```
POST /api/refresh

(Cookie: refresh_token)
```

**Responses:**
- `200 OK` – Returns an access token
```json
{
  "access_token": "<new JWT>"
}
```
---

### 🔒 Access Protected Route

**Endpoint:**
```
GET /api/data
```

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Responses:**
- `200 OK`
```json
{
  "message": "Dear johndoe,  you have accessed a secure route."
}
```
- `401 Unauthorized` – Missing or invalid token

---
















### 🔒 Change Password

**Endpoint:**
```
POST /api/change-password
```

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Request Body (JSON):**
```json
{
  "old_password": "johndoe",
  "new_password": "secret"
}
```

**Responses:**
- `200 OK`
```json
{
  "message": "Password changed successfully."
}
```
- `401 Unauthorized` – Missing or invalid token

---


### 🧪 Test with `curl`

```bash
# Register
curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "secret"}'

# Login
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "secret"}'

# Refresh token
curl -X POST http://localhost:5000/api/refresh -H "Content-Type: application/json"

# Change password
curl -X POST http://localhost:5000/api/change-password -H "Content-Type: application/json" \
-d '{"old_password": "johndoe", "new_password": "secret"}'

# Protected (replace <TOKEN>)
curl -X GET http://localhost:5000/api/data \
-H "Authorization: Bearer <TOKEN>"
```
