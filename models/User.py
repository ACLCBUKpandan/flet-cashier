from pocketbase.client import Record


class User(Record):

    username: str
    avatar: str

    def load(self, data: dict):
        super().load(data)
        self.username = data.get('username', '')
        self.avatar = data.get('avatar', '')
        return self
