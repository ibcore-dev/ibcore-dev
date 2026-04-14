import requests


class ChatController:

    def __init__(self, token):

        self.url = "http://127.0.0.1:8000/command"
        self.token = token

    def send_message(self, message):

        data = {
            "token": self.token,
            "input": message
        }

        try:

            r = requests.post(self.url, json=data)

            print("STATUS:", r.status_code)
            print("RESPONSE:", r.text)

            if r.status_code == 200:

                return r.json()["response"]

            return f"Erro servidor: {r.text}"

        except Exception as e:

            return f"Erro conexão: {e}"