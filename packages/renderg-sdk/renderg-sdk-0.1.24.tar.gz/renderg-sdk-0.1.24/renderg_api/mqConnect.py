class MqConnect:
    def __init__(self, auth_key):
        self._auth_key = auth_key

    def get_key(self):
        return self._auth_key
