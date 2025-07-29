class EdmError(Exception):
    pass


class EdmAPIError(EdmError):
    pass


class EdmEulaError(EdmError):
    def __init__(self, *args, **kwargs):
        self.description = kwargs.pop("description", None)
        self.eula_url = kwargs.pop("eula_url", None)
        super().__init__(*args, **kwargs)


class EdmAuthError(EdmError):
    pass


class EdmTokenNotFoundError(EdmAuthError):
    pass


class EdmTokenExpiredError(EdmAuthError):
    pass
