class BaseFacadeService:
    def __getattr__(self, item):
        pass


class CurrencyFacadeSerivce(BaseFacadeService):
    pass


class DirectionFacadeService(BaseFacadeService):
    pass


class ExchangerFacadeService(BaseFacadeService):
    pass


class KycVerificationFacadeService(BaseFacadeService):
    pass


class MethodFacadeService(BaseFacadeService):
    pass


class OrderFacadeService(BaseFacadeService):
    pass


class PaymentFacadeService(BaseFacadeService):
    pass


class RateFacadeService(BaseFacadeService):
    pass


class RateSourceFacadeService(BaseFacadeService):
    pass


class RequestFacadeService(BaseFacadeService):
    pass


class UserFacadeService(BaseFacadeService):
    pass
