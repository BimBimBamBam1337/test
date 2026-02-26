class MessageEmpty(Exception):
    pass


class DBError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class StorageError(Exception):
    pass


class UserError(StorageError):
    pass


class UserAlreadyExistsError(UserError):
    pass


class UserNotFoundError(UserError):
    pass
