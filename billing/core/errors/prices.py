from .base import BusinessError


class InvalidPriceTiersError(BusinessError):
    pass


class InvalidPriceTiersModeError(BusinessError):
    pass


class PriceNotFoundError(BusinessError):
    pass


class InvalidPriceError(BusinessError):
    pass

