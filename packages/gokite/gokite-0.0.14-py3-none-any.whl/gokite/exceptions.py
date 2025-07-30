class KiteError(Exception):
    pass


class KiteAuthenticationError(KiteError):
    pass


class KitePaymentError(KiteError):
    pass


class KiteNetworkError(KiteError):
    pass


class KiteNotFoundError(KiteError):
    pass
