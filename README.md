# basic_auth
This module is a basic authentication using Flask created for learning purpose


## Setup

- Create python environment with version `3.12`
- Run pip install -r requirements.txt
- Run the application using `python app.py` ( ensure you are in the current directory)
- Also if you are using a vscode, the configuration of the debugger using flask has been added.


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

### 🧪 Test with `curl`

```bash
# Register
curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "secret"}'

# Login
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "secret"}'

# Protected (replace <TOKEN>)
curl -X GET http://localhost:5000/api/data \
-H "Authorization: Bearer <TOKEN>"
```
