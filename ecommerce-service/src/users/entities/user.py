class User():

    def __init__(self, id=None, username=None, password=None, created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.username = username
        self.password = password

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @classmethod
    def from_dict(cls, dict):
        username = dict.get("username")
        password = dict.get("password")

        return User(username, password)
