# libraries
import socket
import json
from typing import Optional

# user libraries
from app.windows.login.classes import User
from app.config import SERVER_HOST, SERVER_PORT

# function for send request
def send_request(request: dict) -> dict:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return json.loads(response)
    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"Network error: {e}")
        return {"status": "error", "message": "Network error"}

# method for toggle password
def toggle_password(p_block, show_password_var) -> None:
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")

# method for user authorization
def check_login(username: str, password: str) -> Optional[User]:
    response = send_request({
        "action": "check_login",
        "username": username,
        "password": password
    })

    if response["status"] == "success" and response.get("user"):
        user_data = response["user"]
        user_data['password'] = 'password'

        return User(**user_data)

    return None

def register_user(username: str, password: str) -> bool:
    response = send_request({
        "action": "register_user",
        "username": username,
        "password": password
    })

    return response.get("status") == "success"