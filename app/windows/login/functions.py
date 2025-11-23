import socket
import json
from app.windows.login.classes import User

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def send_request(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return json.loads(response)
    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"Network error: {e}")
        return {"status": "error", "message": "Network error"}


def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")


def check_login(username, password):
    response = send_request({
        "action": "check_login",
        "username": username,
        "password": password
    })

    if response.get("status") == "success" and response.get("user"):
        user_data = response["user"]
        return User(
            id=user_data["id"],
            username=user_data["username"],
            password=user_data["password"],
            admin=user_data["admin"],
            authorized=user_data["authorized"]
        )
    return False


def register_user(username, password):
    response = send_request({
        "action": "register_user",
        "username": username,
        "password": password
    })

    return response.get("status") == "success"