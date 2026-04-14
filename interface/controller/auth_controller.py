import requests


class AuthController:

    def __init__(self):

        self.url = "http://127.0.0.1:8000"
        self.token = None

    def login(self, username, password):

        data = {
            "username": username,
            "password": password
        }

        r = requests.post(f"{self.url}/login", json=data)

        if r.status_code == 200:

            token = r.json()["access_token"]

            self.token = token

            return token   # ← retorna o token

        return None